import os
from redis import Redis
from rq import Queue, SimpleWorker


def main():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    conn = Redis.from_url(redis_url)
    # Bind queue and worker to the same Redis connection (no Connection ctx needed)
    q = Queue(connection=conn)  # default queue
    # SimpleWorker is Windows-friendly (no fork/wait4)
    worker = SimpleWorker([q], connection=conn)
    worker.work()


if __name__ == "__main__":
    main()

#  ran this in multple reminals so multiple workers spin up -> python -m 10-Rag-Queues.queues.run_worker