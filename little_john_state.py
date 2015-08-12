from enum import Enum
import logging


class LittleJohnStateError(Exception):
    pass


class LittleJohnDecision(Enum):
    STAND = Enum("LittleJohnDecisionStand",
                 "stay",
                 "buy",
                 "sell")

    def __init__(self):
        self._stand = LittleJohnDecision.STAND.stay
        self._symbol = None
        self._bid_price = None
        self._quantity = None
        self._acted_on = False

    @property
    def stand(self):
        return self._stand.name

    @property
    def symbol(self):
        return self._symbol

    @property
    def bid_price(self):
        return self._bid_price

    @property
    def quantity(self):
        return self._quantity

    def IsActed(self):
        return self._acted_on

    def SetActed(self):
        logging.info(
            "Decision acted on. Details: type: %s, symbol: %s, bid price: %s, quantity: %d",
            self.stand, self.symbol, self.bid_price, self.quantity)
        self._acted_on = True

    @staticmethod
    def Stay():
        decision = LittleJohnDecision()
        decision._SetStayDecision()
        return decision

    @staticmethod
    def Buy(symbol, bid_price, quantity):
        decision = LittleJohnDecision()
        decision._SetBuyDecision(symbol, bid_price, quantity)
        return decision

    @staticmethod
    def Sell(symbol, bid_price, quantity):
        decision = LittleJohnDecision()
        decision._SetSellDecision(symbol, bid_price, quantity)
        return decision

    def _SetDecision(self, stand, symbol=None, bid_price=None, quantity=None):
        self._stand = stand
        self._symbol = symbol
        self._bid_price = bid_price
        self._quantity = quantity

    def _SetStayDecision(self):
        self._SetDecision(LittleJohnDecision.STAND.stay)

    def _SetBuyDecision(self, symbol, bid_price, quantity):
        self._SetDecision(
            LittleJohnDecision.STAND.buy,
            symbol, bid_price, quantity)

    def _SetSellDecision(self, symbol, bid_price, quantity):
        self._SetDecision(
            LittleJohnDecision.STAND.sell,
            symbol, bid_price, quantity)


class LittleJohnState(object):
    """Little John State Class"""

    def __init__(self):
        self.decision

    @staticmethod
    def Create():
        return LittleJohnState()

    def GetDecision(self):
        return None
