from . import database


def insert_into_ownership(pokemon_name, trainer_name):
    connection = database.connect_to_database()
    try:
        database.execute_query(
            connection,
            """
            INSERT INTO Ownership (trainer_name, pokemon_id)
            SELECT %s, p.id
            FROM Pokemon p
            WHERE p.name = %s
            """,
            (trainer_name, pokemon_name)
        )
        connection.commit()
        return f"Successfully inserted {pokemon_name} for trainer {trainer_name}."
    except Exception as e:
        connection.rollback()
        return f"Failed to insert {pokemon_name} for trainer {trainer_name}: {str(e)}"
    finally:
        connection.close()


def trainer_has_pokemon(trainer_name, pokemon_name):
    connection = database.connect_to_database()
    query = """
    SELECT p.name 
    FROM Pokemon p
    JOIN Ownership o ON o.pokemon_id=p.id 
    WHERE p.name=%s AND o.trainer_name = %s;
    """
    result = database.execute_and_fetch_query(connection, query, (pokemon_name, trainer_name))
    return len(result) != 0



def trainer_exists(trainer_name):
    connection = database.connect_to_database()
    query = """
    SELECT name 
    FROM Trainer 
    WHERE name=%s;
    """
    result = database.execute_and_fetch_query(connection, query, (trainer_name,))
    return len(result) != 0
