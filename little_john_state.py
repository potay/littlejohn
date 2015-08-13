from enum import Enum
import json
import datetime
import logging


LOGGER = logging.getLogger(__name__)


class LittleJohnStateError(Exception):
    pass


class LittleJohnDecision(object):
    """Little John Decision Class

    Attributes:
        type: (LittleJohnDecision.TYPE) The type of decision.
        symbol: (string) Symbol of the instrument.
        bid_price: (float) Bid Price of the decision.
        quantity: (int) Quantity of the decision.
    """

    TYPE = Enum("LittleJohnDecisionStand", [
                "null",
                "stay",
                "buy",
                "sell"])

    def __init__(self):
        self._type = LittleJohnDecision.TYPE.null
        self._symbol = None
        self._bid_price = None
        self._quantity = None
        self._acted_on = False

    @property
    def type(self):
        return self._type.name

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
        """Returns whether decision has been acted on."""
        return self._acted_on

    def SetActed(self):
        """Sets that decision has been acted on."""
        LOGGER.info(
            "Decision acted on. Details: type: %s, symbol: %s, bid price: %f, quantity: %d",
            self.type, self.symbol, self.bid_price, self.quantity)
        self._acted_on = True

    @staticmethod
    def Stay():
        """Creator function that creates a stay decision."""
        decision = LittleJohnDecision()
        decision._SetStayDecision()
        return decision

    @staticmethod
    def Buy(symbol, bid_price, quantity):
        """Creator function that creates a buy decision.

        Args:
            symbol: (string) Symbol of the instrument.
            bid_price: (float) Bid Price of the decision.
            quantity: (int) Quantity of the decision.
        """
        decision = LittleJohnDecision()
        decision._SetBuyDecision(symbol, bid_price, quantity)
        return decision

    @staticmethod
    def Sell(symbol, bid_price, quantity):
        """Creator function that creates a sell decision.

        Args:
            symbol: (string) Symbol of the instrument.
            bid_price: (float) Bid Price of the decision.
            quantity: (int) Quantity of the decision.
        """
        decision = LittleJohnDecision()
        decision._SetSellDecision(symbol, bid_price, quantity)
        return decision

    def _SetDecision(self, decision_type, symbol=None, bid_price=None, quantity=None):
        self._type = decision_type
        self._symbol = symbol
        self._bid_price = bid_price
        self._quantity = quantity

    def _SetStayDecision(self):
        self._SetDecision(LittleJohnDecision.TYPE.stay)

    def _SetBuyDecision(self, symbol, bid_price, quantity):
        self._SetDecision(
            LittleJohnDecision.TYPE.buy,
            symbol, bid_price, quantity)

    def _SetSellDecision(self, symbol, bid_price, quantity):
        self._SetDecision(
            LittleJohnDecision.TYPE.sell,
            symbol, bid_price, quantity)


class LittleJohnInstrument(object):
    """Little John Instrument"""

    def __init__(self, symbol, url, splits, fundamentals, quote, market, position=None):
        self.timestamp = datetime.datetime.now()
        self.symbol = symbol
        self.url = url
        self.splits = splits
        self.fundamentals = fundamentals
        self.quote = quote
        self.market = market
        self.position = position


class LittleJohnState(object):
    """Little John State Class"""

    def __init__(self, instruments):
        self._decision = LittleJohnDecision()
        self.instruments = instruments

    @property
    def decision(self):
        if self._decision.type == "null":
            LOGGER.warning("Decision has not been made.")
            return None
        else:
            return self._decision

    @decision.setter
    def decision(self, decision):
        if self._decision.type == "null":
            self._decision = decision
        else:
            LOGGER.error("Decision has already been made.")

    def __str__(self):
        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        return "Decision: %s, Instruments: %s" % (self._decision.__dict__, ", ".join([json.dumps(instrument.__dict__, default=date_handler, sort_keys=True, indent=4, separators=(',', ': ')) for instrument in self.instruments]))
