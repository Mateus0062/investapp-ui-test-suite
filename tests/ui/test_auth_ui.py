"""Testes de autenticação e do LoginModal.jsx (US01) - Integrante 1 (Líder)."""
import os

from playwright.sync_api import Page, expect

from pages.login_modal_page import LoginModalPage
from pages.navbar_component import NavbarComponent

TEST_USER = os.getenv("TEST_USER", "userXX")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password")


def test_abertura_e_fechamento_modal_login(page: Page, base_url: str, navbar: NavbarComponent,
                                           login_modal: LoginModalPage):
    """Valida o ciclo de abertura e fechamento do LoginModal na UI."""
    page.goto(base_url)

    navbar.clicar_entrar()
    expect(login_modal.container_modal).to_be_visible()

    login_modal.fechar_modal()
    expect(login_modal.container_modal).not_to_be_visible()


def test_login_ui_com_sucesso(page: Page, base_url: str, navbar: NavbarComponent, login_modal: LoginModalPage):
    """Valida o fluxo completo de autenticação com credenciais corretas."""
    page.goto(base_url)

    navbar.clicar_entrar()
    login_modal.realizar_login(TEST_USER, TEST_PASSWORD)

    expect(navbar.botao_sair).to_be_visible(timeout=10000)
    expect(navbar.link_carteira).to_be_visible()


def test_login_ui_credenciais_invalidas(page: Page, base_url: str, navbar: NavbarComponent,
                                        login_modal: LoginModalPage):
    """Valida a exibição de aviso na UI ao fornecer senha incorreta."""
    page.goto(base_url)

    navbar.clicar_entrar()
    login_modal.realizar_login(TEST_USER, "senha_completamente_errada_xyz")

    expect(login_modal.mensagem_erro).to_be_visible(timeout=10000)
    expect(navbar.botao_sair).not_to_be_visible()


# ---------------------------------------------------------------------------
# Cenários adicionais do Líder (além dos fornecidos no roteiro)
# ---------------------------------------------------------------------------

def test_mensagem_de_erro_exibe_texto_da_api(page: Page, base_url: str, navbar: NavbarComponent,
                                             login_modal: LoginModalPage):
    """Valida que o aviso de erro mostra a mensagem devolvida pela API e que o modal continua aberto."""
    page.goto(base_url)

    navbar.clicar_entrar()
    login_modal.realizar_login(TEST_USER, "senha_completamente_errada_xyz")

    expect(login_modal.mensagem_erro).to_have_text("Usuário ou senha incorretos", timeout=10000)
    expect(login_modal.container_modal).to_be_visible()


def test_fechar_modal_clicando_fora(page: Page, base_url: str, navbar: NavbarComponent,
                                    login_modal: LoginModalPage):
    """Valida que clicar no fundo escurecido, fora da caixa, fecha o modal."""
    page.goto(base_url)

    navbar.clicar_entrar()
    expect(login_modal.container_modal).to_be_visible()

    login_modal.fechar_clicando_fora()
    expect(login_modal.container_modal).not_to_be_visible()


def test_logout_encerra_sessao(logged_page: Page, navbar: NavbarComponent):
    """Valida que, após o logout, o botão Entrar volta e o menu da Carteira some."""
    navbar.clicar_sair()

    expect(navbar.botao_entrar).to_be_visible()
    expect(navbar.link_carteira).not_to_be_visible()
