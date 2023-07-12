import timeit


def timer(func):
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - start
        return result, elapsed
    return wrapper
