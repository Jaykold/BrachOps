from fastapi import APIRouter
from src.schema.index import ScanJobRequest, GetBuildStatusSchema
from src.controllers.jenkins_controller import (
    check_job_exists_handler,
    create_scan_job_handler,
    get_build_status_handler,
    get_jenkins_info_handler,
    delete_job_handler)

router = APIRouter(prefix="/jenkins")

# Get jenkins info
@router.get("/info")
async def get_jenkins_info():
    return await get_jenkins_info_handler()

# Check if job Exists
@router.get("/job/{job_name}/build")
async def check_job_exists(job_name: str):
    return await check_job_exists_handler(job_name)  # http://localhost:8000/jenkins/job/{my_job}/build

# Get build status
@router.get("/job/{job_name}/build/{build_id}/status")
async def get_build_status(job_name, build_id):
    schema = GetBuildStatusSchema(job_name=job_name, build_id=build_id)
    return await get_build_status_handler(schema.job_name, schema.build_id) # http://localhost:3000/jenkins/job/{job_name}/build/{build_id}/status

# Create a scan job and trigger it
@router.post("/job/scan")
async def create_scan_job(request: ScanJobRequest):
    return await create_scan_job_handler(request.job_name, 
                                            request.git_url, 
                                            request.build_path, 
                                            request.project_type) # http://localhost:3000/jenkins/job/scan

@router.delete("/job/{job_name}")
async def delete_job(job_name: str):
    return await delete_job_handler(job_name) # http://localhost:3000/jenkins/job/{job_name}