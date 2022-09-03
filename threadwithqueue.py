import logging
from queue import SimpleQueue
from threading import Thread


class ThreadWithQueue(Thread):
    def __init__(self):
        logging.info(f'Init {self.get_name()}')
        self.message_queue: SimpleQueue = SimpleQueue()
        super().__init__()

    def run(self):
        logging.info(f'Run {self.get_name()}')
        super().run()

    def get_name(self):
        return self.__class__.__name__

    def get_message(self, timeout=1):
        message = self.message_queue.get(timeout=timeout)
        logging.info(f'{self.get_name()} got message: {message}')
        return message

