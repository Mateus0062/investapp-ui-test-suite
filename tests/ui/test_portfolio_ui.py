"""Testes da Carteira (US02): cadastro de aportes e exclusao/patrimonio.

Responsavel: Integrantes 3 (Júlia Suriani de Oliveira Silva) e 4.
"""

# Cadastrando um novo aporte e validando inserção na tabela da carteira via POM - Júlia Suriani
from playwright.sync_api import Page, expect
from pages.navbar_component import NavbarComponent
from pages.portfolio_page import PortfolioPage


def test_cadastrar_novo_aporte_carteira(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
):
    """Valida a criação de aporte e renderização exata na tabela da carteira."""
    navbar.navegar_para_carteira()

    dias_inv = "0"
    dias_plan = "365"

    portfolio_page.cadastrar_aporte(
        ativo="Poupança",
        quantidade="2500.00",
        preco="1.00",
        dias_inv=dias_inv,
        dias_plan=dias_plan,
    )

    linha_aporte = portfolio_page.obter_linha_por_ativo_e_prazo(
        "Poupança", dias_inv, dias_plan
    )
    expect(linha_aporte).to_be_visible(timeout=5000)
    expect(linha_aporte).to_contain_text("Poupança")


# ---------------------------------------------------------------------------
# Exclusão de ativos e recálculo de métricas consolidadas (US02) - Integrante 4
# ---------------------------------------------------------------------------

def test_remover_ativo_recalcula_patrimonio(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
):
    """Valida a exclusão do primeiro ativo e conferência da redução na tabela."""
    navbar.navegar_para_carteira()

    total_inicial = portfolio_page.total_de_ativos_listados()
    if total_inicial == 0:
        portfolio_page.cadastrar_aporte(
            ativo="Poupança",
            quantidade="1000.00",
            preco="1.00",
            dias_inv="0",
            dias_plan="365",
        )
        linha_criada = portfolio_page.obter_linha_por_ativo_e_prazo("Poupança", "0", "365")
        expect(linha_criada).to_be_visible(timeout=10000)
        total_inicial = portfolio_page.total_de_ativos_listados()

    if total_inicial > 0:
        portfolio_page.excluir_primeiro_ativo()
        if total_inicial > 1:
            # Aguarda a tabela re-renderizar para o novo total esperado
            expect(portfolio_page.linhas_tabela_carteira).to_have_count(
                total_inicial - 1, timeout=10000
            )
        else:
            expect(portfolio_page.linhas_tabela_carteira.first).to_contain_text(
                "Nenhum ativo cadastrado", timeout=10000
            )


def test_excluir_aporte_especifico_da_tabela(
    logged_page: Page,
    navbar: NavbarComponent,
    portfolio_page: PortfolioPage,
):
    """Valida o cadastro e a exclusão de um aporte específico na tabela com tratamento de alerta e métricas."""
    navbar.navegar_para_carteira()

    total_antes = portfolio_page.total_de_ativos_listados()
    soma_antes = portfolio_page.calcular_soma_valor_atual_tabela()

    dias_inv = "45"
    dias_plan = "180"
    portfolio_page.cadastrar_aporte(
        ativo="Poupança",
        quantidade="1000.00",
        preco="1.00",
        dias_inv=dias_inv,
        dias_plan=dias_plan,
    )

    expect(portfolio_page.linhas_ativos_carteira).to_have_count(
        total_antes + 1, timeout=10000
    )
    linha_aporte = portfolio_page.obter_linha_por_ativo_e_prazo(
        "Poupança", dias_inv, dias_plan
    )
    expect(linha_aporte).to_be_visible(timeout=10000)

    # Verifica que a soma dos ativos na tabela aumentou com o novo aporte
    soma_apos_cadastro = portfolio_page.calcular_soma_valor_atual_tabela()
    assert soma_apos_cadastro > soma_antes

    # Exclui o aporte recém-cadastrado e valida que a tabela e os cards permanecem consistentes
    portfolio_page.excluir_ativo_da_linha(linha_aporte)
    expect(portfolio_page.linhas_ativos_carteira).to_have_count(
        total_antes, timeout=10000
    )

    soma_apos_exclusao = portfolio_page.calcular_soma_valor_atual_tabela()
    assert soma_apos_exclusao == soma_antes
    expect(portfolio_page.card_patrimonio_total).to_be_visible()
    expect(portfolio_page.card_projecao_futura_total).to_be_visible()
    expect(portfolio_page.card_patrimonio_total).to_contain_text("R$")
    expect(portfolio_page.card_projecao_futura_total).to_contain_text("R$")
