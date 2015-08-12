import logging
import threading
import time

import little_john_brain
import little_john_state
import little_john_worker


LOGGER = logging.getLogger(__name__)


class LittleJohnError(Exception):
    pass


class LittleJohn(object):
    """Little John Main Class"""

    TICK_INTERVAL = 10
    DEFAULT_STATE_CLASS = little_john_state.LittleJohnState

    def __init__(self, worker, brain):
        """Init for LittleJohn with Worker"""
        self.worker = worker
        self.brain = brain
        self.stop_request = threading.Event()
        self.state = LittleJohn.DEFAULT_STATE_CLASS.Create()

    @staticmethod
    def CreateWithGeneratedWorkerWithCredentials(username, password):
        """Create LittleJohn with RobinHood username and password.

        Args:
            username: (string) Robinhood account username.
            password: (string) Robinhood account password.
        """
        worker = little_john_worker.LittleJohnWorker.Create(username, password)
        brain = little_john_brain.LittleJohnBrain()
        return LittleJohn(worker, brain)

    def _UpdateState(self):
        self.worker.UpdateState(self.state)

    def _UpdateDecision(self):
        self.brain.UpdateDecision(self.state)

    def _PerformDecision(self):
        self.worker.PerformDecision(self.state.GetDecision())

    def _LoopWorker(self):
        while not self.stop_request.isSet():
            self._UpdateState()
            self._UpdateDecision()
            self._PerformDecision()
            time.sleep(LittleJohn.TICK_INTERVAL)

    def Loop(self):
        loop_worker = threading.Thread(target=self._LoopWorker)
        loop_worker.start()
        raw_input("Running...\nEnter anything to stop.")
        self.stop_request.set()


def main():
    import getpass
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    lj = LittleJohn.CreateWithGeneratedWorkerWithCredentials(username, password)
    lj.Loop()


if __name__ == "__main__":
    main()
