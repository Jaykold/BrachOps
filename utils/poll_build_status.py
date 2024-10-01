import asyncio
import time
from datetime import datetime
from your_service import jenkinsService
from getSonarAnalysisUrl import extractSonarqubeDashboardUrl

async def poll_build_status(job_name: str, build_number: int, timeout: int = 300000) -> str:
    start_time = datetime.now()
    while True:
        status = await jenkinsService.get_build_status(job_name, build_number)
        print("Polling build status...", status['buildInfo']['result'])

        # Check if the build is finished
        if status['buildInfo']['result'] is not None:
            return extractSonarqubeDashboardUrl(status['buildInfo']['actions'])  # Return SonarQube URL when done

        # Wait before polling again
        await asyncio.sleep(7)

        # Check if timeout has been reached
        elapsed_time = (datetime.now() - start_time).total_seconds() * 1000
        if elapsed_time > timeout:
            raise TimeoutError("Timeout waiting for job to start")

# Example usage
# result = asyncio.run(poll_build_status("job_name", 123))
# print(result)
