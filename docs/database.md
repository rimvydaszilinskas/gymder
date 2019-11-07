# Database setup

We are using PostgreSQL database in the backend.

## Installing Postgres on MacOS

Go to https://postgresapp.com/ and follow the instructions. When installed run the following commands:

```shell
$ psql postgres

CREATE USER gymder WITH PASSWORD 'password';
ALTER ROLE gymder SUPERUSER;
CREATE DATABASE gymder;
GRANT ALL PRIVILEGES ON DATABASE gymder TO gymder;
```

If all done successfully the migrations should run smoothly.

## Installing Postgres on Windows

Go to https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows and download the required version of Postgres and install it via the wizard. When installing the database you will be asked to create a superuser, remember the details for later.

After installation you should have Postgres command line utility available from the Start menu.

Connect to the DB server:

```shell
psql -h <host_name> -U <superuser_username> -d postgres
```

After that create a new user and database for the application to run:

```sql
CREATE USER gymder WITH PASSWORD 'password';
ALTER ROLE gymder SUPERUSER;
CREATE DATABASE gymder;
GRANT ALL PRIVILEGES ON DATABASE gymder TO gymder;
```

If all done successfully the migrations should run smoothly.


## Installing Postgres on Ubuntu

Run the following commands to install Postgres and its dependencies:

```shell
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
```

Start up a terminal with superuser rights and then enter Posgres session from there:

```shell
sudo su - postgres
psql
```

Finally create the user and database for the application:

```sql
CREATE USER gymder WITH PASSWORD 'password';
ALTER ROLE gymder SUPERUSER;
CREATE DATABASE gymder;
GRANT ALL PRIVILEGES ON DATABASE gymder TO gymder;
```

Run migrations to verify you're connected.