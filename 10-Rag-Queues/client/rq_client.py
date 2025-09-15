from redis import Redis
from rq import Queue

queue = Queue(connection=Redis(
    host="localhost",
    port="6379"
))

# q.enqueue(process_query)
#  rq worker -w rq.worker.SpawnWorker --url redis://localhost:6379  default