import logging
import threading
import time
import functools

def func_1():
    print(1)
    time.sleep(0.5)

def func_2():
    print(2)
    time.sleep(1)


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as err:
            print("EEEEEEEEEEEEEE")
    return wrapper


@error_handler
def main():
    threads_1 = [threading.Thread(target=func_1) for _ in range(4)]
    threads_2 = [threading.Thread(target=func_2) for _ in range(5)]
    print("A")
    for thread in threads_1:
        thread.start()
    for thread in threads_1:
        thread.join()
    print("B")
    raise ValueError
    for thread in threads_2:
        thread.start()
    for thread in threads_2:
        thread.join()
    print("C")

main()
