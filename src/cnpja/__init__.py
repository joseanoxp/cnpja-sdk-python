"""SDK Python para a API CNPJá.

Este SDK permite consultar dados de empresas brasileiras através da API CNPJá.
Inclui consultas de CNPJ, CPF, CEP, Receita Federal, Simples Nacional e mais.

Example:
    ```python
    from cnpja import Client

    client = Client(api_key="sua-api-key")

    # Consulta CNPJ
    office = client.office.read({"tax_id": "37335118000180"})
    print(f"Empresa: {office.company.name}")
    print(f"Status: {office.status.text}")

    # Pesquisa com filtros
    for office in client.office.search({"address.state.in": ["SP", "RJ"]}):
        print(f"{office.tax_id}: {office.company.name}")

    client.close()
    ```

API Pública (sem autenticação):
    ```python
    from cnpja import CnpjaOpen

    client = CnpjaOpen()
    zip_info = client.zip.read("01452922")
    print(f"Cidade: {zip_info.city}")
    client.close()
    ```
"""

from . import errors, types
from .client import AsyncClient, Client
from .errors import (
    APIError,
    BadRequestError,
    ClientError,
    CnpjaError,
    NotFoundError,
    ServerError,
    TooManyRequestsError,
    UnauthorizedError,
)
from .open_client import AsyncCnpjaOpen, CnpjaOpen
from .version import __version__

__all__ = [
    # Version
    "__version__",
    # Clients
    "Client",
    "AsyncClient",
    "CnpjaOpen",
    "AsyncCnpjaOpen",
    # Submodules
    "types",
    "errors",
    # Error classes
    "CnpjaError",
    "APIError",
    "ClientError",
    "ServerError",
    "BadRequestError",
    "UnauthorizedError",
    "NotFoundError",
    "TooManyRequestsError",
]
