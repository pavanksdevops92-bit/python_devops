pipeline {
    agent any

    parameters {
            booleanParam(
                name: 'RUN_OWASP_CHECK',
                defaultValue: false,
                description: 'Run OWASP dependency check'
            )
            string(
                name: 'ECR_REGISTRY',
                defaultValue: '488279421330.dkr.ecr.us-east-1.amazonaws.com',
                description: 'ECR Registry URL'
            )
            string(
                name: 'IMAGE_NAME',
                defaultValue: 'python-app',
                description: 'Docker image name'
            )
            string(
                name: 'AWS_REGION',
                defaultValue: 'us-east-1',
                description: 'AWS Region'
            )
            string(
                name: 'IMAGE_TAG',
                defaultValue: 'latest',
                description: 'Docker image tag'
            )
        }

    stages {

        stage('Welcome'){
            steps{
                sh "echo 'Hello Everyone'"
            }
        }
        
      stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    python3 --version
                    echo "Installing python3-venv..."
                    sudo apt-get update
                    sudo apt-get install -y python3-venv python3-pip

                    
                    # Create and activate virtual environment
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Clean Dependency-Check Cache') {
            steps {
                sh 'rm -rf ~/.dependency-check/data || true'
            }
        }
        
        stage('OWASP check'){
            when {
                expression { params.RUN_OWASP_CHECK == true }
            }
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
                        sh '''
                            . venv/bin/activate
                            pytest tests/test.py -v
                        '''
                    }
                }
                stage('Code Coverage'){
                    steps{
                        sh '''
                            . venv/bin/activate
                            pytest tests/test.py --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing
                        '''
                    }
                }
            }
        }

        stage('Building Docker Image'){
            steps{
                script {
                    def imageName = "${params.ECR_REGISTRY}/${params.IMAGE_NAME}:${params.IMAGE_TAG}"
                    sh "docker build -t ${imageName} ."
                    params.DOCKER_IMAGE = imageName
                }
            }
        }

        stage('Trivy Scan'){
            steps{
                sh "trivy image ${params.DOCKER_IMAGE}"
            }
        }

        stage('ECR Login'){
            steps{
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        sh "aws ecr get-login-password --region ${params.AWS_REGION} | docker login --username AWS --password-stdin ${params.ECR_REGISTRY}"
                    }
                }
            }
        }

        stage('Pushing Docker Image to ECR'){
            steps{
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        sh "docker push ${params.DOCKER_IMAGE}"
                    }
                }
            }
        }

    }

    post{
        always{
            script {
                // Cleanup Docker image
                if (env.DOCKER_IMAGE) {
                    sh "docker rmi ${env.DOCKER_IMAGE} || true"
                }
                // Cleanup virtual environment
                sh "rm -rf venv || true"
            }
            
            // Publish test results
            junit allowEmptyResults: true, testResults: '/test-results/*.xml'
            
            // Publish coverage reports
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        
        success {
            echo "Pipeline completed successfully! Image: ${env.DOCKER_IMAGE}"
        }
        
        failure {
            echo "Pipeline failed. Please check the logs."
        }
    }
}