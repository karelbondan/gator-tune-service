# Gator Tune Service

This is the service repository for [Gator Tune](https://github.com/karelbondan/gator-tune).

## Foreword

This bot uses pytubefix underneath, hence possible errors relating to YouTube's side is probably coming from pytubefix. Since PoToken is now deprecated, I didn't implent the PoToken alternative. **It is highly recommended not to use your main account** since you can be banned by YouTube.

You also need to setup a webserver to allow streaming to a file on the network. Since I wrote this at 3 am I won't be covering this for you. Good luck, little guy! A heads up would be to search for "nginx view file on the browser"

## Setup

This project uses uv, which can be installed from [the official website](https://docs.astral.sh/uv/getting-started/installation/).

Generating an API key can be done using `secrets`, a built-in Python library, [which was added in version 3.6](https://docs.python.org/3/library/secrets.html). Generating the key could be done using the following set of commands:

```python
>>> import secrets
>>> secrets.token_urlsafe(64)
'R8gHzzzGHUi_MDVTikJKnqcW4AHOy4Bfzd6W_VfKS7207AdqWT-VbVjmenYB97aATR2JsyEgtsyEMa_JVJp6oA'
>>> 
```

**Do not use this example output as your API key**. Run the bot using `uv run poe dev` after you've finished configuring. You will be prompted to connect your account to this bot. It will only prompt you once unless you delete the cache in the .venv folder.

### Example `.env` configuration

```python
# leave as "" if you want to use the default download folder
DOWNLOAD_LOC=""

# see readme on how to generate one
API_KEY=abcdefg

# cors settings - they're basically unused but they're here hehe
ALLOW_ORIGINS=localhost:3000,localhost:4000
ALLOW_METHODS=OPTIONS,GET

# the static file serving endpoint prefix you've configured using your preferred webserver
SERVICE_URL=https://monty.rocks/music/
```

### Docker

Docker configurations were added for ease of use (including for myself). You can change the port on which this service will run through the `docker-compose.yml` file along with other environment variables in the `environment` section. Setting up the service can be done by using the following steps:

1. Run `docker compose up -d --build` inside the directory where this repo is cloned.
2. Wait for docker to finish building the image. It will auto run the container.
3. Output curently running containers with `docker ps`, you should see this service running as something like `gator-tune-service`.
4. Copy the container ID displayed beside the container name, I'll use `c71bae393fc6` as an example.
5. Run `docker logs c71bae393fc6` to view the logs. You should see the OAuth prompt being displayed there. Authenticate using your account.
6. Run `docker attach --detach-keys="ctrl-a" c71bae393fc6`. You should see a blank output. Press `Enter` afterwards. A new set of logs telling the app is now running will be displayed.
7. Detach from the container using `ctrl + a`.

You can restart the container anytime and the auth prompt won't ask you again, similar to how if this service is run without Docker. Do keep in mind if for whatever reason you need to rebuild the image, you will need to redo the steps above to re-authenticate.

© 2025 Karel Bondan © 2025 Unofficial [private] Fazbear Entertainment Discord Server
