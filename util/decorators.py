import time


def time_measuring_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        print(f"Time taken to finish {func.__name__} is {time.time() - start_time}")
        return res
    return wrapper
