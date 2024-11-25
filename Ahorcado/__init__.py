from tkinter import Tk
from Ahorcado.Interface import HangmanInterface
from Ahorcado.Logic import HangmanGame

if __name__ == "__main__":
    try:
        game = HangmanGame()
        root = Tk()
        app = HangmanInterface(root, game)
        root.mainloop()
    except Exception as e:
        print(f"Error inexperado al iniciar el juego: {e}")