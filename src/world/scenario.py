"""
scenario.py — Cenário 3D do Super Racer 3D
===========================================
Responsável por: chão em grid, paredes limítrofes e obstáculos variados.

Tipos de obstáculos:
    - Cubos/caixas:  obstáculos sólidos de metal enferrujado.
    - Canos (canos): bollards metálicos verticais com anel refletor.
    - Cones:         cones de trânsito laranja com faixas brancas.

Todas as cores vêm de palette.py (RT-02).
"""

import pyray as rl
from src.world.palette import (
    CHAO_A, CHAO_B,
    PAREDE, PAREDE_TOPO,
    OBSTACULO, OBSTACULO_WIRE,
    CANO, CANO_TOPO, CANO_ANEL,
    CONE, CONE_FAIXA, CONE_BASE,
)
from config import ARENA_SIZE


class Scenario:
    """
    Constrói e renderiza o cenário completo da arena.

    Estrutura:
        - Chão:   grid de tiles 1×1 com cores alternadas.
        - Paredes: 4 paredes ao redor da arena (height=2).
        - Cubos:   caixas metálicas espalhadas pela arena.
        - Canos:   bollards cilíndricos verticais.
        - Cones:   cones de trânsito com faixas refletivas.
    """

    # ── Obstáculos — Cubos ── (cx, cy_centro, cz, tamanho_lado)
    CUBOS: list[tuple] = [
        ( 3.0, 0.50,  2.0, 1.0),
        (-4.0, 0.60,  5.0, 1.2),
        ( 7.0, 0.40,  1.0, 0.8),
        (-2.0, 0.75, -4.0, 1.5),
        ( 5.0, 0.50, -6.0, 1.0),
        (-6.0, 0.55, -2.0, 1.1),
        ( 2.0, 0.45,  8.0, 0.9),
        (-8.0, 0.65,  3.0, 1.3),
        ( 0.0, 0.50, -8.0, 1.0),
        ( 7.0, 0.40,  7.0, 0.8),
    ]

    # ── Obstáculos — Canos ── (cx, cz)   raio=0.15, altura=1.5
    CANOS: list[tuple] = [
        (-3.0,  3.0),
        ( 5.0,  4.0),
        (-6.0, -6.0),
        ( 1.0, -5.0),
        ( 8.5, -2.0),
        (-1.0,  6.0),
    ]

    # ── Obstáculos — Cones ── (cx, cz)   base=0.45, altura=1.0
    CONES: list[tuple] = [
        ( 4.0, -3.0),
        (-5.0,  1.0),
        ( 2.0,  5.0),
        (-7.5, -4.0),
        ( 7.5,  4.5),
    ]

    def __init__(self):
        self._half = ARENA_SIZE / 2  # = 10.0

    # ── API pública ───────────────────────────────────────────────────────────

    def draw(self) -> None:
        """Renderiza o cenário completo (chamar dentro de begin_mode_3d)."""
        self._draw_chao()
        self._draw_paredes()
        self._draw_cubos()
        self._draw_canos()
        self._draw_cones()

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _draw_chao(self) -> None:
        """Grid de tiles 1×1 com cores alternadas (CHAO_A / CHAO_B)."""
        half = self._half
        n    = int(ARENA_SIZE)
        for row in range(n):
            for col in range(n):
                x   = -half + col + 0.5
                z   = -half + row + 0.5
                cor = CHAO_A if (row + col) % 2 == 0 else CHAO_B
                rl.draw_cube(rl.Vector3(x, -0.05, z), 1.0, 0.10, 1.0, cor)

    def _draw_paredes(self) -> None:
        """Quatro paredes limítrofes com topo decorativo."""
        half  = self._half
        h     = 2.0
        t     = 0.5
        arena = float(ARENA_SIZE)

        self._parede(rl.Vector3( 0,      h / 2,  half), arena, h, t)  # Norte
        self._parede(rl.Vector3( 0,      h / 2, -half), arena, h, t)  # Sul
        self._parede(rl.Vector3( half,   h / 2,  0),    t,     h, arena)  # Leste
        self._parede(rl.Vector3(-half,   h / 2,  0),    t,     h, arena)  # Oeste

    def _parede(self, pos: rl.Vector3, w: float, h: float, d: float) -> None:
        rl.draw_cube(pos, w, h, d, PAREDE)
        topo = rl.Vector3(pos.x, pos.y + h / 2 + 0.06, pos.z)
        rl.draw_cube(topo, w, 0.12, d, PAREDE_TOPO)

    def _draw_cubos(self) -> None:
        """Caixas metálicas com wireframe de destaque."""
        for (cx, cy, cz, s) in self.CUBOS:
            pos = rl.Vector3(cx, cy, cz)
            rl.draw_cube(pos, s, s, s, OBSTACULO)
            rl.draw_cube_wires(pos, s, s, s, OBSTACULO_WIRE)

    def _draw_canos(self) -> None:
        """
        Bollards metálicos: cilindro cinza com tampa e anel refletor amarelo.
        Raio = 0.15, Altura = 1.5 unidades.
        """
        raio  = 0.15
        alt   = 1.40
        for (cx, cz) in self.CANOS:
            base = rl.Vector3(cx, 0.0,  cz)
            topo = rl.Vector3(cx, alt,  cz)
            anel = rl.Vector3(cx, alt * 0.55, cz)

            # Corpo
            rl.draw_cylinder(base, raio, raio, alt, 12, CANO)
            # Tampa (levemente mais larga)
            rl.draw_cylinder(topo, raio + 0.05, raio + 0.05, 0.08, 12, CANO_TOPO)
            # Anel refletor
            rl.draw_cylinder(anel, raio + 0.02, raio + 0.02, 0.07, 12, CANO_ANEL)

    def _draw_cones(self) -> None:
        """
        Cones de trânsito: laranja com faixas brancas refletivas e base escura.
        Base = 0.45, Altura = 1.0 unidade.
        """
        base_r = 0.45
        alt    = 1.00

        for (cx, cz) in self.CONES:
            orig = rl.Vector3(cx, 0.0, cz)

            # Base de borracha (disco fino escuro)
            rl.draw_cylinder(rl.Vector3(cx, -0.02, cz),
                             base_r + 0.05, base_r + 0.05, 0.04, 10, CONE_BASE)

            # Corpo do cone (afilado até ponteiro quase nulo)
            rl.draw_cylinder(orig, 0.04, base_r, alt, 10, CONE)

            # Faixa refletiva inferior (altura ~30% do cone)
            #   raio nessa altura = lerp(0.04, 0.45, 1 - 0.3) = ~0.32
            rl.draw_cylinder(rl.Vector3(cx, alt * 0.28, cz),
                             0.32, 0.32, 0.08, 10, CONE_FAIXA)

            # Faixa refletiva superior (altura ~60% do cone)
            #   raio nessa altura = lerp(0.04, 0.45, 1 - 0.6) = ~0.20
            rl.draw_cylinder(rl.Vector3(cx, alt * 0.58, cz),
                             0.20, 0.20, 0.06, 10, CONE_FAIXA)
