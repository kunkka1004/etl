from datetime import datetime
import time

from core.extraction import APIBaseExtraction
from core.datalake import DataLake
from core.transformation import Transformation
from core.const import *


def run():
    now = int(datetime.now().timestamp())
    node1= APIBaseExtraction(timestamp=now)
    node2 = Transformation(timestamp=now)
    node3 = DataLake(timestamp=now)
    exec_list = [node1, node2, node3]
    for node in exec_list:
        node.process()





if __name__ == '__main__':
    while True:
        run()
        time.sleep(INTERVAL)
