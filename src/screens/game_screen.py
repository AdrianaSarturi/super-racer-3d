"""game_screen.py — Tela de Jogo"""

import pyray as rl
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState


class GameScreen:
    """Tela principal do jogo — a implementar"""

    def update(self, dt: float):
        # TODO: implementar lógica do jogo
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            return GameState.START  # volta para a tela inicial com ESC
        if rl.is_key_pressed(rl.KEY_ENTER):
            return GameState.GAME_OVER  # atalho temporário para ver a end_screen
        return None

    def draw(self):
        # Placeholder visual até a implementação completa
        rl.clear_background(rl.Color(10, 10, 20, 255))
        msg = "Tela de Jogo"
        sub = "[ A implementar ]"
        fs, sf = 48, 22
        rl.draw_text(msg, SCREEN_WIDTH // 2 - rl.measure_text(msg, fs) // 2,
                     SCREEN_HEIGHT // 2 - 40, fs, rl.WHITE)
        rl.draw_text(sub, SCREEN_WIDTH // 2 - rl.measure_text(sub, sf) // 2,
                     SCREEN_HEIGHT // 2 + 20, sf, rl.Color(150, 150, 180, 255))
        rl.draw_text("ESC - voltar", 20, SCREEN_HEIGHT - 30, 18, rl.Color(120, 120, 150, 255))
