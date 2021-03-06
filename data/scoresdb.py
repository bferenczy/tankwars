import sqlite3
from contextlib import contextmanager
from collections import namedtuple

Connection = namedtuple("Connection", "db, cursor")
scores_db_name = "scores.db"


class ScoresDB:

    def __init__(self):
        self.scores_db_name = scores_db_name
        self.create_table_if_not_exist()

    def create_table_if_not_exist(self):
        db = None

        try:
            db = sqlite3.connect(self.scores_db_name)
            db.execute(("CREATE TABLE players "
                        "(name TEXT PRIMARY KEY, "
                        "wins INTEGER, "
                        "looses INTEGER)"))
        except sqlite3.OperationalError:
            pass  # Table already exists
        finally:
            if db:
                db.close()

    def save_player_result(self, player_name, is_winner):
        player = self.select_player_by_name(player_name)

        if player:
            if is_winner:
                wins = player['wins'] + 1
                losses = player['looses']
            else:
                wins = player['wins']
                losses = player['looses'] + 1

            update_query = ("UPDATE players "
                            "SET wins=?, looses=?"
                            "WHERE name=?")

            try:
                with self.connect_to_db() as connection:
                    connection.cursor.execute(update_query, (wins, losses, player_name))
                    connection.db.commit()
            except sqlite3.Error:
                print("Cannot update player")

        else:
            insert_player_query = ("INSERT INTO players "
                                   "(name, wins, looses) VALUES (?, ?, ?)")

            try:
                with self.connect_to_db() as connection:
                    if is_winner:
                        connection.cursor.execute(insert_player_query,
                                                  (player_name, 1, 0))
                    else:
                        connection.cursor.execute(insert_player_query,
                                                  (player_name, 0, 1))
                    connection.db.commit()
            except sqlite3.Error:
                print("Cannot save players information")

    def select_player_by_name(self, player_name):
        select_player_query = "SELECT * FROM players WHERE name =?"

        try:
            with self.connect_to_db() as connection:
                connection.cursor.execute(select_player_query, (player_name,))
                player = connection.cursor.fetchone()
        except sqlite3.Error:
            print("Cannot query player from db")

        return dict(player) if player else None

    def select_players(self):
        select_player_query = "SELECT * FROM players"

        try:
            with self.connect_to_db() as connection:
                connection.cursor.execute(select_player_query)
                players = connection.cursor.fetchall()
        except sqlite3.Error:
            print("Cannot query player from db")

        result = list()
        for p in players:
            if p:
                result.append(dict(p))

        return result

    @contextmanager
    def connect_to_db(self):
        db = None
        cursor = None
        try:
            db = sqlite3.connect(self.scores_db_name, detect_types=sqlite3.PARSE_COLNAMES)
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            yield Connection(db, cursor)
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
