"""Page Object da aba Gerenciar Taxas (AssetManager.jsx - US05).

Responsavel: Integrante 2 - Júlia Suriani 12319522
"""
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class AssetManagerPage(BasePage):
    """Representa a aba de Gerenciamento de Taxas (AssetManager.jsx)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.tabela_taxas = page.locator("table").first
        self.linhas_taxas = self.tabela_taxas.locator("tbody tr")
        self.botao_salvar = page.locator(
            "[data-testid='btn-save-rates'], button:has-text('Salvar')"
        ).first

    def obter_linha_ativo(self, nome_ativo: str) -> Locator:
        """Retorna a linha correspondente ao ativo na tabela de taxas."""
        return self.linhas_taxas.filter(has_text=nome_ativo).first

    def alterar_taxa_anual(self, nome_ativo: str, nova_taxa: str):
        """Altera o percentual anual na linha do ativo informado."""
        linha = self.obter_linha_ativo(nome_ativo)
        linha.wait_for(state="visible")
        campo_taxa = linha.locator("input").first
        campo_taxa.fill(str(nova_taxa))

    def salvar_alteracoes(self):
        """Clica no botão de salvar taxas."""
        self.botao_salvar.click()