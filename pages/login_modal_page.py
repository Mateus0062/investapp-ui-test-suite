from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginModalPage(BasePage):
    """Representa o modal flutuante de login (LoginModal.jsx)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.container_modal = page.locator("[data-testid='login-modal-content']")
        self.campo_usuario = page.locator("[data-testid='input-username']")
        self.campo_senha = page.locator("[data-testid='input-password']")
        self.botao_submeter = page.locator("[data-testid='btn-submit-login']")
        self.botao_fechar = page.locator(".btn-close-modal, button:has-text('Cancelar')").first
        self.mensagem_erro = page.locator("[data-testid='login-error']")
        # Adicionado pelo Líder: fundo escurecido atrás do modal
        self.fundo_modal = page.locator("[data-testid='login-modal-overlay']")

    def preencher_usuario(self, usuario: str):
        self.campo_usuario.wait_for(state="visible")
        self.campo_usuario.fill(usuario)

    def preencher_senha(self, senha: str):
        self.campo_senha.fill(senha)

    def submeter(self):
        self.botao_submeter.click()

    def fechar_modal(self):
        self.botao_fechar.click()

    def fechar_clicando_fora(self):
        """Clica no canto do fundo escurecido, fora da caixa do modal."""
        self.fundo_modal.click(position={"x": 5, "y": 5})

    def realizar_login(self, usuario: str, senha: str):
        """Fluxo de preenchimento completo e submissão."""
        self.preencher_usuario(usuario)
        self.preencher_senha(senha)
        self.submeter()
