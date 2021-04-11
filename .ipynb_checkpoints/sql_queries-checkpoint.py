import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_evets"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (artist varchar, 
                                                                            auth varchar, 
                                                                            firstName varchar, 
                                                                            gender varchar, 
                                                                            itemInSession int, 
                                                                            lastName varchar, 
                                                                            length numeric, 
                                                                            level varchar, 
                                                                            location varchar, 
                                                                            method varchar, 
                                                                            page varchar, 
                                                                            registration varchar, 
                                                                            sessionid int, 
                                                                            song varchar, 
                                                                            status int, 
                                                                            ts numeric, 
                                                                            userAgent varchar, 
                                                                            userId int)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (artist_id varchar, 
                                                                           artist_latitude varchar, 
                                                                           artist_location varchar, 
                                                                           artist_logitude varchar, 
                                                                           artist_name varchar, 
                                                                           duration NUMERIC, 
                                                                           num_songs int, 
                                                                           song_id varchar, 
                                                                           title varchar, 
                                                                           year int)
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id varchar PRIMARY KEY, start_time varchar, user_id varchar NOT NULL, level varchar, song_id varchar NOT NULL, artist_id varchar, session_id varchar, location varchar, user_agent varchar)
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id varchar PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL, year int, duration NUMERIC)
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude varchar, longitude varchar)
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time varchar PRIMARY KEY, hour varchar, day varchar, week varchar, month varchar, year int, weekday int)
""")

# STAGING TABLES

staging_events_copy = ("""COPY staging_events FROM {}
                          credentials 'aws_iam_role={}'
                          region 'us-west-2'
                          format as json {};
""").format(LOG_DATA,IAM_ROLE,LOG_JSONPATH)


staging_songs_copy = ("""COPY staging_songs FROM {}
                         credentials 'aws_iam_role={}'
                         region 'us-west-2'
                         json 'auto'
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (songplay_id, 
                                                   start_time, 
                                                   user_id, 
                                                   level, 
                                                   song_id, 
                                                   artist_id, 
                                                   session_id, 
                                                   location, 
                                                   user_agent) 
                            SELECT ROW_NUMBER() OVER (ORDER BY e.ts),
                                   DISTINCT e.ts,
                                   e.userid,
                                   e.level,
                                   s.song_id,
                                   s.artist_id,
                                   e.sessiongid,
                                   e.location,
                                   e.userAgent
                                FROM staging_events e,
                                 JOIN staging_songs s
                              ON e.song = s.title AND e.length = s.duration
                              WHERE e.page = 'NextSong'                   
""")

user_table_insert = ("""INSERT INTO users (user_id, 
                                           first_name, 
                                           last_name, 
                                           gender, 
                                           level) 
                            SELECT e.userid,
                                   e.firstName,
                                   e.lastName,
                                   e.gender,
                                   e.level
                    
                              FROM staging_events e
                    
""")

song_table_insert = ("""INSERT INTO songs (song_id, 
                                           title, 
                                           artist_id, 
                                           year, 
                                           duration) 
                             SELECT s.song_id,
                                    s.title,
                                    s.artist_id,
                                    s.year,
                                    s.duration
                               FROM staging_songs s
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, 
                                               name, 
                                               location, 
                                               latitude, 
                                               longitude) 
                             SELECT s.artist_id,
                                    s.artist_name,
                                    e.location,
                                    e.latitude,
                                    e.longitude
                              FROM staging_songs s,
                                   staging_events e
                                WHERE s.title = e.song
""")

time_table_insert = ("""INSERT INTO time (start_time, 
                                          hour, 
                                          day, 
                                          week, 
                                          month, 
                                          year, 
                                          weekday) 
                            SELECT DISTINCT e.ts,
                                   EXTRACT(hour FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms")),
                                   EXTRACT(day FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms")),
                                   EXTRACT(week FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms")),
                                   EXTRACT(month FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms")),
                                   EXTRACT(year FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms")),
                                   EXTRACT(weekend FROM TIMESTAMP TO_TIMESTAMP(e.ts, unit="ms"))
                                   
                                   
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
