"""player.py — Entidade do Jogador (Stickman Personalizado com Rotação e Expressão Facial)"""

import math
import pyray as rl
from config import VELOCIDADE_JOGADOR, ARENA_SIZE

class Player:
    """
    Classe do jogador baseada num Boneco de Palito (Stickman) 3D.
    Garante o modelo geométrico colorido, rosto com olhos/boca, 
    colisão dinâmica perfeita e rotação para a direção de movimento.
    """
  
    def __init__(self):
        # Posição inicial dos pés do boneco no chão (Y = 0.0)
        self.posicao = rl.Vector3(0.0, 0.0, 0.0)
        # Raio de colisão lateral ajustado para o boneco de palito
        self.raio_colisao = 0.35
        # Ângulo atual de rotação do personagem (em graus)
        self.angulo_rotacao = 0.0

        self.tempo_andando = 0.0
        self.velocidade_passada = 8.0
        self.amplitude_passada = 35.0
        self.angulo_passada = 0.0

        # Definindo as novas cores solicitadas
        self.cor_corpo = rl.Color(0, 121, 241, 255)    # Azul vibrante
        self.cor_cabeca = rl.Color(245, 200, 160, 255) # Bege / tom de pele
        self.cor_detalhe = rl.Color(20, 20, 30, 255)   # Preto fosco para olhos e boca

    def update(self, dt: float, sin_h: float, cos_h: float, cenario):
        """Atualiza o movimento baseado no input, roda o modelo e resolve colisões."""
        spd = VELOCIDADE_JOGADOR * dt

        # Guarda a intenção de movimento relativa à câmera
        mover_x = 0.0
        mover_z = 0.0

        if rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_UP):
            mover_x -= sin_h * spd
            mover_z -= cos_h * spd
        if rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_DOWN):
            mover_x += sin_h * spd
            mover_z += cos_h * spd
        if rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_LEFT):
            mover_x -= cos_h * spd
            mover_z += sin_h * spd
        if rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_RIGHT):
            mover_x += cos_h * spd
            mover_z -= sin_h * spd

        # Se houver qualquer intenção de movimento, calcula o ângulo para onde olhar
        if mover_x != 0.0 or mover_z != 0.0:
            radianos = math.atan2(mover_x, mover_z)
            self.angulo_rotacao = math.degrees(radianos)

        esta_andando = (mover_x != 0.0 or mover_z != 0.0)
        if esta_andando:
            self.tempo_andando += dt
            self.angulo_passada = (
                math.sin(self.tempo_andando * self.velocidade_passada)
                * self.amplitude_passada
            )
        else:
            self.angulo_passada *= max(0.0, 1.0 - dt * 10.0)

        # Próxima posição proposta
        proximo_x = self.posicao.x + mover_x
        proximo_z = self.posicao.z + mover_z

        # Deslize inteligente contra o cenário ativo
        if not self._verificar_colisao(proximo_x, self.posicao.z, cenario):
            self.posicao.x = proximo_x

        if not self._verificar_colisao(self.posicao.x, proximo_z, cenario):
            self.posicao.z = proximo_z

        # Limites das paredes externas da arena
        half = ARENA_SIZE / 2 - 0.35
        self.posicao.x = max(-half, min(half, self.posicao.x))
        self.posicao.z = max(-half, min(half, self.posicao.z))

    def _verificar_colisao(self, x: float, z: float, cenario) -> bool:
        """Deteção de colisão precisa lendo as listas reais do objeto Scenario."""
        for cubo in cenario.CUBOS:
            cx, _, cz, tamanho = cubo
            if self._testar_caixa(x, z, cx, cz, tamanho, Manhattan:=tamanho):
                return True

        for cx, cz in cenario.CANOS:
            if self._testar_caixa(x, z, cx, cz, 0.4, 0.4):
                return True

        for cx, cz in cenario.CONES:
            if self._testar_caixa(x, z, cx, cz, 0.9, 0.9):
                return True

        return False

    def _testar_caixa(self, px: float, pz: float, ob_x: float, ob_z: float, tam_x: float, tam_z: float) -> bool:
        """Função auxiliar matemática para a caixa de colisão expandida."""
        min_x = ob_x - (tam_x / 2.0) - self.raio_colisao
        max_x = ob_x + (tam_x / 2.0) + self.raio_colisao
        min_z = ob_z - (tam_z / 2.0) - self.raio_colisao
        max_z = ob_z + (tam_z / 2.0) + self.raio_colisao
        return min_x <= px <= max_x and min_z <= pz <= max_z

    def draw(self):
            """Desenha o personagem estilo Boneco de Palito colorido e detalhado em 3D."""
            p = self.posicao

            rl.rl_push_matrix()
            
            # 1. Translação e Rotação no eixo Y local baseadas nas matrizes da Raylib
            rl.rl_translatef(p.x, p.y, p.z)
            # Adicionamos + 180 para inverter o rosto e alinhá-lo com a direção de movimento
            rl.rl_rotatef(self.angulo_rotacao + 180.0, 0.0, 1.0, 0.0)

            # ── CORPO (AZUL) ──────────────────────────────────────────────────────
            # Tronco/Corpo
            rl.draw_cylinder_ex(rl.Vector3(0.0, 0.5, 0.0), 
                                rl.Vector3(0.0, 1.2, 0.0), 
                                0.05, 0.05, 8, self.cor_corpo)

            rad_passada = math.radians(self.angulo_passada)
            desloc_perna = math.sin(rad_passada) * 0.18

            rl.draw_cylinder_ex(rl.Vector3(0.0, 0.5, 0.0),
                                rl.Vector3(-0.18, 0.0, desloc_perna),
                                0.035, 0.035, 6, self.cor_corpo)
            rl.draw_cylinder_ex(rl.Vector3(0.0, 0.5, 0.0),
                                rl.Vector3(0.18, 0.0, -desloc_perna),
                                0.035, 0.035, 6, self.cor_corpo)

            desloc_braco = math.sin(rad_passada) * 0.15

            rl.draw_cylinder_ex(rl.Vector3(0.0, 1.0, 0.0),
                                rl.Vector3(-0.22, 0.75, -0.05 - desloc_braco),
                                0.03, 0.03, 6, self.cor_corpo)
            rl.draw_cylinder_ex(rl.Vector3(0.0, 1.0, 0.0),
                                rl.Vector3(0.22, 0.75, -0.05 + desloc_braco),
                                0.03, 0.03, 6, self.cor_corpo)

            # ── CABEÇA (BEGE) ─────────────────────────────────────────────────────
            cabeca_centro = rl.Vector3(0.0, 1.35, 0.0)
            rl.draw_sphere(cabeca_centro, 0.15, self.cor_cabeca)

            # ── FEIÇÕES FACIAIS (Agora apontadas corretamente para a frente do movimento) ──
            # Olho Esquerdo
            rl.draw_sphere(rl.Vector3(-0.05, 1.38, -0.13), 0.02, self.cor_detalhe)
            
            # Olho Direito
            rl.draw_sphere(rl.Vector3(0.05, 1.38, -0.13), 0.02, self.cor_detalhe)

            # Boca (Sorriso)
            rl.draw_cube(rl.Vector3(0.0, 1.29, -0.13), 0.06, 0.015, 0.02, self.cor_detalhe)

            rl.rl_pop_matrix()