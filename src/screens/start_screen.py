"""start_screen.py — Tela Inicial"""

import pyray as rl
import math
import random

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, GameState


# ── Partícula de Estrela ───────────────────────────────────────────────────────

class _Particula:
    """Estrela/partícula animada de fundo."""

    def __init__(self):
        self._renascer()
        # Começa espalhada pela tela
        self.y = random.uniform(0, SCREEN_HEIGHT)

    def _renascer(self):
        self.x      = random.uniform(0, SCREEN_WIDTH)
        self.y      = SCREEN_HEIGHT + 5.0
        self.speed  = random.uniform(15.0, 60.0)
        self.radius = random.uniform(1.0, 3.0)
        self.phase  = random.uniform(0, math.pi * 2)

    def update(self, dt: float):
        self.y -= self.speed * dt
        if self.y < -5:
            self._renascer()

    def draw(self, tempo: float):
        brilho = 0.4 + 0.6 * abs(math.sin(tempo * 1.5 + self.phase))
        alpha  = int(brilho * 220)
        amarelo = int(200 + 55 * brilho)
        rl.draw_circle(int(self.x), int(self.y), self.radius,
                       rl.Color(255, amarelo, 100, alpha))


# ── Botão Interativo ───────────────────────────────────────────────────────────

class _Botao:
    """Botão com efeito de hover suave."""

    def __init__(self, x: int, y: int, w: int, h: int,
                 texto: str, cor: rl.Color, cor_hover: rl.Color):
        self.rect      = rl.Rectangle(x, y, w, h)
        self.texto     = texto
        self.cor       = cor
        self.cor_hover = cor_hover
        self.hovered   = False
        self.escala    = 1.0

    def update(self, dt: float) -> bool:
        """Retorna True se o botão foi clicado."""
        self.hovered = rl.check_collision_point_rec(
            rl.get_mouse_position(), self.rect)
        alvo = 1.06 if self.hovered else 1.0
        self.escala += (alvo - self.escala) * dt * 12
        return self.hovered and rl.is_mouse_button_pressed(
            rl.MouseButton.MOUSE_BUTTON_LEFT)

    def draw(self):
        e = self.escala
        w = self.rect.width  * e
        h = self.rect.height * e
        x = self.rect.x - (w - self.rect.width)  / 2
        y = self.rect.y - (h - self.rect.height) / 2
        r = rl.Rectangle(x, y, w, h)

        # Sombra
        rl.draw_rectangle_rounded(
            rl.Rectangle(x + 4, y + 4, w, h), 0.35, 8,
            rl.Color(0, 0, 0, 90))

        # Corpo
        cor = self.cor_hover if self.hovered else self.cor
        rl.draw_rectangle_rounded(r, 0.35, 8, cor)

        # Borda
        borda_a = 200 if self.hovered else 80
        rl.draw_rectangle_rounded_lines(
            r, 0.35, 8, rl.Color(255, 255, 255, borda_a))

        # Texto centralizado
        fs = 26
        tw = rl.measure_text(self.texto, fs)
        tx = int(x + w / 2 - tw / 2)
        ty = int(y + h / 2 - fs / 2)
        rl.draw_text(self.texto, tx + 1, ty + 2, fs, rl.Color(0, 0, 0, 100))
        rl.draw_text(self.texto, tx, ty, fs, rl.WHITE)


# ── Tela Inicial ──────────────────────────────────────────────────────────────

