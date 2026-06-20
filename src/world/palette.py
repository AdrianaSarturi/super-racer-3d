"""
palette.py — Paleta de Cores do Super Racer 3D
================================================
Todos os materiais e cores do jogo definidos aqui.
Altere neste arquivo para ajustar o visual sem tocar nos outros módulos.

Tema: Sci-fi / Corrida Noturna — escuro com acentos vibrantes.
"""

import pyray as rl

# ── Chão ──────────────────────────────────────────────────────────────────────
CHAO_A      = rl.Color(38,  35,  52,  255)  # quadrado escuro (roxo profundo)
CHAO_B      = rl.Color(52,  48,  72,  255)  # quadrado claro  (roxo médio)

# ── Paredes ───────────────────────────────────────────────────────────────────
PAREDE      = rl.Color(55,  50,  78,  255)  # pedra roxa acinzentada
PAREDE_TOPO = rl.Color(88,  82, 125,  255)  # fresta superior (mais clara)

# ── Obstáculos — Cubos ────────────────────────────────────────────────────────
OBSTACULO      = rl.Color(175,  72,  35,  255)  # laranja ferrugem
OBSTACULO_WIRE = rl.Color(215, 110,  60,  255)  # wireframe — destaque quente

# ── Obstáculos — Canos (bollards metálicos) ───────────────────────────────────
CANO        = rl.Color( 78,  84,  96,  255)  # cinza metálico escuro
CANO_TOPO   = rl.Color(112, 120, 136,  255)  # tampa reflexiva (mais clara)
CANO_ANEL   = rl.Color(255, 200,  45,  200)  # anel refletor amarelo

# ── Obstáculos — Cones de Trânsito ───────────────────────────────────────────
CONE        = rl.Color(220,  55,  25,  255)  # laranja-vermelho (perigo)
CONE_FAIXA  = rl.Color(248, 248, 248,  240)  # faixas brancas refletivas
CONE_BASE   = rl.Color( 40,  40,  40,  255)  # base escura de borracha

# ── Estrelas (coletáveis) ─────────────────────────────────────────────────────
ESTRELA        = rl.Color(255, 208,  28,  255)  # dourado vivo
ESTRELA_BRILHO = rl.Color(255, 248, 180,  255)  # reflexo central (quase branco)
ESTRELA_BORDA  = rl.Color(195, 145,   8,  255)  # borda mais escura

# ── Jogador ───────────────────────────────────────────────────────────────────
JOGADOR      = rl.Color( 40, 200, 115,  255)  # verde néon
JOGADOR_WIRE = rl.Color( 15, 130,  70,  255)  # wireframe do jogador

# ── HUD ───────────────────────────────────────────────────────────────────────
HUD_TEXTO  = rl.Color(220, 225, 255,  255)  # branco levemente azulado
HUD_ALERTA = rl.Color(255,  90,  70,  255)  # vermelho-laranja (timer baixo)
