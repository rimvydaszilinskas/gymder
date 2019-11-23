# Setting up development environment

## Before starting

Go to `database.md` file to start up and configure a Postgres database.

## Setting up node

### Ubuntu

```sh
sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt install nodejs
```

Now check if node installed successfuly:

```sh
node -v
```

If no errors will pop up and a version number will apear you have done it successfuly.

### MacOS and Windows

Go to https://nodejs.org/en/download/ and download the appropriate installer. Follow the step by step GUI to install. When asked if `Add to path`, select the feature to be **enabled!**

To test your installation open up a new terminal/command prompt and run the following:

```sh
node -v
```

## Step by step

Clone the repository:

```shell
git clone git@github.com:rimvydaszilinskas/gymder.git gymder-backend
cd gymder-backend
```

Create local variables if you have set up database with other settings than default ones:

```shell
touch .env
echo 'DB_HOST=127.0.0.1' > .env
echo 'DB_PORT=5432' >> .env
echo 'DB_NAME=gymder' >> .env
echo 'DB_USERNAME' >> .env
echo 'DB_PASSWORD' >> .env
```

Link local development settings files to `settings.py`

```shell
ln settings/development.py settings/settings.py
```

Create a virtual environment for the project:

```shell
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate
```

If you're on windows subsitute the last line with:

```
env\scripts\activate.bash
```

Install requirements:

```
pip install -r requirements
```

Run migrations:

```
./manage.py migrate
```

Create a superuser to be able to login to the admin panel:

```
./manage.py createsuperuser
```

The wizard will guide you through creating a superuser.

Finally start an application instance:

```shell
./manage.py runserver
```

If the application started correctly you can now navigate on your browser to `https://localhost:8000/`.


### Setting up React + Webpack

Install the dependencies:

```shell
npm install
```

Finally run the webpack listener on the project:

```shell
npm run watch
```

### Using Google Maps Api

To use Google Maps API add the API KEY to environmental variables:

```shell
echo 'GOOGLE_MAPS_API_KEY=<api_key>' >> .env
```

Replace `api_key` with the key retrieved from GCP.
