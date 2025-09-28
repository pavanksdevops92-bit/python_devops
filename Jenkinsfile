pipeline {
    agent any

    stages {

        stage('Welcome'){
            steps{
                sh "echo 'Hello Everyone'"
            }
        }
        
        stage('Clean Dependency-Check Cache') {
            steps {
                sh 'rm -rf ~/.dependency-check/data || true'
            }
        }
        
        stage('OWASP check'){
            steps{
                dependencyCheck additionalArguments: '''--scan . \\
                --format "ALL" \\
                --prettyPrint''', odcInstallation: 'OWASP_Dependency'
            }
        }

        stage('Testing and Coverage'){
            parallel{
                stage('unit testing'){
                    steps{
                        sh "pytest tests/test.py -v"
                    }
                }
                stage('Code Coverage'){
                    steps{
                        sh "pytest tests/test.py --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing"
                    }
                }
            }
        }

        stage('Building Docker Image'){
            steps{
                sh "docker build -t python-app ."
            }
        }

        stage('Trivy Scan'){
            steps{
                sh "trivy image python-app:latest"
            }
        }

        stage('Pushing Docker Image to ECR'){
            steps{
                sh "docker push <ECR_REGISTRY>/python-app:latest"
            }
        }

    }

    post{
        always{
            sh "docker rmi 315366007460.dkr.ecr.ap-south-1.amazonaws.com/python-app:latest"
        }
    }
}