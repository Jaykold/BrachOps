from utils import escape_xml

class PipelineGenerator:
    def __init__(self, image_name, project_type):
        self.image_name = image_name
        self.project_type = project_type

    def common_pipeline_stage(self):
        return '''
        stage('Check Docker Image on Docker Hub) {
            steps {
                script {
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                        def imageExistsOnHub = sh(script: "docker manifest inspect ${IMAGE_NAME}", returnStatus: true)
                        if(imageExistsonHub != 0) {
                            error 'Image does not exist on Docker Hub'
                        } else {
                            echo 'Image exists on Docker Hub'
                        }
                    }
                }
            }
        }
        stage('Pull Docker Image') {
            steps {
                scripts{
                    withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                        def imageExistsLocally = sh(script: "docker image inspect ${IMAGE_NAME}", returnStatus: true)
                        if(imageExistsLocally != 0) {
                            echo 'Image does not exist locally, pulling from Docker Hub'
                            sh "docker pull ${IMAGE_NAME}"
                        } else {
                            echo 'Image already exists locally'
                        }
                    }   
                }
            }
        }
        '''.strip()    
    def dot_net_core_pipeline(self):
        return '''
        stage('Deploy Web App To Kubernetes') {
            steps {
                withCredentials([
                    string(credentialsId: 'postgres_user', variable: 'POSTGRES_USER'),
                    string(credentialsId: 'postgres_password', variable: 'POSTGRES_PASSWORD'),
                    string(credentialsId: 'postgres_db', variable: 'POSTGRES_DB'),        
                    string(credentialsId: 'postgres_host', variable: 'POSTGRES_HOST'),
                    string(credentialsId: 'postgres_port', variable: 'POSTGRES_PORT'),
                    string(credentialsId: 'vault_addr', variable: 'VAULT_ADDR'),
                    string(credentialsId: 'vault_token', variable: 'VAULT_TOKEN'),
                    string(credentialsId: 'my_kubernetes', variable: 'api_token')
                ]) {
                    script {
                            sh 'envsubst < infra/k8s/server/deployment.yaml | kubectl --token $api_token --server http://127.0.0.1:45269 --insecure-skip-tls-verify=true apply -f -'
                            sh 'envsubst < infra/k8s/server/service.yaml | kubectl --token $api_token --server http://127.0.0.1:45269 --insecure-skip-tls-verify=true apply -f -'
                    }
                }
            }
        }
        '''.strip()

    def node_js_pipeline(self):
        return '''
        stage('Run Node.js Container') {
            steps {
                withCredentials([
                    string(credentialsId: 'postgres_user', variable: 'POSTGRES_USER'),
                    string(credentialsId: 'postgres_password', variable: 'POSTGRES_PASSWORD'),
                    string(credentialsId: 'postgres_db', variable: 'POSTGRES_DB'),
                    string(credentialsId: 'postgres_host', variable: 'POSTGRES_HOST'),
                    string(credentialsId: 'postgres_port', variable: 'POSTGRES_PORT'),
                    string(credentialsId: 'vault_addr', variable: 'VAULT_ADDR'),
                    string(credentialsId: 'vault_token', variable: 'VAULT_TOKEN')
                ]) {
                    script {
                        withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                            sh "docker run -d -p 8081:8080 ${IMAGE_NAME}"
                        }
                    }
                }
            }
        }
        '''.strip()    
    def generate_pipeline(self):
        common_stage = self.common_pipeline_stage
        project_specific_pipeline = self.dot_net_core_pipeline() if self.project_type == '.NET Core' else self.node_js_pipeline()

        return f'''
        pipeline {{
            agent any
            
            environment {{
                IMAGE_NAME = "{self.image_name}"
            }}
            
            stages {{
                {common_stage}
                {project_specific_pipeline}
            }}
        }}
        '''.strip()