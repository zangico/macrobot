import contextvars
import logging

source_var = contextvars.ContextVar("source", default="be")
target_var = contextvars.ContextVar("target", default="worker")


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.source = source_var.get()
        record.target = target_var.get()
        return True


def set_log_context(source=None, target=None):
    if source is not None:
        source_var.set(source)
    if target is not None:
        target_var.set(target)
