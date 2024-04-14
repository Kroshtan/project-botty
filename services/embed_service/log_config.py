LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {
            "fmt": "[%(asctime)s] [%(process)s] [%(name)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "std_out_handler": {
            "formatter": "app",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["std_out_handler"],
        "level": "INFO",
    },
    "loggers": {
        "gunicorn": {
            "propagate": True,
        },
        "watchdog": {
            "propagate": False,
        },
    },
}
