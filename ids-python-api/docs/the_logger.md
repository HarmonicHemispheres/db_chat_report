# Using the Logger
Logging is builtin to the app and can be configured in the `app.py` model's `start_application` function. The logging configuration is using python's builtin `logging` package. More details about `logging` and `dictConfig` can be found here: https://docs.python.org/3/library/logging.config.html.

<br>

```python
def start_application():
    global CONFIG

    # config for Logging
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",

            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "main-logger": {"handlers": ["default"], "level": "DEBUG"},
        },
    })

    CONFIG = Config()
    CONFIG.load()

    return FastAPI()
```

<br>
<br>
<br>


# Logging to File
...

<br>
<br>

# Logging to Email
...