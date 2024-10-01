import sys
import config
from jenkins import Jenkins
from src.exception import CustomException
from utils.escape_xml import escape_xml
from utils.scan_pipeline_generator import ScanPipelineGenerator
import xml.sax.saxutils as saxutils

class JenkinsHelper:
    def __init__(self, url, username, password):
        self.jenkins = Jenkins(url, username, password)
        self.image_tag = config.DOCKER_REGISTRY_URL
      
    def config_xml(self, pipeline_script):
        escaped_pipeline_script = saxutils.escape(pipeline_script)
        return f'''<?xml version='1.1' encoding='UTF-8'?>
        <flow-definition plugin="workflow-job@2.40">
          <description></description>
          <keepDependencies>false</keepDependencies>
          <properties/>
          <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.87">
            <script>\n{pipeline_script}</script>
            <sandbox>true</sandbox>
          </definition>
          <triggers/>
          <disabled>false</disabled>
        </flow-definition>
        '''.strip()
    
    def create_job(self, name, pipeline_script):
        try:
            config_xml = self.config_xml(pipeline_script)
            self.jenkins.create_job(name, config_xml)
            self.jenkins.build_job(name)
        except Exception as e:
            raise CustomException(e, sys) from e
        
if __name__ == '__main__':
    try:
      server = Jenkins(config.JENKINS_URL, config.JENKINS_CRED['USERNAME'], config.JENKINS_CRED['PASSWORD'])
      project_name = "Test4"
      git_url = "https://github.com/The-CodeINN/quizzie.git"
      build_path = "server/quizzie/quizzie.csproj"
      project_type = ".NET Core"
      jenkins_cred = config.JENKINS_CRED
      jenkins = JenkinsHelper(config.JENKINS_URL, jenkins_cred['USERNAME'], jenkins_cred['PASSWORD'])
      scan_pipeline = ScanPipelineGenerator(project_name, git_url, build_path, project_type)
      pipeline_script = scan_pipeline.generate()
      jenkins.create_job(project_name, pipeline_script)
      config_xml =jenkins.config_xml(pipeline_script)
    except Exception as e:
        raise CustomException(e, sys) from e