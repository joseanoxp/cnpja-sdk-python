# CNPJá — SDK para Python

SDK para consultas em tempo real de CNPJs nos portais da Receita Federal, Simples Nacional, Cadastro de Contribuintes e SUFRAMA, fornecido pelo CNPJá.

Permite pesquisas de empresas e sócios utilizando múltiplos filtros, emissão de comprovantes em PDF, geração de mapas aéreos e geocodificação.

Baseado na especificação disponível em:
https://cnpja.com/api/reference

## Requisitos

- Python 3.12 ou superior
- (Opcional) Chave de API: disponível gratuitamente registrando-se no site [CNPJá](https://cnpja.com).

## Instalação

Este SDK é distribuído via Git. Adicione ao seu projeto com `uv`:

```bash
uv add git+https://github.com/joseanoxp/cnpja-sdk-python --tag v1.0.0
```

Ou acompanhando o branch principal:

```bash
uv add git+https://github.com/joseanoxp/cnpja-sdk-python
```

## GitHub Codespaces

Este repositório inclui um `.devcontainer/` para abrir diretamente em GitHub Codespaces com Python 3.12.

- o bootstrap instala `uv` e `task` se necessário;
- sincroniza dependências com `uv sync --locked`;
- instala os hooks do `pre-commit` na criação inicial do Codespace.

Depois de abrir o Codespace, o fluxo recomendado continua o mesmo:

```bash
task doctor
task qa
```

## Uso Básico

### Cliente Autenticado

```python
from cnpja import Client

client = Client(api_key="sua-api-key")

# Consulta CNPJ
office = client.office.read({"tax_id": "37335118000180"})
print(f"Empresa: {office.company.name}")
print(f"Status: {office.status.text}")
print(f"Endereço: {office.address.city}/{office.address.state}")

# Fecha o cliente
client.close()
```

### Context Manager

```python
with Client(api_key="sua-api-key") as client:
    office = client.office.read({"tax_id": "37335118000180"})
    print(f"Empresa: {office.company.name}")
```

### Pesquisa com Filtros

```python
# Pesquisa empresas ativas em SP
for office in client.office.search({
    "address.state.in": ["SP"],
    "status.id.in": [2],  # Ativas
}):
    print(f"{office.tax_id}: {office.company.name}")
```

### Cliente Assíncrono

```python
import asyncio
from cnpja import Client

async def main():
    client = Client(api_key="sua-api-key")

    async with client.aio as async_client:
        office = await async_client.office.read({"tax_id": "37335118000180"})
        print(f"Empresa: {office.company.name}")

    client.close()

asyncio.run(main())
```

### Pesquisa Assíncrona (Paginação)

O pager assíncrono é consumido com `async for`. Use `await pager.page()` (método,
não propriedade) para obter a página atual sem consumir a iteração.

```python
async def main():
    with Client(api_key="sua-api-key") as client:
        async with client.aio as aio:
            # Iteração transparente sobre todas as páginas
            async for office in aio.office.search({"address.state.in": ["SP"]}):
                print(f"{office.tax_id}: {office.company.name}")

            # Ou apenas a primeira página como lista
            pager = aio.office.search({"address.state.in": ["SP"]})
            first_page = await pager.page()
            print(f"{len(first_page)} registros na primeira página")

            # collect() aceita um limite opcional
            top_10 = await aio.office.search({"address.state.in": ["SP"]}).collect(limit=10)
```

### API Pública (Sem Autenticação)

```python
from cnpja import CnpjaOpen

client = CnpjaOpen()

# Consulta CEP
zip_info = client.zip.read("01452922")
print(f"Cidade: {zip_info.city}")
print(f"Estado: {zip_info.state}")

client.close()
```

## Recursos Disponíveis

| Recurso | Descrição |
|---------|-----------|
| `office` | Estabelecimentos (CNPJ) |
| `company` | Empresas |
| `person` | Pessoas/Sócios |
| `rfb` | Receita Federal |
| `simples` | Simples Nacional e MEI |
| `ccc` | Cadastro de Contribuintes (IE) |
| `suframa` | SUFRAMA |
| `zip` | CEP |
| `list` | Listas de CNPJs |
| `credit` | Créditos |

## Exemplos

### Consulta Receita Federal

```python
rfb = client.rfb.read({"tax_id": "37335118000180"})
print(f"Razão Social: {rfb.name}")
print(f"QSA: {len(rfb.members)} sócios")

for member in rfb.members:
    print(f"  - {member.person.name}: {member.role.text}")
```

### Emissão de Comprovante (PDF)

```python
# Comprovante RFB
pdf = client.rfb.certificate({"tax_id": "37335118000180"})
with open("comprovante_rfb.pdf", "wb") as f:
    f.write(pdf)

# Comprovante Simples Nacional
pdf = client.simples.certificate({"tax_id": "37335118000180"})
with open("comprovante_simples.pdf", "wb") as f:
    f.write(pdf)
```

### Mapa e Visão de Rua

```python
# Mapa aéreo do endereço
mapa = client.office.map({"tax_id": "37335118000180"})
with open("mapa.png", "wb") as f:
    f.write(mapa)

# Visão de rua
rua = client.office.street({"tax_id": "37335118000180"})
with open("rua.png", "wb") as f:
    f.write(rua)
```

### Listas de CNPJs

```python
# Criar lista
lista = client.list.create({
    "title": "Fornecedores",
    "items": ["37335118000180", "00000000000191"]
})

# Listar todas
for lista in client.list.search():
    print(f"{lista.title}: {lista.size} CNPJs")

# Exportar
export = client.list.create_export(
    lista.id,
    {"options": {"simples": True, "registrations": ["ORIGIN"]}},
)
```

## Tratamento de Erros

```python
from cnpja import Client, NotFoundError, TooManyRequestsError

client = Client(api_key="sua-api-key")

try:
    office = client.office.read({"tax_id": "00000000000000"})
except NotFoundError as e:
    print(f"CNPJ não encontrado: {e.message}")
except TooManyRequestsError as e:
    print(f"Créditos insuficientes. Necessário: {e.required}, Disponível: {e.remaining}")
```

## Tipos e Validação

O SDK usa Pydantic v2 para validação automática:

```python
from cnpja import types

# Usando modelos Pydantic
params = types.OfficeReadParams(
    tax_id="37335118000180",
    strategy=types.CacheStrategy.CACHE_IF_FRESH,
    simples=True,
)
office = client.office.read(params)

# Ou usando dicionários (também validados)
office = client.office.read({
    "tax_id": "37335118000180",
    "strategy": "CACHE_IF_FRESH",
    "simples": True,
})
```

## Configuração

```python
client = Client(
    api_key="sua-api-key",
    base_url="https://api.cnpja.com",  # URL base (padrão)
    timeout=30.0,                       # Timeout em segundos
    retry_limit=3,                      # Tentativas em caso de erro
    headers={"X-Custom": "value"},      # Headers adicionais
)
```

## Links

- [Documentação da API](https://cnpja.com/docs)
- [Repositório GitHub](https://github.com/joseanoxp/cnpja-sdk-python)

## Licença

MIT
