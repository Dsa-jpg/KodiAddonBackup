from functools import wraps
from .logging import logged_message
from .config import ERROR_LVL

def log_exceptions(func):
    @wraps(func)  # Zachová název a docstring původní funkce
    def wrapper(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except Exception as e:
            logged_message(f"Exception occured in def {func.__name__} : {e}", ERROR_LVL.LOGWARNING)
            raise
    return wrapper

