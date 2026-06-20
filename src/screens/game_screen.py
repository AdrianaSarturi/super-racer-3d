"""game_screen.py — Tela de Jogo"""

import math
import pyray as rl
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState


class GameScreen:
    """Tela principal do jogo — a implementar"""

    def __init__(self):
        self.cubo_posicao = rl.Vector3(0.0, 0.5, 0.0)

        self.camera = rl.Camera3D()
        self.camera.position = rl.Vector3(0.0, 3.0, 6.0)
        self.camera.target = self.cubo_posicao
        self.camera.up = rl.Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 60.0
        self.camera.projection = rl.CAMERA_PERSPECTIVE

        self.angulo_horizontal = 0.0
        self.angulo_vertical = 0.3
        self.distancia = 6.0
        self.distancia_min = 4.0
        self.distancia_max = 10.0


    def update(self, dt: float):

        mouse_delta = rl.get_mouse_delta()
        self.angulo_horizontal -= mouse_delta.x * 0.003
        self.angulo_vertical -= mouse_delta.y * 0.003
        limite = math.radians(80)
        self.angulo_vertical = max(-limite, min(limite, self.angulo_vertical))
        scroll = rl.get_mouse_wheel_move()
        self.distancia -= scroll * 1.0
        self.distancia = max(self.distancia_min, min(self.distancia_max, self.distancia))

        self.camera.position.x = self.cubo_posicao.x + self.distancia * math.sin(self.angulo_horizontal) * math.cos(self.angulo_vertical)
        self.camera.position.y = max(0.3, self.cubo_posicao.y + 1.5 + self.distancia * math.sin(self.angulo_vertical))
        self.camera.position.z = self.cubo_posicao.z + self.distancia * math.cos(self.angulo_horizontal) * math.cos(self.angulo_vertical)
        self.camera.target = self.cubo_posicao

        # TODO: implementar lógica do jogo
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            return GameState.START  # volta para a tela inicial com ESC
        if rl.is_key_pressed(rl.KEY_ENTER):
            return GameState.GAME_OVER  # atalho temporário para ver a end_screen
        return None

    def draw(self):
        rl.clear_background(rl.Color(20, 20, 30, 255))

        rl.begin_mode_3d(self.camera)
        rl.draw_grid(20, 1.0)
        rl.draw_cube(self.cubo_posicao, 1.0, 1.0, 1.0, rl.RED)
        rl.draw_cube_wires(self.cubo_posicao, 1.0, 1.0, 1.0, rl.MAROON)
        rl.draw_cube(rl.Vector3(5.0, 0.5, 0.0), 1.0, 1.0, 1.0, rl.BLUE)
        rl.draw_cube(rl.Vector3(-5.0, 0.5, 0.0), 1.0, 1.0, 1.0, rl.GREEN)
        rl.draw_cube(rl.Vector3(0.0, 0.5, 5.0), 1.0, 1.0, 1.0, rl.YELLOW)
        rl.draw_cube(rl.Vector3(0.0, 0.5, -5.0), 1.0, 1.0, 1.0, rl.PURPLE)
        rl.end_mode_3d()

        rl.draw_text("Mova o mouse para orbitar a camera", 20, 20, 20, rl.WHITE)
        rl.draw_text("ESC - voltar", 20, SCREEN_HEIGHT - 30, 18, rl.Color(120, 120, 150, 255))