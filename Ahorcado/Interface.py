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

        # Ajustar el tamaño del lienzo para adaptarse al tamaño razonable de las imágenes
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        # Campo de entrada para que el usuario ingrese una letra
        self.entryLetter = tk.Entry(root)
        self.entryLetter.pack()

        # Botón para adivinar una letra
        self.buttonGuess = tk.Button(root, text="ADIVINAR", command=self.guessLetterHandler)  # Cambié guessLetter a guessLetterHandler
        self.buttonGuess.pack()

        # Etiqueta para mostrar el estado del juego
        self.labelStatus = tk.Label(root, text="Introduzca la letra:")
        self.labelStatus.pack()

    def updateImage(self):
        """Actualiza la imagen del ahorcado según la cantidad de intentos fallidos"""
        imagePath = self.game.getCurrentImage()

        if imagePath:
            try:
                # Cargar la imagen y ajustarla al tamaño del canvas
                img = Image.open(imagePath)
                img = img.resize((300, 300), Image.LANCZOS)  # Ajustar el tamaño de la imagen con el filtro adecuado
                self.imgTk = ImageTk.PhotoImage(img)
                # Limpiar el canvas antes de mostrar la nueva imagen
                self.canvas.delete("all")
                self.canvas.create_image(150, 150, image=self.imgTk)  # Centrar la imagen en el canvas
            except Exception as e:
                print(f"Error cargando la imagen: {e}")

    def guessLetterHandler(self):
        """Gestiona el intento de adivinar una letra"""
        letter = self.entryLetter.get().strip().lower()
        self.entryLetter.delete(0, tk.END)

        try:
            # Verifica que el usuario ingrese una letra válida
            if not letter.isalpha() or len(letter) != 1:
                raise ValueError("Introduce una letra válida individual")

            # Llamar a la función de lógica para adivinar la letra
            if self.game.guessLetter(letter):
                self.labelStatus.config(text="¡Correcto!")
            else:
                self.labelStatus.config(text="¡Incorrecto!")
                self.updateImage()

            # Actualizar la palabra mostrada
            self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")

            # Verificar si el juego ha terminado
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
