import logging
from logging.handlers import TimedRotatingFileHandler
from queue import SimpleQueue
from threading import Thread

import _queue


class ThreadWithQueue(Thread):
    def __init__(self, log_to_file=False):
        self.log = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        self.log.info(f'Init')
        self._message_queue: SimpleQueue = SimpleQueue()

        if log_to_file:
            handler = TimedRotatingFileHandler('log.log', when='midnight', backupCount=30)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.log.addHandler(handler)


        super().__init__()

    def run(self):
        self.log.info(f'Run')
        while True:
            msg = self._get_message()
            if msg:
                if msg[0] == 'DIE':
                    self.log.info(f'Stopping')
                    break
                else:
                    self._handle_message(msg)

    def _handle_message(self, msg):
        raise NotImplementedError('Implement _handle_message')

    def get_message_queue(self):
        return self._message_queue

    def _get_message(self, timeout=6):
        message = None
        try:
            message = self._message_queue.get(timeout=timeout)
            self.log.debug(f'Got message - {message}')
        except _queue.Empty:
            pass
        return message
