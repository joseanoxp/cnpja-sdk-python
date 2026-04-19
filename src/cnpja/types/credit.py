"""DTOs do recurso Credit (Créditos)."""

from __future__ import annotations

from .._common import BaseModel


class CreditDto(BaseModel):
    """Informações de créditos."""

    transient: float
    """Créditos transitórios (expiram)."""
    perpetual: float
    """Créditos perpétuos (não expiram)."""

    @property
    def balance(self) -> float:
        """Saldo total de créditos disponível."""
        return self.transient + self.perpetual
