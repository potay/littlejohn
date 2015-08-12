import logging

import little_john_worker


LOGGER = logging.getLogger(__name__)


class LittleJohnError(Exception):
    pass


class LittleJohn(object):
    """Little John Main Class"""

    def __init__(self, worker):
        """Init for LittleJohn with Worker"""
        self.worker = worker

    @staticmethod
    def CreateWithGeneratedWorkerWithCredentials(username, password):
        """Create LittleJohn with RobinHood username and password.

        Args:
            username: (string) Robinhood account username.
            passowrd: (string) Robinhood account password.
        """
        worker = little_john_worker.LittleJohnWorker.Create(username, password)
        return LittleJohn(worker)


def main():
    import getpass
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    lj = LittleJohn.CreateWithGeneratedWorkerWithCredentials(username, password)


if __name__ == "__main__":
    main()
