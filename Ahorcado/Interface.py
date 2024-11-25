import tkinter as tk
from PIL import Image, ImageTk
from Ahorcado.Logic import HangmanGame

class HangmanInterface:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.root.title("EL AHORCADO")
        self.labelWord = tk.Label(root, text="Palabra: ___", font=("Helvetica", 16))
        self.labelWord.pack()

        # Adjust canvas size to match a reasonable size for the images
        self.canvas = tk.Canvas(root, width=200, height=200)
        self.canvas.pack()

        self.entryLetter = tk.Entry(root)
        self.entryLetter.pack()

        self.buttonGuess = tk.Button(root, text="ADIVINAR", command=self.guessLetter)
        self.buttonGuess.pack()

        self.labelStatus = tk.Label(root, text="Introduzca la letra:")
        self.labelStatus.pack()

    def updateImage(self):
        """Update the hangman image based on the number of failed attempts"""
        imagePath = self.game.getCurrentImage()

        if imagePath:
            try:
                img = Image.open(imagePath)
                # Resize image to fit the canvas size
                img = img.resize((200, 200)) # in case of necessary , Image.ANTIALIAS
                self.imgTk = ImageTk.PhotoImage(img)
                self.canvas.create_image(150, 200, image=self.imgTk)  # Center the image in the canvas
            except Exception as e:
                print(f"Error loading image: {e}")

    def guessLetter(self):
        """Handle the letter guess"""
        letter = self.entryLetter.get().strip().lower()
        self.entryLetter.delete(0, tk.END)

        try:
            if not letter.isalpha() or len(letter) != 1:
                raise ValueError("Introduce una letra válida individual")

            if self.game.guessLetter(letter):
                self.labelStatus.config(text="¡Correcto!")
            else:
                self.labelStatus.config(text="¡Incorrecto!")
                self.updateImage()

            # Update the displayed word
            self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")

            # Check if the game is over
            if self.game.isGameOver():
                if '_' not in self.game.guessedLetters:
                    self.labelStatus.config(text="¡Enhorabuena, ganaste!")
                else:
                    self.labelStatus.config(text=f"¡Perdiste! La palabra era: {self.game.word}")
                self.buttonGuess.config(state=tk.DISABLED)

        except ValueError as e:
            self.labelStatus.config(text=f"Error: {e}")
        except Exception as e:
            self.labelStatus.config(text=f"Error inesperado: {e}")
