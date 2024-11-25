import sqlite3

class DatabaseConnection:
    def __init__(self, dbName="HangmanDB.db"):
        self.dbName = dbName
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.dbName)
            self.connection.execute("PRAGMA foreign_keys = ON;")
            print("Conexión a la base de datos realizada")
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def close(self):
        """Close the database connection."""
        try:
            if self.connection:
                self.connection.close()
                print("Conexión a la base de datos cerrada")
        except sqlite3.Error as e:
            print(f"Error al cerrar la base de datos: {e}")

    def createTables(self):
        """Create the database tables."""
        try:
            cursor = self.connection.cursor()

            # Create tables
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS USER (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(60) NOT NULL UNIQUE,
                    win INTEGER DEFAULT 0,
                    loss INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS THEME (
                    id_word INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS FRUIT (
                    id_fruit INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_word INTEGER NOT NULL,
                    FOREIGN KEY (id_word) REFERENCES THEME (id_word) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS IT (
                    id_tech INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_word INTEGER NOT NULL,
                    FOREIGN KEY (id_word) REFERENCES THEME (id_word) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS NAME (
                    id_name INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_word INTEGER NOT NULL,
                    FOREIGN KEY (id_word) REFERENCES THEME (id_word) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS IMAGES (
                    id_image INTEGER PRIMARY KEY AUTOINCREMENT,
                    url VARCHAR(60) NOT NULL
                );
            """)

            print("Tablas creadas correctamente.")
            self.insertInitialData(cursor)

        except sqlite3.Error as e:
            print(f"Error creando las tablas o insertando datos: {e}")
            self.connection.rollback()

    def insertInitialData(self, cursor):
        """Insert initial data into the database."""
        try:
            # Insert words for the FRUIT category
            cursor.execute("SELECT COUNT(*) FROM FRUIT")
            if cursor.fetchone()[0] == 0:
                cursor.executescript("""
                    INSERT INTO THEME (text) VALUES
                        ('manzana'), ('platano'), ('uva'), ('mango'), ('kiwi'), 
                        ('naranja'), ('pera'), ('fresa'), ('melocoton'), ('granada');

                    INSERT INTO FRUIT (id_word)
                        VALUES ((SELECT id_word FROM THEME WHERE text = 'manzana')),
                               ((SELECT id_word FROM THEME WHERE text = 'platano')),
                               ((SELECT id_word FROM THEME WHERE text = 'uva')),
                               ((SELECT id_word FROM THEME WHERE text = 'mango')),
                               ((SELECT id_word FROM THEME WHERE text = 'kiwi')),
                               ((SELECT id_word FROM THEME WHERE text = 'naranja')),
                               ((SELECT id_word FROM THEME WHERE text = 'pera')),
                               ((SELECT id_word FROM THEME WHERE text = 'fresa')),
                               ((SELECT id_word FROM THEME WHERE text = 'melocoton')),
                               ((SELECT id_word FROM THEME WHERE text = 'granada'));
                """)

            # Insert words for the IT category
            cursor.execute("SELECT COUNT(*) FROM IT")
            if cursor.fetchone()[0] == 0:
                cursor.executescript("""
                    INSERT INTO THEME (text) VALUES
                        ('python'), ('java'), ('android'), ('debugging'), ('servidor'), 
                        ('mysql'), ('encriptacion'), ('cyberseguridad'), ('frontend'), ('backend');

                    INSERT INTO IT (id_word)
                        VALUES ((SELECT id_word FROM THEME WHERE text = 'python')),
                               ((SELECT id_word FROM THEME WHERE text = 'java')),
                               ((SELECT id_word FROM THEME WHERE text = 'android')),
                               ((SELECT id_word FROM THEME WHERE text = 'debugging')),
                               ((SELECT id_word FROM THEME WHERE text = 'servidor')),
                               ((SELECT id_word FROM THEME WHERE text = 'mysql')),
                               ((SELECT id_word FROM THEME WHERE text = 'encriptacion')),
                               ((SELECT id_word FROM THEME WHERE text = 'cyberseguridad')),
                               ((SELECT id_word FROM THEME WHERE text = 'frontend')),
                               ((SELECT id_word FROM THEME WHERE text = 'backend'));
                """)

            # Insert words for the NAME category
            cursor.execute("SELECT COUNT(*) FROM NAME")
            if cursor.fetchone()[0] == 0:
                cursor.executescript("""
                    INSERT INTO THEME (text) VALUES
                        ('figaro'), ('marta'), ('lucas'), ('elena'), ('rafael'), 
                        ('florencia'), ('angeles'), ('sandra'), ('veronica'), ('sandalio');

                    INSERT INTO NAME (id_word)
                        VALUES ((SELECT id_word FROM THEME WHERE text = 'figaro')),
                               ((SELECT id_word FROM THEME WHERE text = 'marta')),
                               ((SELECT id_word FROM THEME WHERE text = 'lucas')),
                               ((SELECT id_word FROM THEME WHERE text = 'elena')),
                               ((SELECT id_word FROM THEME WHERE text = 'rafael')),
                               ((SELECT id_word FROM THEME WHERE text = 'florencia')),
                               ((SELECT id_word FROM THEME WHERE text = 'angeles')),
                               ((SELECT id_word FROM THEME WHERE text = 'sandra')),
                               ((SELECT id_word FROM THEME WHERE text = 'veronica')),
                               ((SELECT id_word FROM THEME WHERE text = 'sandalio'));
                """)

            # Insert images in IMAGES table
            cursor.execute("SELECT COUNT(*) FROM IMAGES")
            if cursor.fetchone()[0] == 0:
                cursor.executescript("""
                    INSERT INTO IMAGES (url) VALUES
                        ('Resources/img1.png'), ('Resources/img2.png'), ('Resources/img3.png'), 
                        ('Resources/img4.png'), ('Resources/img5.png'), ('Resources/img6.png'), 
                        ('Resources/img7.png'), ('Resources/img8.png'), ('Resources/img9.png');
                """)

            print("Datos iniciales insertados correctamente.")

        except sqlite3.Error as e:
            print(f"Error al insertar datos iniciales: {e}")

