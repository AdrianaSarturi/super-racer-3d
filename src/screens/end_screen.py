"""end_screen.py — Tela de Fim de Jogo"""

import pyray as rl
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GameState

 
class EndScreen:
    """
    Tela de fim de jogo com exibição de resultados dinâmicos e opções de reinício.
    """

    # Variáveis estáticas de classe para receber os dados vindos de game_screen.py
    score = 0
    victory = False

    def update(self, dt: float):
        # Permite ao jogador reiniciar a partida diretamente
        if rl.is_key_pressed(rl.KEY_ENTER):
            return GameState.PLAYING

        # Permite ao jogador voltar para o menu principal
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            return GameState.START

        return None

    def draw(self):
        # Fundo escuro personalizado para a tela de fim
        rl.clear_background(rl.Color(10, 10, 20, 255))

        # 1. Definir o título e subtítulo com base no resultado da partida
        if EndScreen.victory:
            titulo = "VITÓRIA!"
            cor_titulo = rl.GOLD
            subtitulo = "Incrivel! Voc\u00ea coletou todas as estrelas a tempo!"
        else:
            titulo = "FIM DE JOGO"
            cor_titulo = rl.RED
            subtitulo = "O tempo limite esgotou!"

        # Desenhar o título principal centralizado
        fs_titulo = 56
        tw_titulo = rl.measure_text(titulo, fs_titulo)
        rl.draw_text(titulo, SCREEN_WIDTH // 2 - tw_titulo // 2, 200, fs_titulo, cor_titulo)

        # Desenhar o subtítulo de contexto centralizado
        fs_sub = 20
        tw_sub = rl.measure_text(subtitulo, fs_sub)
        rl.draw_text(subtitulo, SCREEN_WIDTH // 2 - tw_sub // 2, 280, fs_sub, rl.LIGHTGRAY)

        # 2. Exibição da pontuação final alcançada
        txt_score = f"Estrelas Coletadas: {EndScreen.score}"
        fs_score = 24
        tw_score = rl.measure_text(txt_score, fs_score)
        rl.draw_text(txt_score, SCREEN_WIDTH // 2 - tw_score // 2, 360, fs_score, rl.YELLOW)

        # 3. Instruções de navegação do jogador (Rodapé)
        inst_jogar = "Pressione [ENTER] para Jogar Novamente"
        inst_menu  = "Pressione [ESC] para Voltar ao Menu"
        
        rl.draw_text(inst_jogar, SCREEN_WIDTH // 2 - rl.measure_text(inst_jogar, 18) // 2, 500, 18, rl.GRAY)
        rl.draw_text(inst_menu, SCREEN_WIDTH // 2 - rl.measure_text(inst_menu, 18) // 2, 535, 18, rl.GRAY)