from pythonjsonlogger import jsonlogger

JSON_LOG_FORMAT = (
    "%(asctime)s %(process)d %(levelname)s %(source)s %(target)s %(message)s"
)

STREAM_LOG_FORMAT = (
    "[%(asctime)s][%(process)d][%(levelname)s][%(source)s:%(target)s] %(message)s"
)


def get_json_formatter():
    return jsonlogger.JsonFormatter(JSON_LOG_FORMAT)


def get_stream_formatter():
    import logging

    return logging.Formatter(STREAM_LOG_FORMAT)
