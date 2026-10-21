"""Testes de DTOs, enums e aliases (regression dos bugs descobertos)."""

from __future__ import annotations

import pytest

from cnpja.types import (
    CccDto,
    CompanyDto,
    MemberDto,
    OfficeCompanyDto,
    OfficeDto,
    OfficeReadParams,
    OfficeSearchParams,
    OfficeSuframaDto,
    PersonDto,
    PersonMemberCompanyDto,
    PersonMemberDto,
    RegistrationDto,
    RfbMemberDto,
    SimplesDto,
    SimplesEventDto,
    SimplesEventRegime,
    SimplesNacionalDto,
    SimplesSimeiDto,
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
                    "id": "1",
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


class TestAlphanumericCompanyIdentifiers:
    """Company roots are strings because new CNPJs may contain letters."""

    company = {
        "id": "12ABC345",
        "name": "Empresa Alfanumérica",
        "equity": 0.0,
        "nature": {"id": 2062, "text": "Sociedade Empresária Limitada"},
        "size": {"id": 1, "acronym": "ME", "text": "Microempresa"},
    }

    def test_office_company_accepts_alphanumeric_identifier(self) -> None:
        company = OfficeCompanyDto.model_validate({**self.company, "members": []})

        assert company.id == "12ABC345"

    def test_company_accepts_alphanumeric_identifier(self) -> None:
        company = CompanyDto.model_validate({**self.company, "members": [], "offices": []})

        assert company.id == "12ABC345"

    def test_person_membership_accepts_alphanumeric_company_identifier(self) -> None:
        company = PersonMemberCompanyDto.model_validate(self.company)

        assert company.id == "12ABC345"


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


class TestExtraFieldsIgnored:
    """Tolerância a adições retrocompatíveis da API (extra='ignore')."""

    def test_base_model_ignores_unmapped_fields(self) -> None:
        c = OfficeCompanyDto.model_validate(
            {
                "id": "12345678",
                "name": "Empresa Teste",
                "equity": 1000.0,
                "nature": {"id": 2062, "text": "LTDA"},
                "size": {"id": 1, "acronym": "ME", "text": "ME"},
                "members": [],
                "unmappedField": "should_be_ignored",
                "futureApiPayload": {"deep": [1, 2, 3]},
            }
        )
        assert c.name == "Empresa Teste"
        assert not hasattr(c, "unmappedField")

    def test_nested_dto_ignores_extra_fields(self) -> None:
        s = SimplesNacionalDto.model_validate(
            {
                "optant": False,
                "since": None,
                "futureTaxReformFlag": True,
                "extraDetail": "ignored",
            }
        )
        assert s.optant is False
        assert s.since is None


class TestSimplesNacionalEvents:
    """Suporte a SimplesNacionalDto, SimplesEventDto e compatibilidade com SimplesSimeiDto."""

    def test_simples_event_regime_enum(self) -> None:
        assert SimplesEventRegime.IBS.value == "IBS"
        assert SimplesEventRegime.CBS.value == "CBS"

    def test_simples_event_dto_deserialization(self) -> None:
        event = SimplesEventDto.model_validate(
            {
                "regime": "IBS",
                "from": "2027-01-01",
                "text": "Opção pelo Regime Regular",
            }
        )
        assert event.regime == SimplesEventRegime.IBS
        assert event.from_ == "2027-01-01"
        assert event.text == "Opção pelo Regime Regular"

    def test_simples_nacional_is_subclass_of_simples_simei(self) -> None:
        assert issubclass(SimplesNacionalDto, SimplesSimeiDto)

    def test_simples_nacional_dto_with_events(self) -> None:
        dto = SimplesNacionalDto.model_validate(
            {
                "optant": True,
                "since": "2020-01-01",
                "events": [
                    {
                        "regime": "CBS",
                        "from": "2027-01-01",
                        "text": "Evento Teste",
                    }
                ],
            }
        )
        assert dto.optant is True
        assert dto.since == "2020-01-01"
        assert dto.events is not None
        assert len(dto.events) == 1
        assert dto.events[0].regime == SimplesEventRegime.CBS
        assert dto.events[0].from_ == "2027-01-01"

    def test_simples_dto_accepts_simples_nacional_with_events(self) -> None:
        dto = SimplesDto.model_validate(
            {
                "taxId": "37335118000180",
                "updated": "2024-06-05T17:52:39.136Z",
                "simples": {
                    "optant": True,
                    "since": "2020-06-05",
                    "history": [],
                    "events": [],
                },
                "simei": {
                    "optant": False,
                    "since": None,
                    "history": [],
                },
            }
        )
        assert dto.simples.optant is True
        assert dto.simples.events == []

    def test_office_dto_with_banco_do_brasil_payload(self) -> None:
        """Regressão: payload real do Banco do Brasil que quebrou em produção."""
        payload = {
            "taxId": "00000000000191",
            "updated": "2024-01-01T00:00:00.000Z",
            "company": {
                "id": "00000000",
                "name": "BANCO DO BRASIL SA",
                "equity": 100000000.0,
                "nature": {"id": 2062, "text": "Sociedade Anônima Aberta"},
                "size": {"id": 5, "acronym": "DEMAIS", "text": "Demais"},
                "members": [],
                "simples": {
                    "optant": False,
                    "since": None,
                    "history": [],
                    "events": [],
                },
                "simei": {
                    "optant": False,
                    "since": None,
                    "history": [],
                },
            },
            "alias": "Banco do Brasil",
            "founded": "1808-10-12",
            "head": True,
            "statusDate": "2005-11-03",
            "status": {"id": 2, "text": "Ativa"},
            "address": {
                "municipality": 5300108,
                "street": "SBS Quadra 1 Bloco G",
                "number": "SN",
                "district": "Asa Sul",
                "city": "Brasília",
                "state": "DF",
                "zip": "70073901",
                "country": {"id": 76, "name": "Brasil"},
            },
            "phones": [],
            "emails": [],
            "mainActivity": {"id": 6422100, "text": "Bancos múltiplos, com carteira comercial"},
            "sideActivities": [],
        }

        office = OfficeDto.model_validate(payload)
        assert office.tax_id == "00000000000191"
        assert office.company.name == "BANCO DO BRASIL SA"
        assert office.company.simples is not None
        assert office.company.simples.optant is False
        assert office.company.simples.events == []
