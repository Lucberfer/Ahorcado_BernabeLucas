from Ahorcado.Interface import HangmanInterface
from Ahorcado.Logic import HangmanGame
from tkinter import Tk

if __name__ == "__main__":
    try:
        # Initialize the game
        game = HangmanGame()
        game.addUser("Player 1")

        # Create the main window for the interface
        root = Tk()
        app = HangmanInterface(root, game)

        # Start
        root.mainloop()
    except Exception as e:
        print(f"Error inesperad mientras se inicia el juego: {e}")
