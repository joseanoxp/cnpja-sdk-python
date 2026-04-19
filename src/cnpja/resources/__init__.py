"""Resources (serviços) do SDK CNPJá."""

from .ccc import AsyncCccResource, CccResource
from .company import AsyncCompanyResource, CompanyResource
from .credit import AsyncCreditResource, CreditResource
from .list import AsyncListResource, ListResource
from .office import AsyncOfficeResource, OfficeResource
from .open_office import AsyncOpenOfficeResource, OpenOfficeResource
from .person import AsyncPersonResource, PersonResource
from .rfb import AsyncRfbResource, RfbResource
from .simples import AsyncSimplesResource, SimplesResource
from .suframa import AsyncSuframaResource, SuframaResource
from .zip import AsyncZipResource, ZipResource

__all__ = [
    # Sync
    "CccResource",
    "CompanyResource",
    "CreditResource",
    "ListResource",
    "OpenOfficeResource",
    "OfficeResource",
    "PersonResource",
    "RfbResource",
    "SimplesResource",
    "SuframaResource",
    "ZipResource",
    # Async
    "AsyncCccResource",
    "AsyncCompanyResource",
    "AsyncCreditResource",
    "AsyncListResource",
    "AsyncOpenOfficeResource",
    "AsyncOfficeResource",
    "AsyncPersonResource",
    "AsyncRfbResource",
    "AsyncSimplesResource",
    "AsyncSuframaResource",
    "AsyncZipResource",
]
