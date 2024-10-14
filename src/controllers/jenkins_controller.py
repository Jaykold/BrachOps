import sys
from typing import List 
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.services.jenkins_service import JenkinsService
from utils.exception import CustomException
from utils.logger import logging
from src.helpers.scan_pipeline_generator import ScanPipelineGenerator
from src.helpers.config_xml import config_xml

jenkins_service = JenkinsService()
class JobInfo(BaseModel):
    name: str
    url: str
    color: str

class JenkinsInfo(BaseModel):
    numExecutors: int
    jobs: List[JobInfo]
    url: str

async def check_job_exists_handler(job_name: str) -> bool:
    try:
        return await jenkins_service.check_job_exists(job_name)
    except Exception as e:
        logging.error(f"Error checking if job exists: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while checking job existence") from e
    
async def get_build_status_handler(job_name: str, build_id: int):
    try:
        exists = await jenkins_service.check_job_exists(job_name)
        if not exists:
            raise HTTPException(status_code=404, detail=f"Job '{job_name}' does not exists")
        
        build_info = await jenkins_service.get_build_info(job_name, build_id)

        if not build_info:
            raise HTTPException(status_code=404, detail=f"No build found with ID '{build_id}' for job '{job_name}'")

        relevant_info = {
            "fullDisplayName": build_info.get("fullDisplayName"),
            "number": build_info.get("number"),
            "result": build_info.get("result"),
            "url": build_info.get("url"),
            "duration": build_info.get("duration"),
            "timestamp": build_info.get("timestamp"),
        }
        return JSONResponse(content={"message": relevant_info}, status_code=200)
    except Exception as e:
        logging.error(f"Error getting build status: {e}")
        raise HTTPException(status_code=500, detail="An error occured while retrieving the build status") from e
    
async def create_scan_job_handler(job_name: str, git_url: str, build_path: str, project_type: str) -> None:
    try:
        exists = await jenkins_service.check_job_exists(job_name)
        if exists:
            raise CustomException(f"Job '{job_name}' already exists", "Job already exists")
        
        # Generate pipeline script
        logging.info("Generating pipeline script")
        scan_pipeline_generator = ScanPipelineGenerator(job_name, git_url, build_path, project_type)
        pipeline_script = scan_pipeline_generator.generate()
        xml = config_xml(pipeline_script)
        
        # Create scan job
        logging.info("Creating scan job")
        await jenkins_service.create_scan_job(job_name, xml)
        await jenkins_service.trigger_job(job_name)
        return JSONResponse(content={f"Scan job '{job_name}' created successfully"}, status_code=201)
    except HTTPException as e:
        logging.error(f"Error creating scan job: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the scan job") from e