class StartScreen:
    """
    Tela de entrada do Super Racer 3D.
    Exibe partículas animadas, título, cenário com personagem e botões de JOGAR / SAIR.
    """

    NUM_PARTICULAS = 180

    def __init__(self):
        self.tempo      = 0.0
        self.particulas = [_Particula() for _ in range(self.NUM_PARTICULAS)]

        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2
        bw, bh = 260, 58

        self.btn_jogar = _Botao(cx - bw // 2, cy + 50,  bw, bh, "JOGAR",
                                rl.Color(34, 170, 100, 255),
                                rl.Color(55, 210, 130, 255))
        self.btn_sair  = _Botao(cx - bw // 2, cy + 130, bw, bh, "SAIR",
                                rl.Color(180, 50,  50,  255),
                                rl.Color(220, 75,  75,  255))

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        """Atualiza animações e captura interação. Retorna próximo GameState."""
        self.tempo += dt
        for p in self.particulas:
            p.update(dt)

        if self.btn_jogar.update(dt):
            return GameState.PLAYING

        if self.btn_sair.update(dt):
            return GameState.EXIT

        return None

    # ── Helpers de Desenho ────────────────────────────────────────────────────

    def _draw_fundo(self):
        """Gradiente escuro simulado com linhas horizontais."""
        for i in range(0, SCREEN_HEIGHT, 2):
            t = i / SCREEN_HEIGHT
            r = int(4  + t * 12)
            g = int(4  + t * 4)
            b = int(28 + t * 32)
            rl.draw_line(0, i, SCREEN_WIDTH, i, rl.Color(r, g, b, 255))

    def _draw_cenario(self):
        """Cenário de plataforma com personagem e estrela."""
        sw, sh = SCREEN_WIDTH, SCREEN_HEIGHT
        y_chao = int(sh * 0.82)

        # Chão com colinas
        terra        = rl.Color(50, 30, 15,  255)
        verde_escuro = rl.Color(20, 90, 30,  255)
        verde_claro  = rl.Color(50, 180, 60, 255)
        rl.draw_rectangle(0, y_chao + 6, sw, sh - y_chao, terra)
        for i in range(sw):
            h = int(10 * math.sin(i * 0.014) + 7 * math.sin(i * 0.031 + 1.2))
            rl.draw_line(i, y_chao - h, i, y_chao + 6, verde_escuro)
            rl.draw_line(i, y_chao - h - 3, i, y_chao - h + 1, verde_claro)

        # Personagem (bonequinho)
        cx     = int(sw * 0.18)
        cy     = y_chao  # pés no chão
        alt    = 72
        pulso  = math.sin(self.tempo * 2.2)
        cor_pele  = rl.Color(220, 195, 160, 255)
        cor_roupa = rl.Color(70, 110, 230, 255)
        esp = 3

        quadril  = rl.Vector2(cx,      cy - int(alt * 0.33))
        ombros   = rl.Vector2(cx,      cy - int(alt * 0.68))
        cabeca_c = (cx, cy - int(alt * 0.88))

        # Pernas
        rl.draw_line_ex(quadril, rl.Vector2(cx - 13, cy), esp, cor_roupa)
        rl.draw_line_ex(quadril, rl.Vector2(cx + 13, cy), esp, cor_roupa)
        # Corpo
        rl.draw_line_ex(quadril, ombros, esp + 1, cor_roupa)
        # Braço esquerdo (relaxado)
        rl.draw_line_ex(ombros, rl.Vector2(cx - 22, cy - int(alt * 0.48)), esp, cor_roupa)
        # Braço direito (levantado alcançando a estrela)
        bx = cx + 32 + int(5 * pulso)
        by = cy - int(alt * 0.92) + int(4 * pulso)
        rl.draw_line_ex(ombros, rl.Vector2(bx, by), esp, cor_roupa)
        # Cabeça
        rl.draw_circle(*cabeca_c, 14, cor_pele)
        rl.draw_circle(cabeca_c[0] + 4,  cabeca_c[1] - 3, 2, rl.Color(30, 30, 30, 255))
        rl.draw_circle(cabeca_c[0] + 9,  cabeca_c[1] - 3, 2, rl.Color(30, 30, 30, 255))
        rl.draw_circle(cabeca_c[0] + 6,  cabeca_c[1] + 4, 2, rl.Color(30, 30, 30, 180))

        # Estrela flutuando acima do braço
        ex = bx + 22
        ey = by - 22 + int(6 * math.sin(self.tempo * 2.5))
        er = int(13 + 3 * abs(math.sin(self.tempo * 1.8)))
        ea = int(200 + 55 * abs(math.sin(self.tempo * 2.0)))
        rl.draw_circle(ex, ey, er,        rl.Color(255, 225, 30, ea))
        rl.draw_circle(ex, ey, er // 2,   rl.Color(255, 255, 200, 255))
        for i in range(6):
            ang = self.tempo * 1.8 + i * (math.pi * 2 / 6)
            rl.draw_circle(int(ex + math.cos(ang) * (er + 9)),
                           int(ey + math.sin(ang) * (er + 9)),
                           3, rl.Color(255, 210, 40, 160))

    def _draw_estrelas_orbitando(self):
        """Estrelinhas decorativas girando ao redor do título."""
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 3
        for i in range(7):
            ang    = self.tempo * 0.6 + (i / 7) * math.pi * 2
            r_orb  = 220 + math.sin(self.tempo + i) * 15
            ox     = cx + math.cos(ang) * r_orb
            oy     = cy + math.sin(ang) * 55
            s      = 3.5 + math.sin(self.tempo * 2 + i) * 1.5
            a      = int(180 + 75 * abs(math.sin(self.tempo + i)))
            rl.draw_circle(int(ox), int(oy), s,       rl.Color(255, 230, 50, a))
            rl.draw_circle(int(ox), int(oy), s * 0.4, rl.Color(255, 255, 200, 255))

    def _draw_titulo(self):
        """Título com glow pulsante e sombra."""
        titulo   = SCREEN_TITLE.upper()
        fs       = 82
        pulso    = 0.65 + 0.35 * abs(math.sin(self.tempo * 1.4))
        tw       = rl.measure_text(titulo, fs)
        tx       = SCREEN_WIDTH  // 2 - tw // 2
        ty       = SCREEN_HEIGHT // 3 - fs // 2

        # Camadas de glow
        for raio, base_a in [(7, 18), (4, 45), (2, 90)]:
            ga = int(base_a * pulso)
            gc = rl.Color(80, 190, 255, ga)
            for dx in range(-raio, raio + 1, raio):
                for dy in range(-raio, raio + 1, raio):
                    if dx or dy:
                        rl.draw_text(titulo, tx + dx, ty + dy, fs, gc)

        # Sombra
        rl.draw_text(titulo, tx + 5, ty + 5, fs, rl.Color(0, 0, 0, 110))

        # Texto principal com cor dinâmica
        r_c = int(90  + 165 * pulso)
        g_c = int(170 + 85  * pulso)
        rl.draw_text(titulo, tx, ty, fs, rl.Color(r_c, g_c, 255, 255))

        # Subtítulo
        sub   = "Colete todas as estrelas antes do tempo acabar!"
        sf    = 21
        sw_   = rl.measure_text(sub, sf)
        sub_a = int(160 + 95 * abs(math.sin(self.tempo * 0.9)))
        rl.draw_text(sub,
                     SCREEN_WIDTH // 2 - sw_ // 2,
                     ty + fs + 14,
                     sf, rl.Color(200, 220, 255, sub_a))

    def _draw_dica_controles(self):
        """Dica de controles piscando no rodapé."""
        dica  = "[WASD] ou [SETAS] para mover    [ESC] para pausar"
        df    = 17
        dw    = rl.measure_text(dica, df)
        da    = int(100 + 80 * abs(math.sin(self.tempo * 0.6)))
        rl.draw_text(dica,
                     SCREEN_WIDTH // 2 - dw // 2,
                     SCREEN_HEIGHT - 36,
                     df, rl.Color(170, 180, 210, da))

    # ── Draw Principal ────────────────────────────────────────────────────────

    def draw(self):
        """Renderiza a tela inicial completa."""
        rl.clear_background(rl.Color(4, 4, 28, 255))

        self._draw_fundo()

        for p in self.particulas:
            p.draw(self.tempo)

        self._draw_cenario()
        self._draw_estrelas_orbitando()
        self._draw_titulo()

        self.btn_jogar.draw()
        self.btn_sair.draw()

        self._draw_dica_controles()
