
class Hangman:
    def __init__(self, db, player):
        self.db = db
        self.player = player
        self.category = ""
        self.word = ""
        self.attempts = 0
        self.maxAttempts = 8
        self.guessedLetters = []
        self.incorrectLetters = []

    def selectCategory (self, category):
        self.category = category
        self.word = self.db.get_word(category)

        if not self.word:
            raise  ValueError(f"No hay palabra disponible para esta categoría {category}.")

        self.attempts = 0
        self.guessedLetters = ["_"] * len(self.word)
        self.incorrectLetters = []

    def guessLetter (self, letter)
        if not letter.isalpha():
            print("Introduzca un carácter alfabético")
            return False

        if letter != letter.strip():
            print("Introduce solo una letra sin espacios")
            return False

        letter = letter.lower():

        if letter in self.guessedLetters or letter in self.incorrectLetters:
            print("Ya has usado esta letra")
            return False
