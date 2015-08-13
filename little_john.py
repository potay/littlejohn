import json
import logging
import sys
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

    TICK_INTERVAL = 10.0
    DOTS_NUM = 10
    DEFAULT_STATE_CLASS = little_john_state.LittleJohnState

    def __init__(self, worker, brain):
        """Init for LittleJohn with Worker"""
        self.worker = worker
        self.brain = brain
        self.stop_request = threading.Event()
        self.state_history = []
        self.state = None

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
        state = self.worker.GetState()
        LOGGER.info("Updating State. State: %s", state)
        self.state_history.append(state)
        self.state = state

    def _UpdateDecision(self):
        LOGGER.info("Updating Decision.")
        self.brain.UpdateDecision(self.state)

    def _PerformDecision(self):
        LOGGER.info("Performing Decision.")
        self.worker.PerformDecision(self.state.decision)

    def _LoopWorker(self):
        while not self.stop_request.isSet():
            self._UpdateState()
            self._UpdateDecision()
            self._PerformDecision()
            time_left = LittleJohn.TICK_INTERVAL
            sys.stdout.write("[" + " " * LittleJohn.DOTS_NUM + "]\b" + "\b" * LittleJohn.DOTS_NUM)
            sys.stdout.flush()
            while time_left > 0:
                sys.stdout.write(".")
                sys.stdout.flush()
                time_left -= LittleJohn.TICK_INTERVAL/10
                time.sleep(LittleJohn.TICK_INTERVAL/10)
            sys.stdout.write("\r")
            sys.stdout.flush()

    def Loop(self):
        loop_worker = threading.Thread(target=self._LoopWorker)
        loop_worker.start()
        raw_input("Running...\nPress 'Enter' to stop.\n")
        self.stop_request.set()
        print "Quitting..."


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log", action="store_true", help="Turn on logging output.")
    args = parser.parse_args()

    if args.log:
        LOGGER.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        LOGGER.addHandler(ch)
        little_john_state.LOGGER.addHandler(ch)

    import getpass
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    lj = LittleJohn.CreateWithGeneratedWorkerWithCredentials(username, password)
    lj.Loop()


if __name__ == "__main__":
    main()
