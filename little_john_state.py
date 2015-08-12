from enum import Enum
import logging


LOGGER = logging.getLogger(__name__)


class LittleJohnStateError(Exception):
    pass


class LittleJohnDecision(object):
    pass


class LittleJohnState(object):
    """Little John State Class"""

    def __init__(self):
        pass

    @staticmethod
    def Create():
        return LittleJohnState()

    def GetDecision(self):
        return None
