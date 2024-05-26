import database

# Connect to the database
connection = database.connect_to_database()

# Create a table
database.execute_query(connection,'''
CREATE TABLE IF NOT EXISTS Pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL
)
'''
)

database.execute_query(connection,'''
CREATE TABLE IF NOT EXISTS Type (
    name VARCHAR(255) PRIMARY KEY
)
''')

database.execute_query(connection,'''
CREATE TABLE IF NOT EXISTS PokemonType (
    pokemon_id INT,
    type_name VARCHAR(255),
    PRIMARY KEY (pokemon_id, type_name),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
    FOREIGN KEY (type_name) REFERENCES Type(name)
)
''')



database.execute_query(connection,'''
CREATE TABLE IF NOT EXISTS Trainer (
    name VARCHAR(255) PRIMARY KEY,
    town VARCHAR(255) NOT NULL
)
''')

database.execute_query(connection,'''
CREATE TABLE IF NOT EXISTS Ownership (
    trainer_name VARCHAR(255),
    pokemon_id INT,
    type_name VARCHAR(255),
    PRIMARY KEY (trainer_name, type_name),
    FOREIGN KEY (trainer_name) REFERENCES Trainer(name),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
    FOREIGN KEY (type_name) REFERENCES Type(name)
    
)
''')

database.close_connection(connection)