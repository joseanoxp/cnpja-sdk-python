"""Testes de DTOs, enums e aliases (regression dos bugs descobertos)."""

from __future__ import annotations

import pytest

from cnpja.types import (
    CccDto,
    MemberDto,
    OfficeReadParams,
    OfficeSearchParams,
    OfficeSuframaDto,
    PersonDto,
    PersonMemberDto,
    RegistrationDto,
    RfbMemberDto,
)
from cnpja.types._enums import CacheStrategy, EmailOwnership, PhoneType, State


class TestRelaxedNullableFields:
    """Bug histórico: DTOs tinham campos obrigatórios que vêm null na API real."""

    def test_member_since_is_nullable(self) -> None:
        m = MemberDto.model_validate(
            {
                "person": {"type": "NATURAL", "name": "João"},
                "role": {"id": 49, "text": "Sócio"},
            }
        )
        assert m.since is None

    def test_rfb_member_since_is_nullable(self) -> None:
        m = RfbMemberDto.model_validate(
            {
                "role": {"id": 49, "text": "Sócio"},
                "person": {"type": "NATURAL", "name": "João"},
            }
        )
        assert m.since is None

    def test_person_member_since_is_nullable(self) -> None:
        m = PersonMemberDto.model_validate(
            {
                "role": {"id": 49, "text": "Sócio"},
                "company": {
                    "id": 1,
                    "name": "X",
                    "equity": 0.0,
                    "nature": {"id": 2062, "text": "LTDA"},
                    "size": {"id": 1, "acronym": "ME", "text": "ME"},
                },
            }
        )
        assert m.since is None

    def test_person_id_is_nullable(self) -> None:
        p = PersonDto.model_validate({"type": "NATURAL", "name": "Anônimo", "membership": []})
        assert p.id is None

    def test_registration_status_date_is_nullable(self) -> None:
        r = RegistrationDto.model_validate(
            {
                "number": "123",
                "state": "SP",
                "enabled": True,
                "status": {"id": 1, "text": "OK"},
                "type": {"id": 1, "text": "Normal"},
            }
        )
        assert r.status_date is None

    def test_office_suframa_dates_are_nullable(self) -> None:
        o = OfficeSuframaDto.model_validate(
            {
                "number": "200400029",
                "approved": True,
                "status": {"id": 1, "text": "Ativa"},
                "incentives": [],
            }
        )
        assert o.since is None
        assert o.approval_date is None

    def test_ccc_updated_is_nullable(self) -> None:
        c = CccDto.model_validate(
            {
                "taxId": "37335118000180",
                "name": "X",
                "originState": "SP",
                "registrations": [],
            }
        )
        assert c.updated is None


class TestEnumSerialization:
    """Bug histórico: enums eram serializados como 'State.SP' em vez de 'SP'."""

    def test_state_enum_serializes_as_value(self) -> None:
        p = OfficeSearchParams.model_validate({"address.state.in": ["SP", "RJ"]})
        dump = p.model_dump(by_alias=True, exclude_none=True)
        assert dump["address.state.in"] == ["SP", "RJ"]

    def test_cache_strategy_serializes_as_value(self) -> None:
        p = OfficeReadParams.model_validate(
            {"tax_id": "37335118000180", "strategy": "CACHE_IF_FRESH"}
        )
        dump = p.model_dump(by_alias=True, exclude_none=True, exclude={"tax_id"})
        assert dump["strategy"] == "CACHE_IF_FRESH"

    def test_phone_type_and_email_ownership_as_value(self) -> None:
        p = OfficeSearchParams.model_validate(
            {
                "phones.type.in": ["MOBILE", "LANDLINE"],
                "emails.ownership.in": ["CORPORATE"],
            }
        )
        dump = p.model_dump(by_alias=True, exclude_none=True)
        assert dump["phones.type.in"] == ["MOBILE", "LANDLINE"]
        assert dump["emails.ownership.in"] == ["CORPORATE"]


class TestAliasCorrectness:
    """Regression: aliases que divergiam da API real."""

    def test_side_activities_alias_is_plural(self) -> None:
        p = OfficeSearchParams.model_validate({"sideActivities.id.in": [4751201]})
        dump = p.model_dump(by_alias=True, exclude_none=True)
        assert "sideActivities.id.in" in dump
        assert "sideActivity.id.in" not in dump

    def test_main_activity_alias_stays_singular(self) -> None:
        p = OfficeSearchParams.model_validate({"mainActivity.id.in": [6311900]})
        dump = p.model_dump(by_alias=True, exclude_none=True)
        assert dump["mainActivity.id.in"] == [6311900]

    def test_new_p0_filters_serialize_correctly(self) -> None:
        p = OfficeSearchParams.model_validate(
            {
                "address.street.in": ["Av Paulista"],
                "address.zip.in": ["01310100"],
                "address.country.id.in": [76],
                "activities.id.in": [6311900],
                "emails.domain.in": ["cnpja.com"],
                "phones.number.in": ["971564144"],
            }
        )
        dump = p.model_dump(by_alias=True, exclude_none=True)
        for alias in [
            "address.street.in",
            "address.zip.in",
            "address.country.id.in",
            "activities.id.in",
            "emails.domain.in",
            "phones.number.in",
        ]:
            assert alias in dump, f"alias ausente: {alias}"


class TestEnumValidInputs:
    @pytest.mark.parametrize(
        "value",
        ["CACHE", "CACHE_IF_FRESH", "CACHE_IF_ERROR", "ONLINE"],
    )
    def test_cache_strategy_accepts_all_values(self, value: str) -> None:
        assert CacheStrategy(value).value == value

    def test_phone_type_values(self) -> None:
        assert PhoneType.MOBILE.value == "MOBILE"
        assert PhoneType.LANDLINE.value == "LANDLINE"

    def test_email_ownership_values(self) -> None:
        assert {e.value for e in EmailOwnership} == {
            "PERSONAL",
            "CORPORATE",
            "ACCOUNTING",
        }

    def test_state_has_27_ufs(self) -> None:
        assert len(list(State)) == 27
