from contextlib import contextmanager


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass
