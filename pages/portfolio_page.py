"""Page Object da Carteira (Portfolio.jsx - US02).

Código fornecido no roteiro (seção 4). Criado pelo Líder porque o conftest.py
importa esta classe; os Integrantes 3 e 4 evoluem este arquivo.
"""
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class PortfolioPage(BasePage):
    """Representa a aba da Carteira de Investimentos (Portfolio.jsx)."""

    def __init__(self, page: Page):
        super().__init__(page)
        # Formulário de Cadastro
        self.select_ativo = page.locator("[data-testid='select-asset-name']")
        self.input_quantidade = page.locator("[data-testid='input-asset-amount']")
        self.input_preco_compra = page.locator("[data-testid='input-asset-price']")
        self.input_dias_investidos = page.locator("[data-testid='input-asset-days-invested']")
        self.input_dias_planejados = page.locator("[data-testid='input-asset-planned-days']")
        self.botao_adicionar = page.locator("[data-testid='btn-add-asset']")

        # Indicadores e Tabela
        self.card_patrimonio_total = page.locator("[data-testid='summary-current-val']")
        self.card_projecao_futura_total = page.locator("[data-testid='summary-future-val']")
        self.linhas_tabela_carteira = page.locator("[data-testid='table-portfolio'] tbody tr")
        self.linhas_ativos_carteira = page.locator("[data-testid^='portfolio-row-']")
        self.alerta_erro = page.locator("[data-testid='portfolio-error']")

    def cadastrar_aporte(self, ativo: str, quantidade: str, preco: str, dias_inv: str, dias_plan: str):
        """Preenche todos os campos do formulário e submete o novo aporte."""
        self.select_ativo.wait_for(state="visible")
        try:
            self.select_ativo.select_option(value=ativo)
        except Exception:
            self.select_ativo.select_option(label=f"{ativo}")
        self.input_quantidade.fill(quantidade)
        self.input_preco_compra.fill(preco)
        self.input_dias_investidos.fill(dias_inv)
        self.input_dias_planejados.fill(dias_plan)
        self.botao_adicionar.click()

    def obter_linha_por_ativo_e_prazo(self, nome_ativo: str, dias_inv: str, dias_plan: str) -> Locator:
        """
        Localiza especificamente a linha do ativo que corresponde aos dias cadastrados,
        evitando colisão com outros aportes do mesmo ativo.
        """
        texto_prazo = f"{dias_inv} / {dias_plan} dias"
        return self.linhas_tabela_carteira.filter(has_text=nome_ativo).filter(has_text=texto_prazo).first

    def obter_ultimo_ativo_cadastrado(self, nome_ativo: str) -> Locator:
        """Retorna a última linha inserida na tabela para o ativo informado."""
        return self.linhas_tabela_carteira.filter(has_text=nome_ativo).last

    def excluir_primeiro_ativo(self):
        """Clica no botão de exclusão da primeira linha da tabela."""
        botao_excluir = self.linhas_tabela_carteira.first.locator("[data-testid^='btn-delete-asset-']")
        botao_excluir.click()

    def excluir_ativo_da_linha(self, linha: Locator):
        """Clica no botão de exclusão de uma linha específica da tabela (tratando diálogo se houver)."""
        self.page.once("dialog", lambda dialog: dialog.accept())
        botao_excluir = linha.locator("[data-testid^='btn-delete-asset-']")
        botao_excluir.click()

    @staticmethod
    def converter_moeda_para_float(texto: str) -> float:
        """Converte string monetária brasileira (ex: 'R$ 2.500,00') em float."""
        limpo = texto.replace("R$", "").replace("\xa0", "").replace(".", "").replace(",", ".").strip()
        return float(limpo)

    def obter_valor_patrimonio_total(self) -> float:
        """Retorna o valor numérico exibido no card de Patrimônio Atual."""
        self.card_patrimonio_total.wait_for(state="visible")
        return self.converter_moeda_para_float(self.card_patrimonio_total.inner_text())

    def obter_valor_projecao_futura_total(self) -> float:
        """Retorna o valor numérico exibido no card de Projeção Futura Total."""
        self.card_projecao_futura_total.wait_for(state="visible")
        return self.converter_moeda_para_float(self.card_projecao_futura_total.inner_text())

    def calcular_soma_valor_atual_tabela(self) -> float:
        """Soma a coluna 'Valor Atual' (4ª coluna) de todas as linhas de ativos da tabela."""
        if self.total_de_ativos_listados() == 0:
            return 0.0
        total = 0.0
        for i in range(self.linhas_ativos_carteira.count()):
            texto_celula = self.linhas_ativos_carteira.nth(i).locator("td").nth(3).inner_text()
            total += self.converter_moeda_para_float(texto_celula)
        return round(total, 2)

    def total_de_ativos_listados(self) -> int:
        """Retorna o número atual de registros na tabela da carteira ignorando a mensagem de vazio."""
        self.page.wait_for_selector("[data-testid='table-portfolio'] tbody", timeout=5000)
        # Se a tabela ainda estiver no estado inicial vazio antes da resposta do GET /api/investments,
        # aguarda brevemente a chegada dos dados da API para evitar leitura prematura (0 itens).
        if self.linhas_ativos_carteira.count() == 0:
            try:
                self.linhas_ativos_carteira.first.wait_for(state="visible", timeout=5000)
            except Exception:
                pass
        # Se contiver a mensagem de tabela vazia (colSpan="7"), o total é 0
        if self.linhas_tabela_carteira.filter(has_text="Nenhum ativo cadastrado").count() > 0:
            return 0
        return self.linhas_tabela_carteira.count()
