"""
This class defines Exceptions raised by this package.
"""


class NoFrameFromVideoStreamException(Exception):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def __str__(self):
        return self.reason
