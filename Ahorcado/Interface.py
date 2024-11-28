import tkinter as tk
from PIL import Image, ImageTk


class HangmanInterface:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        # Set fixed size for the window
        self.root.geometry("650x850")
        self.root.resizable(False, False)

        # Center the window on the screen
        self.centerWindow(650, 850)

        # Set soft background color
        self.root.configure(bg="#1E1E2F")  # Dark background

        self.root.title("EL AHORCADO")

        # Title
        self.labelTitle = tk.Label(
            root,
            text="EL AHORCADO",
            font=("Helvetica", 24, "bold"),
            bg="#1E1E2F",
            fg="#FFDD57"
        )
        self.labelTitle.pack(pady=20)

        # Player name input
        self.labelName = tk.Label(
            root,
            text="👤 Introduzca su nombre:",
            font=("Helvetica", 14),
            bg="#1E1E2F",
            fg="white"
        )
        self.labelName.pack(pady=5)

        self.entryName = tk.Entry(
            root,
            bg="#33334D",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 12),
            width=30
        )
        self.entryName.pack()

        self.buttonSetName = tk.Button(
            root,
            text="Aceptar",
            command=self.setPlayerName,
            bg="#FFDD57",
            fg="black",
            font=("Helvetica", 12),
            relief="flat",
            width=15
        )
        self.buttonSetName.pack(pady=10)

        # Category selection
        self.labelCategory = tk.Label(
            root,
            text="📂 Seleccione una categoría:",
            font=("Helvetica", 14),
            bg="#1E1E2F",
            fg="white"
        )
        self.labelCategory.pack(pady=5)

        self.categoryVar = tk.StringVar(root)
        self.categoryVar.set("Seleccione")  # Default value
        self.dropdownCategory = tk.OptionMenu(
            root,
            self.categoryVar,
            "FRUIT",
            "NAME",
            "IT"
        )
        self.dropdownCategory.config(
            bg="#33334D",
            fg="white",
            font=("Helvetica", 12),
            width=15
        )
        self.dropdownCategory.pack()

        self.buttonSetCategory = tk.Button(
            root,
            text="Elegir Categoría",
            command=self.setCategory,
            state=tk.DISABLED,
            bg="#FFDD57",
            fg="black",
            font=("Helvetica", 12),
            relief="flat",
            width=15
        )
        self.buttonSetCategory.pack(pady=10)

        # Word display
        self.labelWord = tk.Label(
            root,
            text="Palabra: _ _ _ _ _",
            font=("Helvetica", 20),
            bg="#1E1E2F",
            fg="#A1E3FF"
        )
        self.labelWord.pack(pady=20)

        # Hangman image canvas
        self.canvas = tk.Canvas(
            root,
            width=300,
            height=300,
            bg="#1E1E2F",
            highlightthickness=0
        )
        self.canvas.pack()

        # Letter input
        self.entryLetter = tk.Entry(
            root,
            state=tk.DISABLED,
            bg="#33334D",
            fg="white",
            insertbackground="white",
            font=("Helvetica", 14),
            width=5
        )
        self.entryLetter.pack(pady=10)

        self.buttonGuess = tk.Button(
            root,
            text="ADIVINA",
            state=tk.DISABLED,
            command=self.guessLetterHandler,
            bg="#FFDD57",
            fg="black",
            font=("Helvetica", 12),
            relief="flat",
            width=15
        )
        self.buttonGuess.pack()

        # Status label
        self.labelStatus = tk.Label(
            root,
            text="Introduce una letra para empezar",
            font=("Helvetica", 14),
            bg="#1E1E2F",
            fg="#FFDD57"
        )
        self.labelStatus.pack(pady=15)

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
            self.labelStatus.config(text=f"¡Hola, {playerName}! Selecciona una categoría para empezar.")
        else:
            self.labelStatus.config(text="Por favor, introduce un nombre válido.")

    def setCategory(self):
        """Set the category for the game and initialize the word to guess."""
        category = self.categoryVar.get()
        if category != "Seleccione":
            if self.game.chooseCategory(category):
                self.dropdownCategory.config(state=tk.DISABLED)
                self.buttonSetCategory.config(state=tk.DISABLED)
                self.entryLetter.config(state=tk.NORMAL)
                self.buttonGuess.config(state=tk.NORMAL)
                self.labelStatus.config(text=f"Categoría seleccionada: {category}. ¡Empieza a adivinar!")
                self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")
                self.updateImage()
            else:
                self.labelStatus.config(text="No se pudo cargar la categoría.")
        else:
            self.labelStatus.config(text="Selecciona una categoría válida.")

    def updateImage(self):
        """Update the hangman image based on the number of failed attempts."""
        imagePath = self.game.getCurrentImage()
        if imagePath:
            try:
                img = Image.open(imagePath)
                img = img.resize((300, 300), Image.LANCZOS)
                self.imgTk = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                self.canvas.create_image(150, 150, image=self.imgTk)
            except Exception as e:
                print(f"Error cargando la imagen: {e}")

    def guessLetterHandler(self):
        """Handle the attempt to guess a letter."""
        letter = self.entryLetter.get().strip().lower()
        self.entryLetter.delete(0, tk.END)

        try:
            if not letter.isalpha() or len(letter) != 1:
                raise ValueError("Por favor, introduce una letra válida.")

            if self.game.guessLetter(letter):
                self.labelStatus.config(text="¡Correcto!")
            else:
                self.labelStatus.config(text="¡Incorrecto!")
                self.updateImage()

            self.labelWord.config(text=f"Palabra: {self.game.getWordDisplay()}")

            if self.game.isGameOver():
                if "_" not in self.game.getWordDisplay():
                    self.labelStatus.config(text="¡Felicidades, ganaste!")
                    self.game.updateGameStats(win=True)
                else:
                    self.labelStatus.config(text=f"¡Perdiste! La palabra era: {self.game.word}")
                    self.game.updateGameStats(win=False)
                self.buttonGuess.config(state=tk.DISABLED)
        except ValueError as e:
            self.labelStatus.config(text=f"Error: {e}")
        except Exception as e:
            self.labelStatus.config(text=f"Error inesperado: {e}")
