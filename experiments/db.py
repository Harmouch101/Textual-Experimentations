import sqlite3
import contextlib


def create_users_table() -> None:
    create_table_query = """
        CREATE TABLE IF NOT EXISTS
            users(
                id integer primary key autoincrement,
                username VARCHAR UNIQUE not null,
                password VARCHAR not null
            )
    """
    # connect to the database
    # using contextlib to avoid connections issues with
    # sqlite when forgetting closing the connection and cursor
    with contextlib.closing(sqlite3.connect("./users.sqlite")) as connection:
        # create a crusor to interract with the database
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute(create_table_query)
            # commit the changes
            connection.commit()

def check_user(username: str, password: str) -> str:
    result = ""
    select_query = """
        SELECT
        *
        FROM
            users
        WHERE
            username = ? 
        AND
            password = ?
    """
    with contextlib.closing(sqlite3.connect("./users.sqlite")) as connection:
        # create a crusor to interract with the database
        with contextlib.closing(connection.cursor()) as cursor:
            cursor.execute(select_query, (username, password))
            # commit the changes
            connection.commit()
            result = cursor.fetchone()
    return result

def register_user(username: str, password: str) -> bool:
    query = """
        INSERT INTO 
            users (
                username
                , password
            )
        VALUES (
                ?
                , ?
            )
    """
    try:
        with contextlib.closing(sqlite3.connect("./users.sqlite")) as connection:
            # create a crusor to interract with the database
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute(query, (username, password))
                # commit the changes
                connection.commit()
        return True
    except:
        return False

if __name__ == "__main__":
    create_users_table()
    register_user("Mahmoud", "password")
    a = check_user('Mahmoud', 'password')
    print(a)