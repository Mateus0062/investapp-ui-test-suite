# investapp-ui-test-suite

Testes E2E de interface do **InvestApp** com Pytest + Playwright, usando Page Object Model (POM).

- Aplicação: http://investapp-frontend.s3-website-us-east-1.amazonaws.com/
- Swagger da API (apoio): https://5bm1nctd1f.execute-api.us-east-1.amazonaws.com/docs

## Setup no Codespaces (cada integrante)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
playwright install-deps

cp .env.example .env   # depois edite TEST_USER e TEST_PASSWORD
```

O `.env` e o `.vscode/launch.json` não vão para o GitHub (têm credenciais). Peça ao Líder.

## Execução

```bash
python -m pytest tests/ui -v -s                                          # headless
python -m pytest tests/ui -v -s --video=on --screenshot=on              # vídeos/prints em test-results/
python -m pytest tests/ui --html=playwright-report.html --self-contained-html   # relatório HTML com prints
```

No Codespaces não existe tela: `--headed` e o F5 só abrem o navegador com o Xvfb + noVNC da Opção 4 do roteiro.

## Regra do POM (critério de avaliação)

Os arquivos `tests/ui/test_*.py` **não podem** ter `page.locator(...)`. Todo seletor fica numa classe em `pages/`,
e o teste só chama métodos e faz `expect(...)`.

## Fixtures (`tests/ui/conftest.py`)

| Fixture          | O que entrega                                  |
|------------------|------------------------------------------------|
| `base_url`       | URL da aplicação (do `.env`)                   |
| `navbar`         | `NavbarComponent`                              |
| `login_modal`    | `LoginModalPage`                               |
| `portfolio_page` | `PortfolioPage`                                |
| `logged_page`    | Navegador já logado com o usuário do `.env`    |

Quem criar um Page Object novo deve adicionar a fixture correspondente no `conftest.py`.

## Divisão de tarefas

| Integrante | Page Object(s)                                       | Teste(s)                          |
|------------|------------------------------------------------------|-----------------------------------|
| 1 (Líder)  | `base_page.py`, `navbar_component.py`, `login_modal_page.py` | configs, `conftest.py`, `test_auth_ui.py` |
| 2          | `asset_manager_page.py`                              | `test_asset_manager_ui.py`        |
| 3          | `portfolio_page.py` (cadastro)                       | `test_portfolio_ui.py` (cadastro) |
| 4          | `portfolio_page.py` (exclusão/patrimônio)            | `test_portfolio_ui.py` (exclusão) |
| 5          | `yield_simulator_page.py`                            | `test_yield_simulation_ui.py`     |
| 6          | `tax_optimizer_page.py`                              | `test_tax_optimizer_ui.py`        |
| 7          | (usa `portfolio_page.py`)                            | `test_portfolio_ddt_ui.py` + CSV  |
| 8          | (a definir)                                          | `test_exceptions_and_a11y_ui.py`  |

## Avisos sobre o código do roteiro (conferidos na aplicação real)

- **Integrante 7:** o teste DDT do roteiro chama `portfolio_page.obter_linha_por_ativo(...)`, que **não existe**
  na `PortfolioPage`. Usar `obter_linha_por_ativo_e_prazo(...)` ou `obter_ultimo_ativo_cadastrado(...)`.
- **Integrante 7:** no CSV do roteiro está `Ações Petrobras` (sem acento), mas na aplicação o ativo é
  `Ações Petrobrás` (com acento). Sem corrigir, o select não encontra a opção e o teste falha.
- Os `data-testid` disponíveis na aplicação incluem: `table-asset-rates`, `section-asset-manager`,
  `input-sim-months`, `btn-calc-monthly`, `table-monthly-projection`, `table-type-summary`,
  `input-withdraw-amount`, `btn-calc-withdrawal`, `table-tax-optimization`, `summary-future-val`.
- A API (AWS Lambda) demora alguns segundos na primeira chamada. Prefiram `timeout=10000` nos `expect`
  que dependem de resposta da API.

Cada integrante deve fazer **os próprios commits**: o professor verifica o histórico.
