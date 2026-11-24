#---------------------------------------------------------------------------
# Simulador de Rentabilidade (US03) - Gustavo Morais - 1242022304
#---------------------------------------------------------------------------

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class YieldSimulatorPage(BasePage):
    """Representa a aba do Simulador de Rentabilidade Mês a Mês (YieldSimulator.jsx)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Seção e formulário de projeção
        self.secao_simulador = page.locator("[data-testid='section-yield-simulator']")
        self.input_meses = page.locator("[data-testid='input-sim-months']")
        self.botao_calcular = page.locator("[data-testid='btn-calc-monthly']")
        self.alerta_erro = self.secao_simulador.locator(".error-message")

        # Tabela de evolução mês a mês
        self.tabela_evolucao_mensal = page.locator("[data-testid='table-monthly-projection']")
        self.linhas_evolucao_mensal = self.tabela_evolucao_mensal.locator("tbody tr")

        # Tabela consolidada por tipo de ativo
        self.tabela_resumo_tipo = page.locator("[data-testid='table-type-summary']")
        self.linhas_resumo_tipo = self.tabela_resumo_tipo.locator("tbody tr")

        # Cards consolidados no rodapé da simulação
        self.card_lucro_total = self.secao_simulador.locator(".summary-value")
        self.card_rendimento_total_pct = self.secao_simulador.locator(".summary-value-future")

    def definir_meses(self, meses: int | str):
        """Preenche o campo de quantidade de meses (1 a 60) para projeção."""
        self.input_meses.wait_for(state="visible")
        self.input_meses.fill(str(meses))

    def calcular_evolucao(self):
        """Submete o formulário para calcular a projeção de rentabilidade."""
        self.botao_calcular.click()

    def simular_projecao(self, meses: int | str):
        """Define a quantidade de meses e aciona o cálculo da evolução."""
        self.definir_meses(meses)
        self.calcular_evolucao()

    def obter_linha_mes(self, numero_mes: int) -> Locator:
        """Retorna a linha correspondente ao mês informado na tabela de evolução mensal."""
        return self.linhas_evolucao_mensal.filter(has_text=f"Mês {numero_mes}").first

    def total_meses_renderizados(self) -> int:
        """Retorna a quantidade de meses exibidos no grid de projeção."""
        return self.linhas_evolucao_mensal.count()

    def total_tipos_ativos_resumo(self) -> int:
        """Retorna a quantidade de tipos de ativos exibidos na tabela discriminada."""
        return self.linhas_resumo_tipo.count()
