"""
config.py — Configurações Globais do Super Racer 3D
=====================================================
Constantes compartilhadas por todos os módulos do jogo.
Altere aqui para ajustar comportamento sem mexer no código.
"""

# ── Tela ──────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE  = "Super Racer 3D"
TARGET_FPS    = 60

# ── Estados do Jogo ───────────────────────────────────────────────────────────
class GameState:
    START     = "start"
    PLAYING   = "playing"
    GAME_OVER = "game_over"
    EXIT      = "exit"   # sinal para encerrar o jogo de forma limpa

# ── Jogo ──────────────────────────────────────────────────────────────────────
# Ajustar conforme necessário ao longo do desenvolvimento
TEMPO_LIMITE        = 60   # segundos para acabar o jogo
QUANTIDADE_ESTRELAS = 20   # número de estrelas no cenário
