"""end_screen.py — Tela de Fim de Jogo"""

import pyray as rl
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState


class EndScreen:
    """Tela de fim de jogo — a implementar"""

    def update(self, dt: float):
        # TODO: implementar lógica da tela de fim
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            return GameState.START
        return None

    def draw(self):
        rl.clear_background(rl.Color(10, 10, 20, 255))
        msg = "Fim de Jogo"
        sub = "[ A implementar ]"
        fs, sf = 48, 22
        rl.draw_text(msg, SCREEN_WIDTH // 2 - rl.measure_text(msg, fs) // 2,
                     SCREEN_HEIGHT // 2 - 40, fs, rl.WHITE)
        rl.draw_text(sub, SCREEN_WIDTH // 2 - rl.measure_text(sub, sf) // 2,
                     SCREEN_HEIGHT // 2 + 20, sf, rl.Color(150, 150, 180, 255))
        rl.draw_text("ESC - voltar", 20, SCREEN_HEIGHT - 30, 18, rl.Color(120, 120, 150, 255))
