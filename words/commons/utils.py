import time


def timer(method):
    def wrapped_func(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        run_time = time.time() - start_time
        print(f"finished {method.__name__!r} in {run_time:.4f} seconds")
        return result
    return wrapped_func




