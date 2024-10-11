class ScanPipelineGenerator:
    def __init__(self, job_name: str, git_url: str, build_path: str, project_type: str):
        self.job_name = job_name
        self.git_url = git_url
        self.build_path = build_path
        self.project_type = project_type

    def dot_net_core_pipeline(self):
        return '''
        stage('Git Checkout') {
            steps {
                echo 'Checking out source code from Git...'
                git branch: 'main', url: "${GIT_URL}"
            }
        }

        stage('Restore Packages') {
            steps {
                echo 'Restoring packages...'
                sh "dotnet restore ${BUILD_PATH}"
            }
        }

        stage('Install SonarQube Scanner') {
            steps {
                script {
                    def scannerInstalled = sh(script: "dotnet tool list -g | grep dotnet-sonarscanner", returnStatus: true)
                    if (scannerInstalled != 0) {
                        echo 'Installing SonarQube Scanner...'
                        sh 'dotnet tool install --global dotnet-sonarscanner'
                    } else {
                        echo 'SonarQube Scanner already installed'
                    }
                }
            }
        }

        stage('SonarQube Begin Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    echo 'Running SonarQube Analysis...'
                    sh """export PATH="$PATH:$HOME/.dotnet/tools"
                    dotnet sonarscanner begin /k:${JOB_NAME} /n:"brachops"
                    """
                }
            }
        }

        stage('Build Solution') {
            steps {
                echo 'Building the project...'
                sh "dotnet build ${BUILD_PATH} --configuration Release"
            }
        }

        stage('SonarQube End Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    export PATH="$PATH:$HOME/.dotnet/tools"
                    dotnet sonarscanner end
                    """
                }
            }
        }

        stage('File System Scan') {
            steps {
                script {
                    def rootFolder = sh(script: "dirname ${BUILD_PATH}", returnStdout: true).trim()
                    sh "trivy fs --format table -o trivy-fs-report.html ${rootFolder}"
                }
            }
        }
        '''.strip()

    def node_js_pipeline(self):
        return """
        stage('Git Checkout') {
            steps {
                echo 'Checking out source code from Git...'
                git branch: 'main', url: "${GIT_URL}"
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing packages...'
                sh 'npm install'
            }
        }

        stage('Install SonarScanner') {
            steps {
                script {
                    def scannerInstalled = sh(script: "npm list -g | grep sonarqube-scanner", returnStatus: true)
                    if (scannerInstalled != 0) {
                        echo 'Installing SonarScanner...'
                        sh 'npm install -g sonar-scanner'
                    } else {
                        echo 'SonarScanner already installed'
                    }
                }
            }
        }

        stage('SonarQube Begin Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    echo 'Running SonarQube Analysis...'
                    sh 'export PATH="$PATH:$HOME/.nvm" && sonar-scanner -Dsonar.projectKey=${JOB_NAME} -Dsonar.projectName="brachops" -Dsonar.sources=.'
                }
            }
        }

        stage('File System Scan') {
            steps {
                script {
                    def rootFolder = sh(script: "dirname ${BUILD_PATH}", returnStdout: true).trim()
                    sh "trivy fs --format table -o trivy-fs-report.html ${rootFolder}"
                }
            }
        }
        """.strip()
    def generate(self):
        tools = 'tools {nodejs "node"}\n' if self.project_type == 'Node.js' else ""
        project_specific_pipeline = self.dot_net_core_pipeline() if self.project_type == '.NET Core' else self.node_js_pipeline()
        return f"""
        pipeline {{
        agent any
        {tools}
        environment {{
            JOB_NAME = "{self.job_name}"
            GIT_URL = "{self.git_url}"
            BUILD_PATH = "{self.build_path}"
        }}
        stages {{
            {project_specific_pipeline}
        }}
        }}""".strip()