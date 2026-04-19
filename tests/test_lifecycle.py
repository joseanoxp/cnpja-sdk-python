"""Testes de ciclo de vida: close, aclose, context managers."""

from __future__ import annotations

import pytest

from cnpja import Client, CnpjaOpen


class TestSyncLifecycle:
    def test_close_resets_sync_client(self, api_key: str) -> None:
        c = Client(api_key=api_key)
        _ = c._http.sync_client
        assert c._http._sync_client is not None
        c.close()
        assert c._http._sync_client is None

    def test_context_manager_closes(self, api_key: str) -> None:
        with Client(api_key=api_key) as c:
            _ = c._http.sync_client
            assert c._http._sync_client is not None
        assert c._http._sync_client is None

    def test_open_client_close(self) -> None:
        c = CnpjaOpen()
        _ = c._http.sync_client
        c.close()
        assert c._http._sync_client is None

    def test_open_client_context_manager(self) -> None:
        with CnpjaOpen() as c:
            _ = c._http.sync_client
        assert c._http._sync_client is None


@pytest.mark.asyncio
class TestAsyncLifecycle:
    async def test_aclose_resets_async_client(self, api_key: str) -> None:
        c = Client(api_key=api_key)
        _ = c._http.async_client
        assert c._http._async_client is not None
        await c.aio.aclose()
        assert c._http._async_client is None
        c.close()

    async def test_async_context_manager_closes(self, api_key: str) -> None:
        c = Client(api_key=api_key)
        async with c.aio as aio:
            _ = aio._http.async_client
            assert aio._http._async_client is not None
        assert c._http._async_client is None
        c.close()

    async def test_open_async_context_manager(self) -> None:
        c = CnpjaOpen()
        async with c.aio as aio:
            _ = aio._http.async_client
        assert c._http._async_client is None
        c.close()


class TestResourceCaching:
    """Garante que cached_property devolve a mesma instância em acessos repetidos."""

    def test_client_resources_cached(self, api_key: str) -> None:
        with Client(api_key=api_key) as c:
            assert c.office is c.office
            assert c.company is c.company
            assert c.list is c.list

    def test_aio_shares_transport(self, api_key: str) -> None:
        with Client(api_key=api_key) as c:
            assert c.aio._http is c._http

    def test_open_aio_shares_transport(self) -> None:
        with CnpjaOpen() as c:
            assert c.aio._http is c._http
