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

## Good to know:
 
**What is Data Warehousing?**

A Data Warehousing (DW) is a process for collecting and managing data from varied sources to provide meaningful business insights. A Data warehouse is typically used to connect and analyze business data from heterogeneous sources. The data warehouse is the core of the BI system which is built for data analysis and reporting.
It is a blend of technologies and components which aids the strategic use of data. It is the electronic storage of a large amount of information by a business that is designed for query and analysis instead of transaction processing. It is a process of transforming data into information and making it available to users in a timely manner to make a difference. You may check this article to know more about Data Warehouse, its Types, Definition & Example.

**How do you create a redshift cluster without using the GUI - by using IAC?**

Infrastructure as Code(IAC) can help avoid cloud deployment inconsistencies, increase developer productivity, and lower costs. Check out the following posts about IaC:
6 best practices to get the most out of IaC
15 Infrastructure as Code tools you can use to automate your deployments
What is AWS CloudFormation and how can it help your IaC efforts?
How AWS CloudFormation Works (and How to Create a Virtual Private Cloud with it)
How do you perform ETL from S3 buckets to Redshift Database?


> **_Your question_**

why the foreign keys should be NON NULL? The previous reviewer send me the suggestion but I don't full understand the necessity. `In songplays table: there should be NOT NULL constraint for user_id and artist_id because they are all foreign keys on this table.
In songs table: There should be NOT NULL for artist_id since it is a foreign key in this table.`