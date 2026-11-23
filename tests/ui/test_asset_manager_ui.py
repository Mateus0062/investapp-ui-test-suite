"""Testes da aba Gerenciar Taxas (US05).

Responsavel: Integrante 2 - Júlia Suriani 12319522
"""
from playwright.sync_api import Page, expect
from pages.navbar_component import NavbarComponent
from pages.asset_manager_page import AssetManagerPage


def test_visualizar_e_persistir_taxa_anual(
    logged_page: Page,
    navbar: NavbarComponent,
):
    """Valida visualização da tabela de taxas, edição e persistência após salvar."""
    navbar.link_gerenciar_taxas.click()
    asset_manager = AssetManagerPage(logged_page)

    expect(asset_manager.tabela_taxas).to_be_visible(timeout=5000)

    ativo_alvo = "Poupança"
    nova_taxa = "7.5"
    linha = asset_manager.obter_linha_ativo(ativo_alvo)
    expect(linha).to_be_visible(timeout=5000)

    asset_manager.alterar_taxa_anual(ativo_alvo, nova_taxa)
    asset_manager.salvar_alteracoes()

    asset_manager.recarregar()
    navbar.link_gerenciar_taxas.click()

    linha_atualizada = asset_manager.obter_linha_ativo(ativo_alvo)
    expect(linha_atualizada).to_be_visible(timeout=5000)
    expect(linha_atualizada).to_contain_text(nova_taxa)