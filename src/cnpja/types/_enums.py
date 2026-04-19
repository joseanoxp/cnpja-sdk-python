"""Enumerações do SDK CNPJá."""

from enum import Enum


class State(str, Enum):
    """Siglas das Unidades Federativas do Brasil."""

    AC = "AC"
    AL = "AL"
    AM = "AM"
    AP = "AP"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MG = "MG"
    MS = "MS"
    MT = "MT"
    PA = "PA"
    PB = "PB"
    PE = "PE"
    PI = "PI"
    PR = "PR"
    RJ = "RJ"
    RN = "RN"
    RO = "RO"
    RR = "RR"
    RS = "RS"
    SC = "SC"
    SE = "SE"
    SP = "SP"
    TO = "TO"


class PhoneType(str, Enum):
    """Tipo de telefone."""

    LANDLINE = "LANDLINE"
    MOBILE = "MOBILE"


class EmailOwnership(str, Enum):
    """Tipo de propriedade do e-mail."""

    PERSONAL = "PERSONAL"
    CORPORATE = "CORPORATE"
    ACCOUNTING = "ACCOUNTING"


class PersonType(str, Enum):
    """Tipo de pessoa."""

    NATURAL = "NATURAL"
    LEGAL = "LEGAL"
    FOREIGN = "FOREIGN"
    UNKNOWN = "UNKNOWN"


class AgeRange(str, Enum):
    """Faixa etária."""

    RANGE_0_12 = "0-12"
    RANGE_13_20 = "13-20"
    RANGE_21_30 = "21-30"
    RANGE_31_40 = "31-40"
    RANGE_41_50 = "41-50"
    RANGE_51_60 = "51-60"
    RANGE_61_70 = "61-70"
    RANGE_71_80 = "71-80"
    RANGE_81_PLUS = "81+"


class OfficeStatusId(int, Enum):
    """Código da situação cadastral do estabelecimento."""

    NULA = 1
    ATIVA = 2
    SUSPENSA = 3
    INAPTA = 4
    BAIXADA = 8


class CompanySizeId(int, Enum):
    """Código do porte da empresa."""

    ME = 1  # Microempresa
    EPP = 3  # Empresa de Pequeno Porte
    DEMAIS = 5  # Demais


class SuframaStatusId(int, Enum):
    """Código da situação cadastral SUFRAMA."""

    ATIVA = 1
    INATIVA = 2
    BLOQUEADA = 3
    CANCELADA = 4
    CANCELADA_AG_REC = 5


class SuframaTribute(str, Enum):
    """Tributo incentivado SUFRAMA."""

    ICMS = "ICMS"
    IPI = "IPI"


class RegistrationStatusId(int, Enum):
    """Código da situação cadastral da Inscrição Estadual."""

    SEM_RESTRICAO = 1
    BLOQUEADO_DESTINATARIO = 2
    VEDADA_OPERACAO = 3
    EMITENTE_BLOQUEADO = 10


class RegistrationTypeId(int, Enum):
    """Código do tipo de Inscrição Estadual."""

    IE_NORMAL = 1
    IE_SUBSTITUTO = 2
    IE_NAO_CONTRIBUINTE = 3
    IE_OUTRA_UF = 4
    IE_PRODUTOR_RURAL = 5
    IE_NAO_INFORMADA = 9


class OfficeLinkType(str, Enum):
    """Tipo de link de arquivo."""

    RFB_CERTIFICATE = "RFB_CERTIFICATE"
    SIMPLES_CERTIFICATE = "SIMPLES_CERTIFICATE"
    CCC_CERTIFICATE = "CCC_CERTIFICATE"
    SUFRAMA_CERTIFICATE = "SUFRAMA_CERTIFICATE"
    OFFICE_MAP = "OFFICE_MAP"
    OFFICE_STREET = "OFFICE_STREET"


class CacheStrategy(str, Enum):
    """Estratégia de cache para consultas."""

    ONLINE = "ONLINE"
    CACHE_IF_FRESH = "CACHE_IF_FRESH"
    CACHE_IF_ERROR = "CACHE_IF_ERROR"
    CACHE = "CACHE"
