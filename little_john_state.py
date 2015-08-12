from enum import Enum
import logging


class LittleJohnStateError(Exception):
    pass


class LittleJohnDecision(object):
    STAND = Enum("LittleJohnDecisionStand",
                 "stay",
                 "buy",
                 "sell")

    def __init__(self):
        self.stand = LittleJohnDecision.STAND.stay
        self.symbol = None
        self.bid_price = None
        self.quantity = None


class LittleJohnState(object):
    """Little John State Class"""

    def __init__(self):
        pass

    @staticmethod
    def Create():
        return LittleJohnState()

    def GetDecision(self):
        return None
