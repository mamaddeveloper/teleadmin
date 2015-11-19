import datetime
import json
import logging
import logging.config
import os
import queue
import random
import time
import stoppable_thread


def main():
    LOGGING_PATH = "logs/config.json"
    if os.path.exists(LOGGING_PATH):
        with open(LOGGING_PATH, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.DEBUG)
    q = queue.Queue()
    s = SimulatorWebhook(q)
    b = SimulatorBot(q)
    s.start()
    b.start()
    while True:
        try:
            time.sleep(1000)
        except KeyboardInterrupt:
            break
    s.stop()
    b.stop()
    print("End stop, joning")
    s.join()
    print("s join")
    b.join()
    print("Full stop")


class SimulatorWebhook(stoppable_thread.StoppableThread):
    def __init__(self, queue):
        super(SimulatorWebhook, self).__init__()
        self.queue = queue
        self.logger = logging.getLogger(type(self).__name__)

    def run(self):
        while self.can_loop():
            w = random.randint(3, 6)
            self.logger.info("Wait %d seconds", w)
            time.sleep(w)
            k = "bonjour %s" % datetime.datetime.now()
            self.logger.info("Send '%s'",k)
            self.queue.put_nowait(k)


class SimulatorBot(stoppable_thread.StoppableThread):
    def __init__(self, queue):
        super(SimulatorBot, self).__init__()
        self.queue = queue
        self.logger = logging.getLogger(type(self).__name__)

    def run(self):
        while self.can_loop():
            try:
                self.logger.info("Wait for next")
                k = self.queue.get(timeout=1)
                self.logger.info("Proceed '%s'", k)
                w = random.randint(1, 3)
                self.logger.info("Wait %d seconds", w)
                time.sleep(w)
                self.logger.info("End proceed '%s'", k)
            except queue.Empty:
                pass


if __name__ == '__main__':
    main()
