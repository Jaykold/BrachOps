#from pyjen.jenkins import Jenkins
import config
from aiojenkins import Jenkins, jobs, builds, queue

class JenkinsService:

    def __init__(self):
        self.jenkins = Jenkins(config.JENKINS_URL, config.JENKINS_CRED['USERNAME'], config.JENKINS_CRED['PASSWORD'])
        self.job = jobs.Jobs(self.jenkins)
        self.build = builds.Builds(self.jenkins)
        self.queue = queue.Queue(self.jenkins)

    async def get_jenkins_info(self):
        system_info = await self.jenkins.get_status()
        return system_info
    
    async def check_job_exists(self, job_name:str):
        return await self.job.is_exists(job_name)
    
    async def get_build_info(self, job_name:str, build_number:int):
        return await self.build.get_info(job_name, build_number)
    
    async def trigger_job(self, job_name:str):
        queue_item_number = await self.build.start(job_name)
        return queue_item_number
    
    async def create_jenkins_job(self, job_name:str, config_xml):
        await self.job.create(job_name, config_xml)

    async def stop_build(self, job_name:str, build_number:int):
        return await self.build.stop(job_name, build_number)
    
    async def delete_job(self, job_name:str):
        await self.job.delete(job_name)
    
    async def list_jobs(self):
        return await self.job.get_all()
    
    async def create_scan_job(self, job_name:str, config_xml):
        await self.job.create(job_name, config_xml)

    async def get_queue_item(self, queue_item_number:int):
        return await self.queue.get_info(queue_item_number)
    
    async def get_job_with_builds(self, job_name:str):
        return await self.job.get_info(job_name)