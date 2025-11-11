## Local Development Setup

These instructions mostly repeat the process scripted in the [Dockerfile](docker-files/Dockerfile), with some minor adjustments for the local development. 

Instructions below assume that they are launched from the repository root

### Building frontend code

These commands are expected to be run from the `frontend` directory.

In order to build the frontend, you need to 
1. Install `node 20.x`. It can be done using [nvm](https://github.com/nvm-sh/nvm)
2. Run `npm install`
3. Run `npm run local:1` to build the frontend code.
4. Run `npm run build:css` to only build the CSS. `local:1` task also runs this command.

It is expected that `frontend/assets/v1/dist` folder will contain the output artifacts.

### Create Python environment
The LMS uses Python 3.10, and there are dependencies that won't work with the newer Python versions out of the box. 
If your local system Python version is different, you can install Python 3.10 using [pyenv](https://realpython.com/intro-to-pyenv/) tool. 

Having installed Python, you need to set up the project with `uv`. Install uv using the [official installer](https://github.com/astral-sh/uv#installation) or `pip install uv`.

Then run `uv sync --extra dev` to create a virtual environment and install all dependencies, including dev packages (it installs django debug toolbar).

All Python commands should be run through `uv run` which automatically uses the project's virtual environment.

### Create and edit a local copy of the environment config
Copy the environment config: `cp lms/settings/.env.example .env`
and fill `AWS.*` variables with some non-empty strings, e.g. `AWS_S3_ACCESS_KEY_ID=asd`

Append the localhost domain name at the end of the file, if you want to access the LMS in dev mode using "localhost:8001" URL:

```
LMS_DOMAIN=localhost
SITE_ID=1
```

### Prepare static files for serving
```
ENV_FILE=.env uv run python manage.py collectstatic --noinput --ignore "webpack-stats-v*.json"
```

### Initialize the database 

Start PostgreSQL in a docker container:
```
docker run -d -p 127.0.0.1:5432:5432 --name lms-postgres -e POSTGRES_USER=csc -e POSTGRES_DB=cscdb -e POSTGRES_PASSWORD=FooBar postgres
```

Start Redis in Docker container: 
```
docker run -d -p 127.0.0.1:6379:6379 --name lms-redis redis:6-alpine redis-server --appendonly yes
```

and apply migrations, that essentially create and initialize the database:
```
ENV_FILE=.env uv run python manage.py migrate
```

### Run the backend in development mode

```
ENV_FILE=.env uv run python manage.py runserver localhost:8001
```

### Run tests

Run tests using pytest through uv:
```
uv run pytest
```

If you want to run tests from some specific folders, append the folder names to the command:
```
uv run pytest apps/core
```

### Testing the JetBrains Academy integration locally

1. Run https://code.jetbrains.team/p/edu/repositories/educational-server locally
2. Set the `SUBMISSION_SERVICE_URL` and `SUBMISSION_SERVICE_TOKEN` variables to the values from the `.env.example` file
3. Enable internal mode in your IDE: https://plugins.jetbrains.com/docs/intellij/enabling-internal.html
4. Install the JetBrains Academy plugin
5. Open any JBA course
6. Use the "Change Submissions Service URL" action to set the URL to `http://localhost:8080`
