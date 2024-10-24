class ScanPipelineGenerator:
    def __init__(self, job_name: str, git_url: str, build_path: str, project_type: str):
        self.job_name = job_name
        self.git_url = git_url
        self.build_path = build_path
        self.project_type = project_type

    def dot_net_core_pipeline(self):
        return f"""
        stage('Git Checkout') {{
            steps {{
                echo 'Checking out source code from Git...'
                git branch: 'main', url: "{self.git_url}"
            }}
        }}

        stage('Restore Packages') {{
            steps {{
                echo 'Restoring packages...'
                sh "dotnet restore {self.build_path}"
            }}
        }}


        stage('Install SonarQube Scanner') {{
            steps {{
                script {{
                    def scannerInstalled = sh(script: "dotnet tool list -g | grep dotnet-sonarscanner", returnStatus: true)
                    if (scannerInstalled != 0) {{
                        echo 'Installing SonarQube Scanner...'
                        sh 'dotnet tool install --global dotnet-sonarscanner'
                    }} else {{
                        echo 'SonarQube Scanner already installed'
                    }}
                }}
            }}
        }}

        stage('SonarQube Begin Analysis') {{
            steps {{
                withSonarQubeEnv('SonarQube') {{
                    echo 'Running SonarQube Analysis...'
                    sh '''export PATH="$PATH:$HOME/.dotnet/tools"
                    dotnet sonarscanner begin /k:"{self.job_name}" /n:"BrachOps-{self.job_name}"
                    '''
                }}
            }}
        }}

        stage('Build Solution') {{
            steps {{
                echo 'Building the project...'
                sh "dotnet build {self.build_path} --configuration Release"
            }}
        }}

        stage('SonarQube End Analysis') {{
            steps {{
                withSonarQubeEnv('SonarQube') {{
                    sh '''
                    export PATH="$PATH:$HOME/.dotnet/tools"
                    dotnet sonarscanner end
                    '''
                }}
            }}
        }}

        stage('File System Scan') {{
            steps {{
                script {{
                    def rootFolder = sh(script: "dirname {self.build_path}", returnStatus: true)
                    sh "trivy fs --format table -o trivy-fs-report.html ${{rootFolder}}"
                }}
            }}
        }}
        """

    def node_js_pipeline(self):
        return f"""
        stage('Git Checkout') {{
            steps {{
                echo 'Checking out source code from Git...'
                git branch: 'main', url: "{self.git_url}"
            }}
        }}

        stage('Install Dependencies') {{
            steps {{
                echo 'Installing packages...'
                sh 'npm install'
            }}
        }}

        stage('Install SonarScanner') {{
            steps {{
                script {{
                    def scannerInstalled = sh(script: "npm list -g | grep sonarqube-scanner", returnStatus: true)
                    if (scannerInstalled != 0) {{
                        echo 'Installing SonarScanner...'
                        sh 'npm install -g sonar-scanner'
                    }} else {{
                        echo 'SonarScanner already installed'
                    }}
                }}
            }}
        }}

        stage('SonarQube Begin Analysis') {{
            steps {{
                withSonarQubeEnv('SonarQube') {{
                    echo 'Running SonarQube Analysis...'
                    sh '''export PATH="$PATH:$HOME/.nvm" 
                    && sonar-scanner -Dsonar.projectKey={self.job_name} 
                    -Dsonar.projectName="Brachops-{self.job_name}" 
                    -Dsonar.sources=.
                    '''
                }}
            }}
        }}

        stage('File System Scan') {{
            steps {{
                script {{
                    def rootFolder = sh(script: "dirname {self.build_path}", returnStdout: true).trim()
                    sh "trivy fs --format table -o trivy-fs-report.html rootFolder"
                }}
            }}
        }}
        """.strip()
    
    def generate(self):
        tools = 'tools {nodejs "node"}\n' if self.project_type == 'Node.js' else ""
        project_specific_pipeline = self.dot_net_core_pipeline() if self.project_type == 'DotNetCore' else self.node_js_pipeline()
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
        }}
        """.strip()