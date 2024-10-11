import xml.sax.saxutils as saxutils

def config_xml(pipeline_script):
    escaped_pipeline_script = saxutils.escape(pipeline_script)
    return f'''<?xml version='1.1' encoding='UTF-8'?>
    <flow-definition plugin="workflow-job@2.40">
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
    <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.87">
    <script>\n{escaped_pipeline_script}</script>
    <sandbox>true</sandbox>
    </definition>
    <triggers/>
    <disabled>false</disabled>
    </flow-definition>
    '''.strip()