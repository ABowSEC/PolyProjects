# nodes/relay.py
import time
import random
from .node import Node



class RelayNode(Node):
    def __init__(self, name):
        super().__init__(name)

# Random delay for Node
    def process_packet(self,message):
        delay=random.uniform(.05,.2) #50 to 200 ms
        time.sleep(delay)
        timestamp=time.time()
        return message,timestamp
