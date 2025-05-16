import time
import random
from config import DEFAULT_DELAY, JITTER

class Node:
    def __init__(self, name):
        self.name = name

    def process_packet(self, packet):
        delay = DEFAULT_DELAY + random.uniform(0, JITTER)
        time.sleep(delay)  # Simulate network delay
        timestamp = time.time()
        print(f"{self.name} processed packet at {timestamp}")
        return packet, timestamp
