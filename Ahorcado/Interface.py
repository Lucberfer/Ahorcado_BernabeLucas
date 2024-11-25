import tkinter as tk
from PIL import Image, ImageTk


class HangmanInterface:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        # Set fixed size for the window
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Center the window on the screen
        self.centerWindow(600, 600)

        # Set dark gray background color
        self.root.configure(bg="#2E2E2E")  # Dark gray

        self.root.title("EL AHORCADO")

        # Player name input
        self.labelName = tk.Label(root, text="Introduzca su nombre:", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.labelName.pack()
        self.entryName = tk.Entry(root, bg="#505050", fg="white", insertbackground="white")
        self.entryName.pack()
        self.buttonSetName = tk.Button(root, text="Aceptar", command=self.setPlayerName, bg="#B0B0B0", fg="black")
        self.buttonSetName.pack()

        # Category selection
        self.labelCategory = tk.Label(root, text="Seleccione una categoría:", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.labelCategory.pack()
        self.categoryVar = tk.StringVar(root)
        self.categoryVar.set("Seleccione")  # Default value
        self.dropdownCategory = tk.OptionMenu(root, self.categoryVar, "FRUIT", "NAME", "IT")
        self.dropdownCategory.config(bg="#505050", fg="white")
        self.dropdownCategory.pack()
        self.buttonSetCategory = tk.Button(root, text="Elegir Categoría", command=self.setCategory, state=tk.DISABLED, bg="#B0B0B0", fg="black")
        self.buttonSetCategory.pack()

        # Word display
        self.labelWord = tk.Label(root, text="Palabra: ", font=("Helvetica", 16), bg="#2E2E2E", fg="white")
        self.labelWord.pack()

        # Hangman image canvas
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack()

        # Letter input
        self.entryLetter = tk.Entry(root, state=tk.DISABLED, bg="#505050", fg="white", insertbackground="white")
        self.entryLetter.pack()
        self.buttonGuess = tk.Button(root, text="ADIVINA", state=tk.DISABLED, command=self.guessLetterHandler, bg="#B0B0B0", fg="black")
        self.buttonGuess.pack()

        # Status label
        self.labelStatus = tk.Label(root, text="Introduce una letra:", font=("Helvetica", 12), bg="#2E2E2E", fg="white")
        self.labelStatus.pack()

    def centerWindow(self, width, height):
        """Center the window on the screen."""
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        xCoordinate = (screenWidth // 2) - (width // 2)
        yCoordinate = (screenHeight // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{xCoordinate}+{yCoordinate}")

    def setPlayerName(self):
        """Set the player's name and initialize the game."""
        playerName = self.entryName.get().strip()
        if playerName:
            self.game.addUser(playerName)
            self.entryName.config(state=tk.DISABLED)
            self.buttonSetName.config(state=tk.DISABLED)
            self.buttonSetCategory.config(state=tk.NORMAL)
            self.labelStatus.config(text=f"Hola, {playerName}! Selecciona una categoría para empezar a jugar.")
        else:
            self.labelStatus.config(text="Introduce un nombre válido.")

    def setCategory(self):
        """Set the category for the game and initialize the word to guess."""
        category = self.categoryVar.get()
        if category != "Seleccione":
            if self.game.chooseCategory(category):
                self.dropdownCategory.config(state=tk.DISABLED)
                self.buttonSetCategory.config(state=tk.DISABLED)
                self.entryLetter.config(state=tk.NORMAL)
                self.buttonGuess.config(state=tk.NORMAL)
                self.labelStatus.config(text=f"Categoría seleccionada: {category}. ¡Comienza a adivinar letras!")
                # Display initial word with underscores
                self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")
                self.updateImage()  # Ensure that the initial image (no attempts) is displayed
            else:
                self.labelStatus.config(text=f"No se pudo cargar la categoría: {category}")
        else:
            self.labelStatus.config(text="Selecciona una categoría válida.")

    def updateImage(self):
        """Update the hangman image based on the number of failed attempts."""
        imagePath = self.game.getCurrentImage()
        if imagePath:
            try:
                # Load the image and resize it to fit the canvas
                img = Image.open(imagePath)
                img = img.resize((300, 300), Image.LANCZOS)
                self.imgTk = ImageTk.PhotoImage(img)
                # Clear the canvas and display the new image
                self.canvas.delete("all")
                self.canvas.create_image(150, 150, image=self.imgTk)
            except Exception as e:
                print(f"Error cargando la imagen: {e}")

    def guessLetterHandler(self):
        """Handle the attempt to guess a letter."""
        letter = self.entryLetter.get().strip().lower()  # Ensure letter is always lowercase
        self.entryLetter.delete(0, tk.END)

        try:
            # Verify that the user inputs a valid letter
            if not letter.isalpha() or len(letter) != 1:
                raise ValueError("Introduzca una letra válida.")

            # Call the logic function to guess the letter
            if self.game.guessLetter(letter):
                self.labelStatus.config(text="¡Correcto!")
            else:
                self.labelStatus.config(text="¡Incorrecto!")
                self.updateImage()  # Update image on incorrect guess

            # Update the displayed word
            self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")

            # Check if the game is over
            if self.game.isGameOver():
                if "_" not in self.game.getWordDisplay():
                    self.labelStatus.config(text="¡Ganaste!")
                    self.game.updateGameStats(win=True)
                else:
                    self.labelStatus.config(text=f"¡Perdiste! La palabra era: {self.game.word}")
                    self.game.updateGameStats(win=False)
                self.buttonGuess.config(state=tk.DISABLED)

        except ValueError as e:
            self.labelStatus.config(text=f"Error: {e}")
        except Exception as e:
            self.labelStatus.config(text=f"Error inesperado: {e}")
