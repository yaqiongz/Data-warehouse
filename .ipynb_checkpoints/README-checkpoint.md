## Build a data warehouse using AWS redshift

In this project, we launched a cloud data warehouse using AWS redshift for a company named spartify. Sparkify is a music app that has a log file contains their user's song play activity in JSON format. We also use a file that contains songs' information. The song's database is called [million song database](http://millionsongdataset.com/).  The files are stored in AWS S3 buckets.


We accomplished the task using the following steps: 
1. Opened an AWS redshift cluster for storing our database.
2. Connecting to the cluster and create the tables. The database was designed using a star schema.
3. transfer the data from the AWS S3 bucket to the staging tables and then insert the data from the staging tables to the database.


`create_tables.py` is the file we run first to connect to Redshift cluster and create the tables.
`dwh.cfg` contains the log-in information for connecting to the redshift cluster, as well as the location that the data was stored in S3.
`etl.py` is the file that copies and transforms the data from S3 to the database in redshift.
`sql_queries.py` contains all the queries we used for creating tables and the ETL process.

## OPTIONAL: Question for the reviewer
 
If you have any question about the starter code or your own implementation, please add it in the cell below. 

For example, if you want to know why a piece of code is written the way it is, or its function, or alternative ways of implementing the same functionality, or if you want to get feedback on a specific part of your code or get feedback on things you tried but did not work.

Please keep your questions succinct and clear to help the reviewer answer them satisfactorily. 

> **_Your question_**
why we the foreign keys should be NON NULL? The previous reviewer send me the suggestion but I don't get it. `In songplays table: there should be NOT NULL constraint for user_id and artist_id because they are all foreign keys on this table.
In songs table: There should be NOT NULL for artist_id since it is a foreign key in this table.`