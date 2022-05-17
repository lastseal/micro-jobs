import sys
sys.path.append('./micro')
import jobs
import time

@jobs.repeat({"every": "10s"}, thread=True)
def test():
    print("hello world")

while True:
    time.sleep(0.1)