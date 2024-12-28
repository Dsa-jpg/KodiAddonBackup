import os
import sqlite3
import xbmc

class SQlLiteDatabase:

    def __init__(self, db_path: str):
        self.db_path = db_path
        xbmc.log(f"Initializing SQLite Database with path: {db_path}", level=xbmc.LOGINFO)
        
        # Ověření adresáře a vytvoření, pokud neexistuje
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            xbmc.log(f"Creating directory: {db_dir}", level=xbmc.LOGINFO)
            os.makedirs(db_dir)
        
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            xbmc.log("Database connection successful.", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Error connecting to database: {e}", level=xbmc.LOGERROR)

    def create_movie_cache_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS movie_cache (
                    tmdb_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    year INTEGER,
                    overview TEXT,
                    poster_url TEXT,
                    inserted_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
            xbmc.log("Movie cache table created or already exists.", level=xbmc.LOGINFO)
        except sqlite3.OperationalError as e:
            xbmc.log(f"Error creating movie cache table: {e}", level=xbmc.LOGERROR)
        except Exception as e:
            xbmc.log(f"Unexpected error while creating table: {e}", level=xbmc.LOGERROR)

    def get_movie_from_cache(self, tmdb_id):
        try:
            self.cursor.execute('''
                SELECT title, year, overview, poster_url FROM movie_cache WHERE tmdb_id = ?
            ''', (tmdb_id,))
            result = self.cursor.fetchone()
            xbmc.log(f"Movie fetched from cache: {result}", level=xbmc.LOGINFO)
            return result
        except Exception as e:
            xbmc.log(f"Error fetching movie from cache: {e}", level=xbmc.LOGERROR)
            return None

    def add_movie_to_cache(self, tmdb_id, title, year, overview, poster_url):
        try:
            self.cursor.execute('''
                INSERT INTO movie_cache (tmdb_id, title, year, overview, poster_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (tmdb_id, title, year, overview, poster_url))
            self.connection.commit()
            xbmc.log(f"Movie added to cache: {title} ({year})", level=xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"Error adding movie to cache: {e}", level=xbmc.LOGERROR)

    def close(self):
        if self.connection:
            self.connection.close()
            xbmc.log("Database connection closed.", level=xbmc.LOGINFO)
