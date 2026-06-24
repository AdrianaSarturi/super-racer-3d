"""game_screen.py — Tela de Jogo"""

import math
import pyray as rl

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GameState,
    ARENA_SIZE, VELOCIDADE_JOGADOR, TEMPO_LIMITE, QUANTIDADE_ESTRELAS,
)
from src.world.palette import HUD_TEXTO, HUD_ALERTA
from src.world.scenario import Scenario
from src.world.star import Star
from src.entities.player import Player
from src.screens.end_screen import EndScreen

# ── Posições das estrelas ─────────────────────────────────────────────────────
# 10 posições verificadas manualmente para não colidirem com nenhum obstáculo.
# Cada posição mantém pelo menos ~1.5 unidades de distância do centro dos obstáculos.
_POSICOES_ESTRELAS: list[tuple[float, float]] = [
    (-8.5, -8.5),   # canto SO — livre
    ( 8.5, -8.5),   # canto SE — livre
    (-8.5,  8.5),   # canto NO — livre
    ( 8.5,  8.5),   # canto NE — livre (2.1u do cubo 7,7)
    ( 0.0, -5.0),   # centro-S — livre (longe do spawn do jogador em 0,0)
    (-4.0, -0.5),   # interior — livre (2.5u dos obstáculos)
    ( 3.0, -7.5),   # sul      — livre (2.5u do cubo 5,-6)
    (-7.0,  7.0),   # noroeste — livre (4.1u do cubo -8,3)
    ( 5.5, -2.5),   # leste    — livre (1.6u do cone 4,-3 → gap > STAR_COLLECT_RADIUS)
    (-1.0,  2.5),   # centro-N — livre (2.1u do cano -3,3)
    # ── 5 Novas Posições Adicionadas para somar 15 ──
    (-3.0, -3.0),   # Quadrante Sudoeste interno
    ( 3.0,  3.0),   # Quadrante Nordeste interno
    (-2.0,  7.5),   # Norte central livre
    ( 7.5,  2.0),   # Leste central livre
    ( 0.0, -2.0),   # Centro-Sul livre
]
 

