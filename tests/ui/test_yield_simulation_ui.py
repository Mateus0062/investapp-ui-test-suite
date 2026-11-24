# ---------------------------------------------------------------------------
# Simulador de Rentabilidade (US03) - Gustavo Morais - 1242022304
# ---------------------------------------------------------------------------

from playwright.sync_api import Page, expect

from pages.navbar_component import NavbarComponent
from pages.portfolio_page import PortfolioPage
from pages.yield_simulator_page import YieldSimulatorPage


def _garantir_carteira_com_ativo(
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
):
    """Garante ao menos um ativo na carteira para viabilizar a simulação de rentabilidade."""
    navbar.navegar_para_carteira()
    if portfolio_page.total_de_ativos_listados() == 0:
        portfolio_page.cadastrar_aporte(
            ativo="Poupança",
            quantidade="2000.00",
            preco="1.00",
            dias_inv="0",
            dias_plan="365",
        )
        linha = portfolio_page.obter_linha_por_ativo_e_prazo("Poupança", "0", "365")
        expect(linha).to_be_visible(timeout=10000)


def test_simular_rentabilidade_12_meses_renderiza_grid_e_resumo_por_tipo(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
    yield_simulator_page: YieldSimulatorPage,
):
    """Valida a simulação padrão de 12 meses, o grid mês a mês e a tabela por tipo de ativo."""
    _garantir_carteira_com_ativo(navbar, portfolio_page)
    navbar.navegar_para_simulador()

    expect(yield_simulator_page.secao_simulador).to_be_visible(timeout=10000)
    expect(yield_simulator_page.input_meses).to_have_attribute("min", "1")
    expect(yield_simulator_page.input_meses).to_have_attribute("max", "60")

    yield_simulator_page.simular_projecao(12)

    expect(yield_simulator_page.tabela_evolucao_mensal).to_be_visible(timeout=10000)
    expect(yield_simulator_page.linhas_evolucao_mensal).to_have_count(12, timeout=10000)
    expect(yield_simulator_page.obter_linha_mes(1)).to_be_visible()
    expect(yield_simulator_page.obter_linha_mes(12)).to_be_visible()
    expect(yield_simulator_page.obter_linha_mes(12)).to_contain_text("R$")

    expect(yield_simulator_page.tabela_resumo_tipo).to_be_visible(timeout=10000)
    assert yield_simulator_page.total_tipos_ativos_resumo() >= 1
    expect(yield_simulator_page.linhas_resumo_tipo.first).to_contain_text("R$")
    expect(yield_simulator_page.linhas_resumo_tipo.first).to_contain_text("%")

    expect(yield_simulator_page.card_lucro_total).to_be_visible()
    expect(yield_simulator_page.card_lucro_total).to_contain_text("R$")
    expect(yield_simulator_page.card_rendimento_total_pct).to_be_visible()
    expect(yield_simulator_page.card_rendimento_total_pct).to_contain_text("%")


def test_alterar_periodo_projecao_atualiza_quantidade_de_meses_no_grid(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
    yield_simulator_page: YieldSimulatorPage,
):
    """Valida o ajuste do input de projeção dentro da faixa de 1 a 60 meses e atualização do grid."""
    _garantir_carteira_com_ativo(navbar, portfolio_page)
    navbar.navegar_para_simulador()

    # Simula o limite mínimo (1 mês)
    yield_simulator_page.simular_projecao(1)
    expect(yield_simulator_page.linhas_evolucao_mensal).to_have_count(1, timeout=10000)
    expect(yield_simulator_page.obter_linha_mes(1)).to_be_visible()

    # Ajusta para o limite máximo (60 meses)
    yield_simulator_page.simular_projecao(60)
    expect(yield_simulator_page.linhas_evolucao_mensal).to_have_count(60, timeout=10000)
    expect(yield_simulator_page.obter_linha_mes(60)).to_be_visible()
    expect(yield_simulator_page.tabela_resumo_tipo).to_be_visible(timeout=10000)
    assert yield_simulator_page.total_tipos_ativos_resumo() >= 1
