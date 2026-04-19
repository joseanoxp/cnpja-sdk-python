"""Classes base para resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._http_client import HttpClient


class BaseResource:
    """Classe base para resources síncronos."""

    def __init__(self, http_client: HttpClient) -> None:
        """Inicializa o resource.

        Args:
            http_client: Cliente HTTP para requisições.
        """
        self._http = http_client


class AsyncBaseResource:
    """Classe base para resources assíncronos."""

    def __init__(self, http_client: HttpClient) -> None:
        """Inicializa o resource.

        Args:
            http_client: Cliente HTTP para requisições.
        """
        self._http = http_client
