

from fastapi import FastAPI, Query, HTTPException
from rq.job import Job
from .client.rq_client import queue
from .queues.worker import process_query


app = FastAPI()


@app.get("/")
def root():
    return {"status": "Server is up and running"}

@app.post("/chat")
def chat(query : str = Query(...,description="The Query of user")):
   job = queue.enqueue(process_query,query)
   return {"status": "queued","job_id" : job.id }
@app.get("/job-status")
def get_result(job_id:str = Query(..., description="Job ID")):
    job = queue.fetch_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    status = job.get_status(refresh=False)
    result = job.return_value() if job.is_finished else None

    return {
        "job_id": job.id,
        "status": status,
        "result": result,
    }
