"""audio_manager.py — Gerenciador de Áudio do Super Racer 3D"""

import pyray as rl

CAMINHO_BASE = "assets/audio/"

MUSICAS = {
    "menu":    CAMINHO_BASE + "menu_music.mp3",
    "jogo":    CAMINHO_BASE + "game_music.mp3",
    "vitoria": CAMINHO_BASE + "victory_music.mp3",
    "derrota": CAMINHO_BASE + "defeat_music.mp3",
}

EFEITOS = {
    "moeda": CAMINHO_BASE + "coin_pickup.mp3",
}


class AudioManager:
    _musicas_carregadas = {}
    _efeitos_carregados = {}
    _musica_atual = None
    _volume_musica = 0.5
    _volume_efeito = 0.7
    _mutado = False

    @classmethod
    def init(cls):
        rl.init_audio_device()
        for nome, caminho in MUSICAS.items():
            cls._musicas_carregadas[nome] = rl.load_music_stream(caminho)
        for nome, caminho in EFEITOS.items():
            cls._efeitos_carregados[nome] = rl.load_sound(caminho)

    @classmethod
    def update(cls):
        if cls._musica_atual is not None:
            rl.update_music_stream(cls._musicas_carregadas[cls._musica_atual])

    @classmethod
    def tocar_musica(cls, nome: str):
        if cls._musica_atual == nome:
            return
        if cls._musica_atual is not None:
            rl.stop_music_stream(cls._musicas_carregadas[cls._musica_atual])
        cls._musica_atual = nome
        musica = cls._musicas_carregadas[nome]
        rl.set_music_volume(musica, 0.0 if cls._mutado else cls._volume_musica)
        rl.play_music_stream(musica)

    @classmethod
    def alternar_mute(cls):
        cls._mutado = not cls._mutado
        if cls._musica_atual is not None:
            musica = cls._musicas_carregadas[cls._musica_atual]
            rl.set_music_volume(musica, 0.0 if cls._mutado else cls._volume_musica)

    @classmethod
    def esta_mutado(cls) -> bool:
        return cls._mutado

    @classmethod
    def parar_musica(cls):
        if cls._musica_atual is not None:
            rl.stop_music_stream(cls._musicas_carregadas[cls._musica_atual])
            cls._musica_atual = None

    @classmethod
    def tocar_efeito(cls, nome: str):
        rl.set_sound_volume(cls._efeitos_carregados[nome], cls._volume_efeito)
        rl.play_sound(cls._efeitos_carregados[nome])

    @classmethod
    def close(cls):
        for musica in cls._musicas_carregadas.values():
            rl.unload_music_stream(musica)
        for efeito in cls._efeitos_carregados.values():
            rl.unload_sound(efeito)
        rl.close_audio_device()