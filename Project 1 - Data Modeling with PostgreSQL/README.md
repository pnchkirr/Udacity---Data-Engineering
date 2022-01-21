### Introduction

<p>A startup called <strong>Sparkify</strong> wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity in the app, as well as a directory with JSON metadata on the songs in their app.</p>

</p>They'd like a Data Engineer to create a PostgreSQL database with tables designed to optimize queries on song play analysis. They hired me, so my role on this project is to <strong>create a database schema</strong> and <strong>ETL pipeline</strong> for this analysis. To test the database and ETL pipeline I will be running queries given to me by the Analytics Team from Sparkify and compare my results with their expected results.</p>


### Project Brief

<p>In this project, I've applied my freshly gained knowledge on Data Modeling with Postgres and built an ETL Pipeline using Python. I've defined Fact and Dimension tables based on a STAR Database Schema for a particular analytic focus, and created an ETL Pipeline that transfers data from Sparkify app files in two local directories into these tables in Postgres using Python and SQL.</p>

<p>The database I created allows to perform extensive analysis and answer different kinds of questions like:</p>
<ol>
    <li>How many users does Sparkify app have?</li>
    <li>What is the gender ratio (Male to Female)?</li>
    <li>How many premium (paid) users do we have?</li>
    <li>What songs users are listening to?</li>
    <li>Where do Sparkify users located?</li>
    <li>What browsers do Sparkify users run?</li>
    <li>At what time of day (or days of week) are Sparkify users the most active?</li>
</ol>
    

### Database Schema

<p>Here is my database schema design: https://imgur.com/a/LvwuMCB</p>

<p>As you can see from the picture above, I've used a STAR schema to allow Sparkify's Analytics Team to write simple queries (with JOINs), do fast agregations (like COUNT, SUM, AVG, etc.) and be able to denormalize the tables on their will.</p>

<p>The schema includes:</p> 

<p>1 Fact Table</p>
<p>songplays - Contains "factual", raw data gathered by Sparkify app:</p>
<ul>
    <li>songplay_id - Action ID</li>
    <li>start_time - Date and Time of user's action</li>
    <li>user_id - User ID</li>
    <li>level - Type of user's account: free or paid</li>
    <li>song_id - Song ID</li>
    <li>artist_id - Artist ID</li>
    <li>session_id - User's session ID</li>
    <li>location - User's location where the action was recorded</li>
    <li>user_agent - User's browser</li>
</ul>

<p>4 Dimension Tables</p>
<p>time - Contains timestamps from songplays table broken down by its' components:</p>
<ul>
    <li>start_time - Date and Time of user's action</li>
    <li>hour - Hour value extracted from start_time</li>
    <li>day - Day value extracted from start_time</li>
    <li>week - Week value extracted from start_time</li>
    <li>month - Month value extracted from start_time</li>
    <li>year - Year value extracted from start_time</li>
    <li>weekday - Day of week value extracted from start_time</li>
</ul>

<p>users - Contains data about Sparkify users:</p>
<ul>
    <li>user_id - User ID</li>
    <li>first_name - User's first name</li>
    <li>last_name - User's last name</li>
    <li>gender - User's gender</li>
    <li>level - Type of user's account: free or paid</li>
</ul>

<p>songs - Contains data about songs presented in Sparkify:</p>
<ul>
    <li>song_id - Song ID
    <li>title - Song title
    <li>artist_id - Artist ID
    <li>year - Year when the song was released
    <li>duration - Song duration (in seconds)
</ul>

<p>artists - Contains data about songs' artists presented in Sparkify:</p>
<ul>
    <li>artist_id - Artist ID
    <li>name - Artist name
    <li>location - Artist location
    <li>latitude - Artist location's latitude
    <li>longitude - Artist location's longitude
</ul>


### ETL Pipeline

<p>Before we start talking about the ETL pipeline itself, let's first take a look at the data we're dealing with.</p>

<p>Sparkify app provides us with two datasets: song_data and log_data.</p>

<p>song_data - Contains Sparkify songs / artists metadata. Each file is in JSON format and contains data about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset:</p>

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

<p>And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like:</p>

{
"num_songs": 1, 
"artist_id": "ARJIE2Y1187B994AB7", 
"artist_latitude": null, 
"artist_longitude": null, 
"artist_location": "", 
"artist_name": "Line Renaud", 
"song_id": "SOUPIRU12A6D4FA1E1", 
"title": "Der Kleine Dompfaff", 
"duration": 152.92036, 
"year": 0
}

