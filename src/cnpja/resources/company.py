"""Resource para operações de empresas."""

from __future__ import annotations

from ..types.company import CompanyDto
from ._base import AsyncBaseResource, BaseResource


class CompanyResource(BaseResource):
    """Operações de empresas (síncrono)."""

    def read(self, company_id: int | str) -> CompanyDto:
        """Consulta informações de uma empresa.

        Args:
            company_id: Código da empresa (8 primeiros dígitos do CNPJ).

        Returns:
            Informações da empresa.

        Example:
            ```python
            company = client.company.read(37335118)
            print(f"Razão Social: {company.name}")
            ```
        """
        result = self._http.get(
            "/company/:companyId",
            replacements={"companyId": str(company_id)},
            response_model=CompanyDto,
        )
        return result


class AsyncCompanyResource(AsyncBaseResource):
    """Operações de empresas (assíncrono)."""

    async def read(self, company_id: int | str) -> CompanyDto:
        """Consulta informações de uma empresa.

        Args:
            company_id: Código da empresa (8 primeiros dígitos do CNPJ).

        Returns:
            Informações da empresa.
        """
        result = await self._http.aget(
            "/company/:companyId",
            replacements={"companyId": str(company_id)},
            response_model=CompanyDto,
        )
        return result
