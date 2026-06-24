"""
Super Racer 3D — main.py
=========================
Trabalho Prático · Computação Gráfica · UTFPR
Prof. Dr. Marlon Marcon

Como rodar:
  pip install -r requirements.txt
  python main.py
"""

import pyray as rl
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, TARGET_FPS, GameState
from src.audio_manager import AudioManager
from src.screens.start_screen import StartScreen
from src.screens.game_screen import GameScreen
from src.screens.end_screen import EndScreen


def main():
    # ── Inicialização ─────────────────────────────────────────────────────────
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    rl.set_target_fps(TARGET_FPS)
    rl.set_exit_key(0)  # Desabilita ESC como saída automática (gerenciado pelo jogo)

    AudioManager.init()
    AudioManager.tocar_musica("menu")

    # ── Telas ─────────────────────────────────────────────────────────────
    screens = {
        GameState.START:     StartScreen(),
        GameState.PLAYING:   GameScreen(),
        GameState.GAME_OVER: EndScreen(),
    }

    current_state = GameState.START

    # ── Game Loop Principal (RT-05) ───────────────────────────────────────────
    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # 1. Tratamento de entrada + atualização de estado
        next_state = screens[current_state].update(dt)

        # Encerrar o jogo de forma limpa
        if next_state == GameState.EXIT:
            break

        # Transição de tela
        if next_state and next_state != current_state:
            current_state = next_state
            if current_state == GameState.START:
                AudioManager.tocar_musica("menu")
            elif current_state == GameState.PLAYING:
                AudioManager.tocar_musica("jogo")
            elif current_state == GameState.GAME_OVER:
                AudioManager.tocar_musica("vitoria" if EndScreen.victory else "derrota")

        AudioManager.update()

        # 2. Renderização
        rl.begin_drawing()
        screens[current_state].draw()
        rl.end_drawing()

    AudioManager.close()
    rl.close_window()


if __name__ == "__main__":
    main()