<p>log_data - Consists of log files in JSON format generated by Sparkify app based on the song_data dataset.</p>

<p>The log files are partitioned by year and month. For example, here are filepaths to two files in this dataset.</p>

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

<p>And below is an example of what the data in a log file, 2018-11-12-events.json, looks like:</p>

{
"artist":null,
"auth":"Logged In",
"firstName":"Walter",
"gender":"M",
"itemInSession":0,
"lastName":"Frye",
"length":null,
"level":"free",
"location":"San Francisco-Oakland-Hayward, CA",
"method":"GET",
"page":"Home",
"registration":1540919166796.0,
"sessionId":38,
"song":null,
"status":200,
"ts":1541105830796,
"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
"userId":"39"
}
{
...
}
{
...
}
...

<p>NOTE: The original dataset contains ts column - the data there is represented in TIMESTAMP format. In this project, I've converted this TIMESTAMP into DATETIME format, and uploaded it into both time and songplays tables (start_time column). Considering the fact start_time column is the PRIMARY KEY for time table, and the FOREIGN KEY for songplays table, using the same data type will guarantee the data consistency.</p>

<p>Now, when we have a full picture, let's build a so-called ETL pipeline, starting with some basic definitions.</p>

<p>ETL (stands for Extract-Transform-Load) includes copying data (Extracting) from a certain source(s), changing it (Transforming) in a way so that a destination system will be able to work with it (as it represents the data differently from the source system), and placing it (Loading) into a destination system.</p>

<p>ETL Pipeline is a process that makes ETL constant (regular) and, thus, ensures that all new data generated by a source system(s) will be successfully integrated into a destination system.</p>

<p>Basically, we need to take the data from two datasets provided by Sparkify app (song_data and log_data), and upload it into our Postgres database in a structured manner. To do so, we'll be using Python (pandas library in particular) and SQL.</p>

<p>In scope of this project, we're using a number of files:</p>

<ol>
    <li>sql_queries.py - Contains all the SQL queries: CREATE TABLES, DROP TABLES and INSERT INTO TABLES for our Postgres database</li>
    <li>create_tables.py - Python script we'll be running to drop and create tables. Uses DROP and CREATE SQL statements from sql_queries.py to re-create the database</li>
    <li>*etl.ipynb - Jupyter Notebook file designed to develop ETL processes for each table of our database. Used to prepare a Python script (see etl.py below) for processing all the datasets</li>
    <li>test.ipynb - Jupyter Notebook file with test SQL queries. Used to confirm the successful creation and population of the tables</li>
    <li>etl.py - Python script that contains the ETL pipeline itself. It processes all the files from both datasets (located in /data/song_data and /data/log_data folders), and then loads their content into the database's tables: songs, artists, time, users, songplays</li>
</ol>

<p>* Non-operational file</p>

<p>To avoid duplicating the information, please feel free to examine each of the files listed above to get a full and detailed understanding (all these files contain helpful comments) of how my ETL pipeline works.</p>

#### How to run the ETL pipeline?

<ol>
    <li>Start with (re)creating sparkifydb database and its tables. Open a terminal and type: 'python create_tables.py' to run create_tables.py script.</li>
    <li>Check that all the tables were succesfully created. Launch Jupyter Notebook, open test.ipynb and run SQL queries sequentially.</li>
    <li>Run the ETL pipeline. Open a terminal and type 'python etl.py' to run etl.py script. It will process both song_data and log_data folders and upload the data into all 5 tables in sparkifydb database.</li>
    <li>Check that all the tables were successfully filled with data. Launch Jupyter Notebook, open test.ipynb and run SQL queries sequentially.</li>
</ol>

### Example queries and results for song play analysis

<p>Please refer to example_queries.ipynb.</p>

### Further Development Plan

<p> I'm currently facing tight deadlines on my full-time job as a Data Analyst at Auchan Retail Russia. Unfortunately, I don't have enough time to implement the functionality listed below. As I'd like to return to the project in the nearest future, I'll keep the following plan:</p>

<ol>
    <li>Insert data using the COPY command to bulk insert log files instead of using INSERT on one row at a time</li>
    <li>Add data quality checks</li>
    <li>Create a dashboard for analytic queries on your new database</li>
</ol>