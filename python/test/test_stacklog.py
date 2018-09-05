import logging
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


from stacklog import stacklog


class TestStacklog(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger('test')
        print(id(logger))
        logger.setLevel(logging.DEBUG)
        stream = StringIO()
        handler = logging.StreamHandler(stream=stream)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s:%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger
        self.stream = stream

    def test_decorator(self):
        logger = self.logger
        expected = [
            'Doing foo...',
            'Foo!',
            'Doing foo...DONE',
        ]

        @stacklog(self.logger.info, 'Doing foo')
        def foo():
            self.logger.debug('Foo!')

        self.stream.seek(0)
        for expected_message, actual_line in zip(expected, self.stream):
            self.assertIn(expected_message, actual_line)

    def test_context_manager(self):
        logger = self.logger
        expected = [
            'Doing foo...',
            'Foo!',
            'Doing foo...DONE',
        ]

        with stacklog(self.logger.info, 'Doing foo'):
            self.logger.debug('Foo!')

        self.stream.seek(0)
        for expected_message, actual_line in zip(expected, self.stream):
            self.assertIn(expected_message, actual_line)
