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
        """Load image URLs from the database"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("SELECT URL FROM IMAGES ORDER BY id_image ASC")
            self.imagesURLs = [row[0] for row in cursor.fetchall()]
            print(f"Images loaded: {self.imagesURLs}")
        except sqlite3.Error as e:
            print(f"Error loading images: {e}")

    def addUser(self, userName):
        """Add a new user to the database or load an existing one"""
        conn = self.db.connection

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_user FROM USER WHERE name = ?", (userName,))
            user = cursor.fetchone()

            if user:
                self.currentUser = user[0]
                print(f"Player {userName} loaded.")
            else:
                cursor.execute("INSERT INTO USER (name) VALUES (?)", (userName,))
                conn.commit()
                self.currentUser = cursor.lastrowid
                print(f"Player {userName} registered.")
        except sqlite3.Error as e:
            print(f"Error adding player: {e}")
            conn.rollback()

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
            print(f"Error updating statistics: {e}")
            conn.rollback()

    def chooseCategory(self, category):
        """Choose a category and randomly select a word from the database"""
        self.category = category
        conn = self.db.connection

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.text FROM THEME t JOIN {} c ON t.id_word = c.id_word""".format(category.upper()))
            words = cursor.fetchall()

            if not words:
                print(f"No words found for category: {category}")
                return False

            # Choose a random word from the list of words
            self.word = random.choice(words)[0]
            self.guessedLetters = ['_'] * len(self.word)
            self.incorrectLetters = []
            self.attempts = 0
            return True

        except sqlite3.Error as e:
            print(f"Error retrieving words for the category: {e}")
            return False

    def guessLetter(self, letter):
        """Process the guessed letter and update the game state"""
        letter = letter.lower()

        # Check if the letter has already been guessed
        if letter in self.guessedLetters or letter in self.incorrectLetters:
            print("Letter already guessed.")
            return False

        # If the letter is in the word, reveal it in the correct positions
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
        if self.attempts < len(self.imagesURLs):
            return self.imagesURLs[self.attempts]
        return None

    def isGameOver(self):
        """Check if the game is over"""
        return self.attempts >= self.maxAttempts or "_" not in self.guessedLetters

    def getWordDisplay(self):
        """Get the current state of the guessed word"""
        return " ".join(self.guessedLetters)

    def resetGame(self):
        """Reset the game state"""
        self.word = ""
        self.category = ""
        self.guessedLetters = []
        self.incorrectLetters = []
        self.attempts = 0