from functools import wraps

class stacklog(object):
    """Stack log messages

    Args:
        method: log callable
        message: log message
        *args: args to log method
        **kwargs: kwargs to log method

    Example usage:

       with stacklog(logging.info, 'Running long function'):
           run_long_function()

       with stacklog(logging.info, 'Running error-prone function'):
           raise Exception

    This produces logging output:

        INFO:root:Running long function...
        INFO:root:Running long function...DONE
        INFO:root:Running error-prone function...
        INFO:root:Running error-prone function...FAILURE
    """

    def __init__(self, method, message, *args, **kwargs):
        self.method = method
        self.message = str(message)
        self.args = args
        self.kwargs = kwargs

    def _log(self, suffix=''):
        self.method(self.message + '...' + suffix, *self.args, **self.kwargs)

    _begin = _log

    def _succeed(self):
        self._log(suffix='DONE')

    def _fail(self):
        self._log(suffix='FAILURE')

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self):
        self._begin()
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._succeed()
        else:
            self._fail()
        return False
