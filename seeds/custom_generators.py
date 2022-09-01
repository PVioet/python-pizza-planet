from flask_seeder.generator import Generator
from datetime import datetime


class DateTime(Generator):
    """ Random datetime generator """

    def __init__(self, start=datetime(1970, 1, 1), end=datetime.now(), **kwargs):
        """ Initialize generator

        Arguments:
            start: Minimum date
            end: Maximum date

        """
        super().__init__(**kwargs)
        self.start = start
        self.end = end

    def generate(self):
        """ Generate a random datetime

        Set the start/end attributes prior to calling this method.

        Returns:
            A single random datetime from `start` to `end`.
        """
        return datetime.utcfromtimestamp(self.rnd.uniform(self.start.timestamp(), self.end.timestamp()))
