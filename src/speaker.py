import time

from pygame import mixer


class Speaker:

    def __init__(self):
        pass

    @staticmethod
    def play_sound():
        try:
            mixer.init()
            mixer.music.load("src/assets/sound/soundtrack.mp3")
            mixer.music.play()
            print("Playing music...")
            while mixer.music.get_busy():
                time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")