class GameScreen:
    """
    Tela principal do jogo.

    Responsabilidades:
        - Câmera orbital com mouse (mantida intacta).
        - Movimento do jogador (WASD / setas).
        - Renderização do cenário (Scenario) e estrelas (Star).
        - HUD: contador de estrelas + timer regressivo + barra de progresso.
        - Pausa (ESC): congela o jogo e exibe overlay com opções.
        - Condição de fim: todas as estrelas coletadas OU tempo esgotado com reset.
    """

    def __init__(self):
        self.tempo        = 0.0
        self.pausado      = False

        # ── Câmera (mantida intacta conforme código original) ─────────────
        self.camera = rl.Camera3D()
        self.camera.up         = rl.Vector3(0.0, 1.0, 0.0)
        self.camera.fovy       = 60.0
        self.camera.projection = rl.CAMERA_PERSPECTIVE

        self.angulo_horizontal = 0.0
        self.angulo_vertical   = 0.3
        self.distancia         = 6.0
        self.distancia_min     = 4.0
        self.distancia_max     = 10.0

        # ── Cenário e estrelas ────────────────────────────────────────────
        self.cenario = Scenario()
        # Flag de controlo para reinicialização interna do estado
        self.needs_reset = True

    def reset(self):
        """Reinicia o estado interno do jogo sempre que uma nova partida começa."""
        self.player = Player()
        self.timer        = float(TEMPO_LIMITE)
        self.estrelas_coletadas = 0
        self.pausado      = False
        self.estrelas: list[Star] = [
            Star(x, z, fase=i * 0.47)
            for i, (x, z) in enumerate(_POSICOES_ESTRELAS[:QUANTIDADE_ESTRELAS])
        ]
        self.camera.target = self.player.posicao
        self.needs_reset = False

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
        if self.needs_reset:
            self.reset()

        # ── Alternar pausa com ESC ou P ───────────────────────────────────
        if rl.is_key_pressed(rl.KEY_ESCAPE) or rl.is_key_pressed(rl.KEY_P):
            self.pausado = not self.pausado

        # ── Quando pausado: só trata saída via Enter ──────────────────────
        if self.pausado:
            if rl.is_key_pressed(rl.KEY_ENTER):
                EndScreen.score = self.estrelas_coletadas
                EndScreen.victory = self.estrelas_coletadas >= QUANTIDADE_ESTRELAS
                self.needs_reset = True
                return GameState.GAME_OVER
            return None

        # ── Lógica de jogo (congelada durante pausa) ──────────────────────
        self.tempo += dt
        self.timer -= dt

        # ── Câmera orbital com mouse (código original intacto) ────────────
        mouse_delta = rl.get_mouse_delta()
        self.angulo_horizontal -= mouse_delta.x * 0.003
        self.angulo_vertical   -= mouse_delta.y * 0.003
        limite = math.radians(80)
        self.angulo_vertical = max(-limite, min(limite, self.angulo_vertical))

        scroll = rl.get_mouse_wheel_move()
        self.distancia -= scroll * 1.0
        self.distancia = max(self.distancia_min, min(self.distancia_max, self.distancia))

        sin_h = math.sin(self.angulo_horizontal)
        cos_h = math.cos(self.angulo_horizontal)
        sin_v = math.sin(self.angulo_vertical)
        cos_v = math.cos(self.angulo_vertical)

        self.camera.position.x = (self.player.posicao.x
                                   + self.distancia * sin_h * cos_v)
        self.camera.position.y = max(
            0.3, self.player.posicao.y + 2.0 + self.distancia * sin_v)
        self.camera.position.z = (self.player.posicao.z
                                   + self.distancia * cos_h * cos_v)
        self.camera.target = self.player.posicao

        # ── Movimento do jogador — WASD / setas (relativo à câmera) ──────
        self.player.update(dt, sin_h, cos_h, self.cenario)

        # ── Atualizar estrelas ────────────────────────────────────────────
        for estrela in self.estrelas:
            if estrela.update(dt, self.tempo, self.player.posicao):
                self.estrelas_coletadas += 1

        # ── Condições de fim de jogo (Guardando dados para a EndScreen)───
        if self.estrelas_coletadas >= QUANTIDADE_ESTRELAS or self.timer <= 0:
            EndScreen.score = self.estrelas_coletadas
            EndScreen.victory = self.estrelas_coletadas >= QUANTIDADE_ESTRELAS
            self.needs_reset = True  # Garante reconfiguração na próxima partida
            return GameState.GAME_OVER

        return None

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self):
        if self.needs_reset:
            return
            
        rl.clear_background(rl.Color(10, 8, 20, 255))

        rl.begin_mode_3d(self.camera)

        # Cenário (chão, paredes, cubos, canos, cones)
        self.cenario.draw()

        # Estrelas coletáveis
        for estrela in self.estrelas:
            estrela.draw(self.tempo)

        # Jogador (cubo verde néon)
        self.player.draw()

        rl.end_mode_3d()

        self._draw_hud()

        if self.pausado:
            self._draw_pause_overlay()

    # ── HUD ───────────────────────────────────────────────────────────────────

    def _draw_hud(self):
        """Painel de informações: contador de estrelas + timer + barra de progresso."""
        rl.draw_rectangle(10, 10, 230, 88, rl.Color(0, 0, 0, 130))
        rl.draw_rectangle_lines(10, 10, 230, 88, rl.Color(255, 210, 30, 160))

        # Estrelas coletadas
        txt_e = f"Estrelas: {self.estrelas_coletadas} / {QUANTIDADE_ESTRELAS}"
        rl.draw_text(txt_e, 24, 22, 22, HUD_TEXTO)

        # Timer (fica vermelho nos últimos 10 segundos)
        secs  = max(0, int(self.timer))
        cor_t = HUD_ALERTA if secs <= 10 else HUD_TEXTO
        txt_t = f"Tempo:    {secs:02d}s"
        rl.draw_text(txt_t, 24, 54, 22, cor_t)

        # Barra de progresso das estrelas
        prog_w = int(206 * self.estrelas_coletadas / QUANTIDADE_ESTRELAS)
        rl.draw_rectangle(24, 80, 206, 8, rl.Color(30, 30, 50, 200))
        rl.draw_rectangle(24, 80, prog_w, 8, rl.Color(255, 210, 30, 220))

        # Dica de controles (rodapé)
        dica = "[WASD] ou [SETAS] para mover   [MOUSE] para orbitar   [ESC] para pausar"
        rl.draw_text(dica, 20, SCREEN_HEIGHT - 30, 16,
                     rl.Color(140, 145, 185, 200))

    # ── Overlay de Pausa ──────────────────────────────────────────────────────

    def _draw_pause_overlay(self):
        """Desenha o painel de pausa semitransparente sobre o jogo."""
        # Fundo escuro semitransparente
        rl.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                          rl.Color(0, 0, 0, 160))

        # Painel central
        pw, ph = 400, 240
        px = (SCREEN_WIDTH  - pw) // 2
        py = (SCREEN_HEIGHT - ph) // 2
        rl.draw_rectangle(px, py, pw, ph, rl.Color(12, 10, 30, 230))
        rl.draw_rectangle_lines_ex(
            rl.Rectangle(float(px), float(py), float(pw), float(ph)),
            2, rl.Color(255, 210, 30, 220)
        )

        # Título
        titulo = "PAUSADO"
        tw = rl.measure_text(titulo, 48)
        rl.draw_text(titulo, px + (pw - tw) // 2, py + 28, 48,
                     rl.Color(255, 210, 30, 255))

        # Separador
        rl.draw_line(px + 24, py + 88, px + pw - 24, py + 88,
                     rl.Color(255, 210, 30, 100))

        # Opções
        rl.draw_text("[ESC] ou [P]  para continuar", px + 40, py + 108, 22,
                     rl.Color(200, 210, 255, 230))
        rl.draw_text("[Enter]  para encerrar partida", px + 40, py + 148, 22,
                     rl.Color(200, 210, 255, 230))

        # Estatísticas rápidas
        secs = max(0, int(self.timer))
        stats = f"Estrelas: {self.estrelas_coletadas}/{QUANTIDADE_ESTRELAS}   Tempo: {secs:02d}s"
        sw = rl.measure_text(stats, 18)
        rl.draw_text(stats, px + (pw - sw) // 2, py + ph - 38, 18,
                     rl.Color(140, 145, 185, 200))