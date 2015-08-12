import logging
import requests
import urllib


LOGGER = logging.getLogger(__name__)


class LittleJohnWorkerError(Exception):
    pass


class LittleJohnWorker(object):
    """Little John Worker Class"""

    _ENDPOINTS = {
        "login": "https://api.robinhood.com/api-token-auth/",
        "investment_profile": "https://api.robinhood.com/user/investment_profile/",
        "accounts": "https://api.robinhood.com/accounts/",
        "ach_iav_auth": "https://api.robinhood.com/ach/iav/auth/",
        "ach_relationships": "https://api.robinhood.com/ach/relationships/",
        "ach_transfers": "https://api.robinhood.com/ach/transfers/",
        "applications": "https://api.robinhood.com/applications/",
        "dividends": "https://api.robinhood.com/dividends/",
        "edocuments": "https://api.robinhood.com/documents/",
        "instruments": "https://api.robinhood.com/instruments/",
        "margin_upgrades": "https://api.robinhood.com/margin/upgrades/",
        "markets": "https://api.robinhood.com/markets/",
        "notifications": "https://api.robinhood.com/notifications/",
        "orders": "https://api.robinhood.com/orders/",
        "password_reset": "https://api.robinhood.com/password_reset/request/",
        "quotes": "https://api.robinhood.com/quotes/",
        "document_requests": "https://api.robinhood.com/upload/document_requests/",
        "user": "https://api.robinhood.com/user/",
        "watchlists": "https://api.robinhood.com/watchlists/",
        "employment": "https://api.robinhood.com/user/employment/",
        "additional_info": "https://api.robinhood.com/user/additional_info/",
        "basic_info": "https://api.robinhood.com/user/basic_info/",
    }

    def __init__(self):
        """Init for LittleJohnWorker"""
        self.session = None
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
        }
        self.username = None
        self.password = None
        self.auth_token = None
        self.accounts = {}
        self._default_account_number = None

    @staticmethod
    def Create(username, password):
        """Little John Worker Creator.

        Args:
            username: (string) Username for Robinhood Account.
            password: (string) Password for Robinhood Account.

        Returns:
            (LittleJohnWorker) Little John Worker object associated with account.
        """
        worker = LittleJohnWorker()
        worker.Start(username, password)
        return worker

    def Start(self, username, password):
        """Start LittleJohnWorker with RobinHood username and password.

        Args:
            username: (string) Robinhood account username.
            passowrd: (string) Robinhood account password.
        """
        self.session = requests.session()
        self.session.headers = self.headers
        self.username = username
        self.password = password
        self._Login()
        self._InitAccount()

    def _Login(self):
        """Attempts to login on robinhood API with credentials.

        Raises:
            LittleJohnWorkerError: If login is unsuccessful.
        """
        data = self._PostToEndpoint(
            "login",
            data={"username": self.username, "password": self.password})
        if "non_field_errors" in data:
            raise LittleJohnWorkerError(", ".join(data["non_field_errors"]))
        self.auth_token = data["token"]
        self.headers["Authorization"] = "Token %s" % self.auth_token

    def _InitAccount(self):
        """Initialize account details."""
        # Get all account information
        accounts = self._GetFromEndpoint("accounts")["results"]
        self.accounts = {account["account_number"]: account for account in accounts}
        self._default_account_number = accounts[0]["account_number"]

    @property
    def default_account(self):
        if self._default_account_number and self._default_account_number in self.accounts:
            return self.accounts[self._default_account_number]
        else:
            return None

    def _PostToUrl(self, url, data):
        data = self.session.post(url, data=data).json()
        if "non_field_errors" in data:
            LOGGER.error(", ".join(data["non_field_errors"]))
            return None
        return data

    def _PostToEndpoint(self, endpoint, data):
        if endpoint in LittleJohnWorker._ENDPOINTS:
            return self._PostToUrl(LittleJohnWorker._ENDPOINTS[endpoint], data=data)
        else:
            return None

    def _GetFromUrl(self, url, params=None):
        data = self.session.get(url, params=params).json()
        if "non_field_errors" in data:
            LOGGER.error(", ".join(data["non_field_errors"]))
            return None
        return data

    def _GetFromEndpoint(self, endpoint, params=None):
        if endpoint in LittleJohnWorker._ENDPOINTS:
            return self._GetFromUrl(
                LittleJohnWorker._ENDPOINTS[endpoint],
                params=params)
        else:
            return None

    def GetPositions(self):
        """Gets All Positions Data from Robinhood API."""
        data = self._GetFromUrl(self.default_account["positions"])
        return data["results"]

    def QueryInstruments(self, query, exact=True):
        """Gets Instruments matching query from Robinhood API.

        Args:
            query: (string) Query to match. Query should relate to symbol.
            exact: (bool) If true, query should be a exact symbol match.

        Returns:
            (dict list) List of instruments data.
        """
        data = self._GetFromEndpoint(
            "instruments",
            params={"query": query.upper()})
        if exact:
            instrument = [result for result in data["results"] if result["symbol"] == query.upper()]
            if len(instrument) == 1:
                return instrument[0]
            else:
                return None
        else:
            return data["results"]

    def GetQuotes(self, *symbols):
        """Returns quotes of the symbols.

        Args:
            *symbols: (string) Symbol of instrument.

        Returns:
            (dict list) List of quote data of instruments.
        """
        data = self._GetFromEndpoint("quotes", params={"symbols": ",".join(symbols)})
        return data["results"]

    def _PlaceOrder(self, transaction, symbol, bid_price=None, quantity=1):
        """Places order via the Robinhood API and returns order data.

        Args:
            transaction: (string) Transaction type. Either "buy" or "sell".
            symbol: (string) Instrument symbol.
            bid_price: (float) Bid price of order.
            quantity: (int) Quantity of stocks of order.

        Returns:
            (dict) Order data.

        Raises:
            LittleJohnWorkerError: If unable to place order.
        """
        if bid_price is None:
            bid_price = self.GetQuotes(symbol)[0]["bid_price"]

        instrument = self.QueryInstruments(symbol, exact=True)
        if instrument is None:
            raise LittleJohnWorkerError("Symbol is not valid. Symbol: %s" % symbol)

        data = {
            "account": urllib.unquote(self.default_account["url"]),
            "instrument": urllib.unquote(instrument["url"]),
            "price": float(bid_price),
            "quantity": quantity,
            "side": transaction,
            "symbol": symbol,
            "time_in_force": "gfd",
            "trigger": "immediate",
            "type": "market"
        }

        order_data = self._PostToEndpoint("orders", data=data)

        if order_data is None:
            raise LittleJohnWorkerError("Unable to place order. | Order: %s | Errors: %s" % (data, ", ".join(order_data["non_field_errors"])))

        return order_data

    def PlaceBuyOrder(self, symbol, bid_price=None, quantity=1):
        """Places a buy order via Robinhood API and returns order data.

        Args:
            symbol: (string) Instrument symbol.
            bid_price: (float) Bid price of order.
            quantity: (int) Quantity of stocks of order.

        Returns:
            (dict) Order data.
        """
        transaction = "buy"
        return self._PlaceOrder(transaction, symbol, bid_price, quantity)

    def PlaceSellOrder(self, symbol, bid_price=None, quantity=1):
        """Places a sell order via Robinhood API and returns order data.

        Args:
            symbol: (string) Instrument symbol.
            bid_price: (float) Bid price of order.
            quantity: (int) Quantity of stocks of order.

        Returns:
            (dict) Order data.
        """
        transaction = "sell"
        return self._PlaceOrder(transaction, symbol, bid_price, quantity)

    def UpdateState(self, state):
        pass

    def PerformDecision(self, decision):
        pass


def main():
    import getpass
    lj = LittleJohnWorker()
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    lj.Start(username, password)
    pprint.pprint(lj.QueryInstruments("GOOG"))
    pprint.pprint(lj.GetQuotes("GOOG", "AAPL", "NFLX"))
    pprint.pprint(lj.GetPositions())


if __name__ == "__main__":
    main()
