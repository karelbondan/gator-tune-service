# Gator Tune Service

This is the service repository for [Gator Tune](https://github.com/karelbondan/gator-tune).

## Foreword

This bot uses pytubefix underneath, hence possible errors relating to YouTube's side is probably coming from pytubefix. Since PoToken is now deprecated, I didn't implent the PoToken alternative. **It is highly recommended not to use your main account** since you can be banned by YouTube.

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

# the domain where this service is hosted
SERVICE_URL=https://monty.rocks
```

© 2025 Karel Bondan © 2025 Unofficial [private] Fazbear Entertainment Discord Server
