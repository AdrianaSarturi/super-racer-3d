"""
coin.py — Moeda 3D Animada do Super Racer 3D
=============================================
Geometria: cilindro achatado (flat disk) com brilho central.
Animações:
    - Oscilação vertical: seno suave para cima e para baixo.
    - Partículas orbitantes: 3 pontos dourados girando ao redor.
    - Pulso de brilho: variação de intensidade luminosa.

Cores vêm de palette.py (RT-02).
"""

import math
import pyray as rl

from src.world.palette import MOEDA, MOEDA_BRILHO, MOEDA_BORDA
from config import COIN_COLLECT_RADIUS


class Coin:
    """
    Moeda 3D coletável com animações de oscilação e brilho pulsante.

    Atributos:
        x, z    -- posição horizontal na arena
        fase    -- offset de fase para variação entre moedas (evita sincronia)
        ativa   -- False quando coletada (não renderiza nem colide)
    """

    # ── Constantes de animação ─────────────────────────────────────────────────
    ALTURA_BASE  = 0.45   # altura do centro da moeda em repouso (acima do chão)
    AMPLITUDE    = 0.18   # amplitude da oscilação vertical (±unidades)
    FREQ_OSCIL   = 2.0    # frequência da oscilação (rad/s)
    FREQ_ORBIT   = 2.4    # velocidade das partículas orbitantes (rad/s)
    NUM_PARTICULAS = 3    # pontos dourados orbitando

    # ── Geometria ─────────────────────────────────────────────────────────────
    RAIO        = 0.14   # raio do disco da moeda
    ESPESSURA   = 0.12   # espessura do cilindro
    RAIO_BRILHO = 0.16   # raio do reflexo central
    RAIO_ORBIT  = 0.58   # raio da órbita das partículas
    TAM_PARTICULA = 0.025 # tamanho dos pontos orbitantes

    def __init__(self, x: float, z: float, fase: float = 0.0):
        self.x    = x
        self.z    = z
        self.fase = fase
        self.ativa = True

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float, tempo: float, player_pos: rl.Vector3) -> bool:
        """
        Verifica colisão com o jogador.

        Returns:
            True se a moeda foi coletada neste frame (distância < COIN_COLLECT_RADIUS).
        """
        if not self.ativa:
            return False

        dx   = player_pos.x - self.x
        dz   = player_pos.z - self.z
        dist = math.sqrt(dx * dx + dz * dz)

        if dist < COIN_COLLECT_RADIUS:
            self.ativa = False
            return True

        return False

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, tempo: float) -> None:
        """Renderiza a moeda animada (chamar dentro de begin_mode_3d)."""
        if not self.ativa:
            return

        # Posição Y oscilante
        y = self.ALTURA_BASE + self.AMPLITUDE * math.sin(
            self.FREQ_OSCIL * tempo + self.fase
        )

        # Pulso de brilho (0.6 → 1.0)
        brilho = 0.70 + 0.30 * abs(math.sin(tempo * 3.0 + self.fase))

        # ── Corpo da moeda (cilindro achatado, horizontal) ─────────────────
        # draw_cylinder posiciona a base (bottom) em `pos`, cresce para +Y
        pos_base = rl.Vector3(self.x, y - self.ESPESSURA / 2, self.z)
        rl.draw_cylinder(pos_base, self.RAIO, self.RAIO, self.ESPESSURA, 20, MOEDA)

        # ── Borda escura (cylider wire levemente maior) ────────────────────
        rl.draw_cylinder_wires(pos_base, self.RAIO + 0.01, self.RAIO + 0.01,
                               self.ESPESSURA, 20, MOEDA_BORDA)

        # ── Brilho central (disco fino no topo) ───────────────────────────
        brilho_alpha = int(180 + 75 * brilho)
        cor_brilho   = rl.Color(
            MOEDA_BRILHO.r, MOEDA_BRILHO.g, MOEDA_BRILHO.b, brilho_alpha
        )
        pos_topo = rl.Vector3(self.x, y + self.ESPESSURA / 2, self.z)
        rl.draw_cylinder(pos_topo, self.RAIO_BRILHO, self.RAIO_BRILHO,
                         0.01, 14, cor_brilho)

        # ── Partículas orbitantes ─────────────────────────────────────────
        step = (math.pi * 2) / self.NUM_PARTICULAS
        for i in range(self.NUM_PARTICULAS):
            ang = self.FREQ_ORBIT * tempo + self.fase + i * step
            px  = self.x + self.RAIO_ORBIT * math.cos(ang)
            pz  = self.z + self.RAIO_ORBIT * math.sin(ang)
            py  = y + 0.04 * math.sin(ang * 2)  # leve ondulação vertical

            # Tamanho varia com o ângulo (dá impressão de profundidade)
            sz  = self.TAM_PARTICULA * (0.7 + 0.3 * abs(math.sin(ang)))
            palpha = int(160 + 95 * abs(math.sin(ang + tempo)))
            cor_p  = rl.Color(MOEDA.r, MOEDA.g, MOEDA.b, palpha)
            rl.draw_sphere(rl.Vector3(px, py, pz), sz, cor_p)
