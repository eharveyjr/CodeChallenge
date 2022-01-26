# StockXCodeChallenge
Code Challenge for DE role with StockX

## Setup Python3 Environment

There is a system level version of python that comes default on a macbook that is usually python2. You will need to install python3 to run this script. See Below Dependencies:
```
$ brew install python3
$ brew install pip # only if python3 installation doesnt cover this
$ pip install boto3
$ pip install pandas
```

## Setup AWS

Before running the script you will need to have awscli installed and export your AWS credentials to your environment. You will do this by:
```
$ brew install awscli

$ export AWS_ACCESS_KEY_ID=<key>
$ export AWS_SECRET_ACCESS_KEY=<key>
```

## Run Script

Once you run the script it will prompt for user input such as the city, start date & end date. The start date and end date specify a range of days, this script works for 7 consecutive days.
```
$ python3 main.py

<<<OUTPUT>>>
Enter the city name (leave blank to default to Detroit): <US_CITY> # input city name here or press enter for Detroit (Default)
Enter Start Date yyyy-mm-dd: <start date of your choice> #input the date or press enter for today's date
Enter End Date yyyy-mm-dd: <end date of your choice> #input the date or press enter for today's date

```

## View API Call Response File in S3

Now you can check for and download the data files such as Detroit.csv from the public S3 bucket. Make sure to follow the "Setup AWS" step first, then try the commands below. 
```
$ aws s3 ls public-weather-cities/cities/ 
# this will allow you to see the weather files (ex. Detroit.csv) with the data from the API.

$ aws s3 cp s3://public-weather-cities/cities/<US_CITY>.csv /local/path<US_CITY>.csv 
# this will allow you to download the csv file to your local machine from the AWS S3 Bucket.

```

## Load Redshift Table from S3 
Here are instructions on how to copy the data.csv file from the AWS S3 Bucket to AWS Redshift. There are various ways to load data into AWS Redshift, we will use the COPY method. Assuming we already have a cluster, database, schema & table (Weather) configured we can start the data copy to the table. Below we include a IAM role with proper credentials that can access the bucket to satisfy the required authentication parameter. All this can be done once logged into the Redshift cluster and database.
This will load the table with the data from the csv file and now you can query
`select * from pubilc.weather_daily_table order by dt, name;`
```
copy weather_daily_table
from 's3://public-weather-cities/cities/Detroit.csv'
aws_iam_role=arn:aws:iam::<aws-account-id>:role/<role-name>'
csv
NULL as ‘\000’;
```
Further copy details can be found [here](https://docs.aws.amazon.com/redshift/latest/dg/t_loading-tables-from-s3.html) and there's a full article on loading data from S3 to redshift [here](https://www.sqlshack.com/load-data-into-aws-redshift-from-aws-s3/).
