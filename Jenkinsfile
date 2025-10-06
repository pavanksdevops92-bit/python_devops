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
            sh "docker rmi ${params.DOCKER_IMAGE}"
        }
    }
}