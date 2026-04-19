"""Versão do SDK CNPJá.

A versão é lida do metadata do pacote instalado (source of truth: pyproject.toml),
evitando drift entre a versão declarada no pyproject e esta constante.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cnpja")
except PackageNotFoundError:  # pragma: no cover — fallback para dev sem instalação
    __version__ = "0.0.0+unknown"
