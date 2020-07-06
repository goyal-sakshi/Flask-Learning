from flask import Flask, request
import redis
from rq import Queue

import time

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def backgroud_task(n):
    delay = 2

    print("Task running")
    print(f"Simulating {delay} second delay")

    time.sleep(delay)

    print(len(n))
    print("Task completed")

    return len(n)


@app.route("/task")
def add_task():
    if request.args.get("n"):

        '''
        when we call q.enqueue, a message is send to Redis and 
        the worker is going to listen, and as soon it gets that, its going to trigger
        '''
        job = q.enqueue(backgroud_task, request.args.get("n"))

        q_len = len(q)

        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in queue"

    else:
        return "No value for n"


if __name__ == '__main__':
    app.run(debug=True)