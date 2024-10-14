from fastapi import FastAPI
from src.schema.index import ScanJobRequest, GetBuildStatusSchema
from src.controllers.jenkins_controller import (
    check_job_exists_handler, 
    create_scan_job_handler, 
    get_build_status_handler)


def router(app: FastAPI):
    # Check if job Exists
    @app.get("/jenkins/job/{job_name}/build")
    async def check_job_exists(job_name: str):
        return await check_job_exists_handler(job_name)  # http://localhost:8000/jenkins/job/{my_job}/build

    # Get build status
    @app.get("/jenkins/job/{job_name}/build/{build_id}/status")
    async def get_build_status(job_name:str, build_id: int):
        schema = GetBuildStatusSchema(job_name=job_name, build_id=build_id)
        return await get_build_status_handler(schema.job_name, schema.build_id) # http://localhost:3000/jenkins/job/my_job/build/{build_id}/status

    # Create a scan job and trigger it
    @app.post("/jenkins/job/scan")
    async def create_scan_job(request: ScanJobRequest):
        return await create_scan_job_handler(request.job_name, 
                                             request.git_url, 
                                             request.build_path, 
                                             request.project_type)