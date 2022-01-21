# DROP & CREATE KEYSPACE

drop_keyspace = "DROP KEYSPACE IF EXISTS sparkifydb"
create_keyspace = """CREATE KEYSPACE sparkifydb
WITH REPLICATION = {
    'class': 'SimpleStrategy', 'replication_factor': 1
}
"""

# DROP TABLES

first_table_drop = "DROP TABLE IF EXISTS session_song_details"
second_table_drop = "DROP TABLE IF EXISTS user_session_songs"
third_table_drop = "DROP TABLE IF EXISTS user_songs"

# CREATE TABLES

first_table_create = ("""CREATE TABLE IF NOT EXISTS session_song_details (
    sessionId INT,
    itemInSession INT,
    artist TEXT,
    song TEXT,
    length DOUBLE,
    PRIMARY KEY (sessionId, itemInSession)
    )
""")

second_table_create = ("""CREATE TABLE IF NOT EXISTS user_session_songs (
    userId INT,
    sessionId INT,
    itemInSession INT,
    firstName TEXT,
    lastName TEXT,
    artist TEXT,
    song TEXT,
    PRIMARY KEY ((userId , sessionId),  itemInSession)
    )
""")

third_table_create = ("""CREATE TABLE IF NOT EXISTS user_songs (
    song TEXT,
    userId INT,
    firstName TEXT,
    lastName TEXT,
    PRIMARY KEY ((song),  userId)
    )
""")

# INSERT RECORDS

first_table_insert = ("""INSERT INTO session_song_details 
(sessionId, itemInSession, artist, song, length)
VALUES 
(%s, %s, %s, %s, %s)
""")

second_table_insert = ("""INSERT INTO user_session_songs 
(userId, sessionId, itemInSession, firstName, lastName, artist, song)
VALUES 
(%s, %s, %s, %s, %s, %s, %s)
""")

third_table_insert = ("""INSERT INTO user_songs 
(song, userId, firstName, lastName)
VALUES 
(%s, %s, %s, %s)
""")

# SELECT RECORDS (DATA MODELING QUERIES)

first_table_select = ("""SELECT artist, song, length 
FROM session_song_details
WHERE sessionId = 338 AND itemInSession = 4
""")

second_table_select = ("""SELECT artist, song, firstName, lastName, itemInSession 
FROM user_session_songs
WHERE userId = 10 AND sessionId = 182
""")

third_table_select = ("""SELECT firstName, lastName 
FROM user_songs
WHERE song = 'All Hands Against His Own'
""")

# QUERY LISTS

drop_table_queries = [first_table_drop, second_table_drop, third_table_drop]
create_table_queries = [first_table_create, second_table_create, third_table_create]