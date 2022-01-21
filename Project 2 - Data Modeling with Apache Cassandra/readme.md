- Project: Data Modeling with Cassandra -

INTRODUCTION

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra (NoSQL) database which can create queries on song play data to answer the questions. They hired me, so my role on this project is to create a database and ETL pipeline for this analysis. To test my output I will be running queries given to me by the Analytics Team from Sparkify.


PROJECT BRIEF

In this project, I've applied my freshly gained knowledge on Data Modeling with Apache Cassandra and built an ETL pipeline using Python. I've created a NoSQL database (Apache Cassandra) and three tables modeled on the queries provided by the Analytics Team, and created an ETL pipeline that first combines data from Sparkify app CSV files, located within a single directory, and then inserts it into the Apache Cassandra database tables using Python and CQL.   

The database I created is originally intended to answer the following questions (each of them represents a separate SELECT query):
   1. Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4.
   2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182.
   3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'.


DATABASE SCHEMA

The NoSQL database called sparkifydb includes 3 tables modeled on the queries:

1. 
    Query (text): Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4
    Table: session_song_details - contains song data (artist name, song name, song length) broken down by session ID / item (song number) in session
    Columns:
        sessionId [INT] - Session ID
        itemInSession [INT] - Song number per session
        artist [TEXT] - Artist name
        song [TEXT] - Song name
        length [DOUBLE] - Song duration
    PRIMARY KEY: (sessionId, itemInSession) 
        PARTITION KEY: sessionId, itemInSession
        CLUSTERING COLUMN(S): -
     PK Justification: According to the query we're modeling the table on, we need to include these two columns in the WHERE statement. These two columns uniquely identify all the other columns included in the table. There is no need to include any clustering columns as there can be only one resulting row for each sessionId / itemItSession pair. So we don't need to sort anything.
     Query (code): SELECT artist, song, length FROM session_song_details WHERE sessionId = 338 AND itemInSession = 4

2. 
    Query (text): Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
    Table: user_session_songs - contains user (first name and last name) and song data (artist name and song name) broken down by user ID / session ID
    Columns:
        userId [INT] - User ID 
        sessionId [INT] - Session ID
        itemInSession [INT] - Song number per session
        firstName [TEXT] - User's first name
        lastName [TEXT] - User's last name
        artist [TEXT] - Artist name
        song [TEXT] - Song name
    PRIMARY KEY: ((userId , sessionId),  itemInSession)
        PARTITION KEY: userId , sessionId
        CLUSTERING COLUMN(S): itemInSession
    PK Justification: According to the query we're modeling the table on, we need to include userId and sessionId columns in the WHERE statement. Though these two columns may represent a Partition Key (which, in turn, will determine how data is split between the database clusters), they're not enough to make the Primary Key unique. To fix that, we need to include one more column in the Primary Key - itemInSession. The query above requests the data to be sorted by itemInSession, so it makes this column a good Clustering Column candidate. 
    Query (code): SELECT artist, song, firstName, lastName, itemInSession FROM user_session_songs WHERE userId = 10 AND sessionId = 182

3. 
    Query (text): Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
    Table: user_songs - contains user (first name and last name) data broken down by song name
    Columns:
        song [TEXT] - Song name
        userId [INT] - User ID
        firstName [TEXT] - User's first name
        lastName [TEXT] - User's last name
    PRIMARY KEY: ((song),  userId)
        PARTITION KEY: song
        CLUSTERING COLUMN(S): userId
    PK Justification: According to the query we're modeling the table on, we need to include song column in the WHERE statement. Though this column may represent a Partition Key, it's not enough to make the Primary Key unique (because a single song can be listened to by many users). To fix that, we need to include one more column in the Primary Key - userId. It will make the Primary Key uniquely identify each song 'listening'.
    Query (code): SELECT firstName, lastName FROM user_songs WHERE song = 'All Hands Against His Own'


ETL PIPELINE

Before we start talking about the ETL pipeline itself, let's first take a look at the data we're dealing with.

Sparkify app provides us with the following dataset: event_data. It consists of log files in CSV format generated by Sparkify app. Each log file includes data for a single day. 
For example, here are filepaths to two files in the dataset:

event_data/2018-11-01-events.csv
event_data/2018-11-02-events.csv

And below is an example of what a single file, 2018-11-01-events.csv, looks like:

artist | auth      | firstName | gender | itemInSession | lastName | length | level | location | method | page     | registration | sessionId | song    | status | ts            |userId
BEP    | Logged In | Walter    | M      | 0             | Frye     |        | free  |          | PUT    | NextSong | 1.54092E+12  | 38        | Pump It | 200    | 1.54111E+12   |8
...

Now, when we have a full picture, let's build a so-called ETL pipeline, starting with some basic definitions.

ETL (stands for Extract-Transform-Load) includes copying data (Extracting) from a certain source(s), changing it (Transforming) in a way so that a destination system will be able to work with it (as it represents the data differently from the source system), and placing it (Loading) into a destination system.

ETL Pipeline is a process that makes ETL constant (regular) and, thus, ensures that all new data generated by a source system(s) will be successfully integrated into a destination system.

Basically, we need to take the data from the dataset provided by Sparkify app (event_data), and upload it into our Apache Cassandra database in a structured manner. To do so, we'll be using Python and SQL.

In scope of this project, we're using a number of files:

    - cql_queries.py - Contains all the CQL queries: DROP / CREATE KEYSPACE, DROP / CREATE TABLES, INSERT INTO tables, SELECT FROM tables for our Apache Cassandra database
    - drop_create_tables.py - Contains 2 functions: drop_tables and create_tables to bulk DROP / CREATE all the 3 tables by using DROP and CREATE CQL queries from cql_queries.py. Used by etl.ipynb
    - *project_template.ipynb - Jupyter Notebook file designed to develop and debug the ETL pipeline. Used to prepare another Jupyter Notebook file (see etl.ipynb below) with the actual ETL pipeline
    - etl.ipynb - Jupyter Notebook file that contains the ETL pipeline itself as well as Data Validity checks (all three SELECT queries). First, it processes all the files the dataset (located in /event_data folder), merges their contents into a single file (event_datafile_new.csv), creates a database with three tables, and then loads the combined file contents into the database tables: session_song_details, user_session_songs, user_songs. After that, it's possible to check the tables by executing the SELECT queries for which these tables were modeled on.
    - functions.py - Contains the function for preprocessing the log files from the dataset and combining them into a single one (event_datafile_new.csv). Used by etl.ipynb
* Non-operational file

To avoid duplicating the information, please feel free to examine each of the files listed above to get a full and detailed understanding (all these files contain helpful comments) of how the ETL pipeline works.


HOW TO RUN THE PROJECT?

The only file you need to interact with is etl.ipynb. Open it and run the code snippets in the order they follow each other.

The file conists of 3 parts:

    - Part I. ETL Pipeline: Pre-Processing the files (EXTRACT + TRANSFORM)
    This part is responsible for processing the log files from the dataset and combining them into a single file.
    
    - Part II. ETL Pipeline: Creating and Filling the Apache Cassandra Database (TRANSFORM + LOAD)
    In this part we create the database with 3 tables and then fill them with the data from the Part I combined file.
    
    - Part III. Data Verification.
    Here we do all the checks to make sure the data is integrated into the tables as well as the original SELECT queries give us the result we'd like to see.
    After that, we delete all the tables and close the session and cluster connection.