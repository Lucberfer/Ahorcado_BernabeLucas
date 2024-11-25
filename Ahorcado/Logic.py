import sqlite3
import random
from Ahorcado.Connection import DatabaseConnection

class HangmanGame:
    def __init__(self, dbName="HangmanDB.db"):
        # Initialize the database connection
        self.db = DatabaseConnection(dbName)
        self.db.connect()
        self.db.createTables()
        self.word = ""
        self.category = ""
        self.guessedLetters = []
        self.incorrectLetters = []
        self.attempts = 0
        self.maxAttempts = 9
        self.currentUser = None
        self.imagesURLs = []
        # Load images from the database
        self.loadImages()

    def loadImages(self):
        """Load image URLs from the database in order."""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT url FROM IMAGES ORDER BY id_image ASC")
            self.imageURLs = [row[0] for row in cursor.fetchall()]
            print(f"Imágenes cargadas: {self.imageURLs}")
        except sqlite3.Error as e:
            print(f"Error cargando las imágenes: {e}")

    def addUser(self, userName):
        """Add a new user or load an existing one"""
        conn = self.db.connection
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT id_user FROM USER WHERE name = ?", (userName,))
            user = cursor.fetchone()

            if user:
                self.currentUser = user[0]
                print(f"Jugador {userName} cargado.")
            else:
                cursor.execute("INSERT INTO USER (name) VALUES (?)", (userName,))
                self.db.connection.commit()
                self.currentUser = cursor.lastrowid
                print(f"Jugador {userName} registrado.")
        except sqlite3.Error as e:
            print(f"Error al añadir al jugador: {e}")

    def updateGameStats(self, win):
        """Update the current user's game Win/Loss stats"""
        conn = self.db.connection
        try:
            cursor = conn.cursor()

            if win:
                cursor.execute("UPDATE USER SET win = win + 1 WHERE id_user = ?", (self.currentUser,))
            else:
                cursor.execute("UPDATE USER SET loss = loss + 1 WHERE id_user = ?", (self.currentUser,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error actualizando las estadisticas: {e}")
            conn.rollback()

    def chooseCategory(self, category):
        """Choose a category and randomly select a word from the database."""
        self.category = category
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(f"SELECT t.text FROM THEME t JOIN {category.upper()} c ON t.id_word = c.id_word")
            words = cursor.fetchall()

            if not words:
                print(f"No hay palabras en la categoría: {category}")
                return False

            # Choose a random word
            self.word = random.choice(words)[0]
            self.guessedLetters = ["_"] * len(self.word)  # Initialize with underscores
            self.incorrectLetters = []
            self.attempts = 0
            return True

        except sqlite3.Error as e:
            print(f"Error al seleccionar la palabra: {e}")
            return False

    def guessLetter(self, letter):
        """Process the guessed letter and update the game state."""
        letter = letter.lower()

        # Check if the letter has already been guessed
        if letter in self.guessedLetters or letter in self.incorrectLetters:
            print("Letra ya usada.")
            return False

        # If the letter is in the word, add it to guessedLetters
        if letter in self.word:
            for i, l in enumerate(self.word):
                if l == letter:
                    self.guessedLetters[i] = letter
            return True
        else:
            # If the letter is incorrect, add it to incorrectLetters and increment attempts
            self.incorrectLetters.append(letter)
            self.attempts += 1
            return False

    def getCurrentImage(self):
        """Get the current image URL based on the number of failed attempts"""
        if self.attempts < len(self.imageURLs):
            return self.imageURLs[self.attempts]
        return None

    def isGameOver(self):
        """Check if the game is over."""
        return "_" not in self.getWordDisplay() or self.attempts >= self.maxAttempts

    def getWordDisplay(self):
        """Return the current state of the word with guessed letters revealed."""
        return " ".join([letter if letter in self.guessedLetters else "_" for letter in self.word])

    def resetGame(self):
        """Reset the game state"""
        self.word = ""
        self.category = ""
        self.guessedLetters = []
        self.incorrectLetters = []
        self.attempts = 0