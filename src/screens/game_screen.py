"""game_screen.py — Tela de Jogo"""

import math
import pyray as rl

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GameState,
    ARENA_SIZE, VELOCIDADE_JOGADOR, TEMPO_LIMITE, QUANTIDADE_ESTRELAS,
)
from src.world.palette import JOGADOR, JOGADOR_WIRE, HUD_TEXTO, HUD_ALERTA
from src.world.scenario import Scenario
from src.world.star import Star


# ── Posições das estrelas ─────────────────────────────────────────────────────
# 10 posições verificadas manualmente para não colidirem com nenhum obstáculo.
# Cada posição mantém pelo menos ~1.5 unidades de distância do centro dos obstáculos.
_POSICOES_ESTRELAS: list[tuple[float, float]] = [
    (-8.5, -8.5),   # canto SO — livre
    ( 8.5, -8.5),   # canto SE — livre
    (-8.5,  8.5),   # canto NO — livre
    ( 8.5,  8.5),   # canto NE — livre (2.1u do cubo 7,7)
    ( 0.0,  0.0),   # centro   — livre (3.6u do cubo mais próximo)
    (-4.0, -0.5),   # interior — livre (2.5u dos obstáculos)
    ( 3.0, -7.5),   # sul      — livre (2.5u do cubo 5,-6)
    (-7.0,  7.0),   # noroeste — livre (4.1u do cubo -8,3)
    ( 5.5, -2.5),   # leste    — livre (1.6u do cone 4,-3 → gap > STAR_COLLECT_RADIUS)
    (-1.0,  2.5),   # centro-N — livre (2.1u do cano -3,3)
]


class GameScreen:
    """
    Tela principal do jogo.

    Responsabilidades:
        - Câmera orbital com mouse (mantida intacta).
        - Movimento do jogador (WASD / setas).
        - Renderização do cenário (Scenario) e estrelas (Star).
        - HUD: contador de estrelas + timer regressivo + barra de progresso.
        - Condição de fim: todas as estrelas coletadas OU tempo esgotado.
    """

    def __init__(self):
        self.cubo_posicao = rl.Vector3(0.0, 0.5, 0.0)
        self.tempo        = 0.0
        self.timer        = float(TEMPO_LIMITE)

        # ── Câmera (mantida intacta conforme código original) ─────────────
        self.camera = rl.Camera3D()
        self.camera.position   = rl.Vector3(0.0, 3.0, 6.0)
        self.camera.target     = self.cubo_posicao
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
        self.estrelas: list[Star] = [
            Star(x, z, fase=i * 0.47)
            for i, (x, z) in enumerate(_POSICOES_ESTRELAS)
        ]
        self.estrelas_coletadas = 0

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float):
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

        self.camera.position.x = (self.cubo_posicao.x
                                   + self.distancia * sin_h * cos_v)
        self.camera.position.y = max(
            0.3, self.cubo_posicao.y + 1.5 + self.distancia * sin_v)
        self.camera.position.z = (self.cubo_posicao.z
                                   + self.distancia * cos_h * cos_v)
        self.camera.target = self.cubo_posicao

        # ── Movimento do jogador — WASD / setas (relativo à câmera) ──────
        spd = VELOCIDADE_JOGADOR * dt

        if rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_UP):
            self.cubo_posicao.x -= sin_h * spd
            self.cubo_posicao.z -= cos_h * spd

        if rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_DOWN):
            self.cubo_posicao.x += sin_h * spd
            self.cubo_posicao.z += cos_h * spd

        if rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_LEFT):
            self.cubo_posicao.x -= cos_h * spd
            self.cubo_posicao.z += sin_h * spd

        if rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_RIGHT):
            self.cubo_posicao.x += cos_h * spd
            self.cubo_posicao.z -= sin_h * spd

        # Colisão simples com as paredes da arena
        half = ARENA_SIZE / 2 - 0.6
        self.cubo_posicao.x = max(-half, min(half, self.cubo_posicao.x))
        self.cubo_posicao.z = max(-half, min(half, self.cubo_posicao.z))

        # ── Atualizar estrelas ────────────────────────────────────────────
        for estrela in self.estrelas:
            if estrela.update(dt, self.tempo, self.cubo_posicao):
                self.estrelas_coletadas += 1

        # ── Condições de fim de jogo ──────────────────────────────────────
        if self.estrelas_coletadas >= QUANTIDADE_ESTRELAS or self.timer <= 0:
            return GameState.GAME_OVER

        if rl.is_key_pressed(rl.KEY_ESCAPE):
            return GameState.START

        if rl.is_key_pressed(rl.KEY_ENTER):
            return GameState.GAME_OVER

        return None

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self):
        rl.clear_background(rl.Color(10, 8, 20, 255))

        rl.begin_mode_3d(self.camera)

        # Cenário (chão, paredes, cubos, canos, cones)
        self.cenario.draw()

        # Estrelas coletáveis
        for estrela in self.estrelas:
            estrela.draw(self.tempo)

        # Jogador (cubo verde néon)
        rl.draw_cube(self.cubo_posicao, 1.0, 1.0, 1.0, JOGADOR)
        rl.draw_cube_wires(self.cubo_posicao, 1.0, 1.0, 1.0, JOGADOR_WIRE)

        rl.end_mode_3d()

        self._draw_hud()

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
        dica = "WASD / \u2191\u2193\u2190\u2192 mover   |   mouse orbitar   |   ESC voltar"
        rl.draw_text(dica, 20, SCREEN_HEIGHT - 30, 16,
                     rl.Color(140, 145, 185, 200))