from pydantic import BaseModel

class ScanJobRequest(BaseModel):
    job_name: str
    git_url: str
    build_path: str
    project_type: str

class GetBuildStatusSchema(BaseModel):
    job_name: str
    build_id: int