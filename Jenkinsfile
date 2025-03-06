pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'master', url: 'https://github.com/AzmeerSohail/MLOps_ass1'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def buildStatus = powershell(returnStatus: true, script: 'docker build -t azmeer914/mlops-app:latest .')
                    if (buildStatus != 0) {
                        error("Docker build failed!")
                    }
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    powershell '''
                    $Password = $env:DOCKER_PASS | ConvertTo-SecureString -AsPlainText -Force
                    $Credential = New-Object System.Management.Automation.PSCredential ($env:DOCKER_USER, $Password)
                    docker login -u $env:DOCKER_USER -p $env:DOCKER_PASS
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    powershell 'docker push azmeer914/mlops-app:latest'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    powershell '''
                    $existingContainer = docker ps -q --filter "name=mlops-app"
                    if ($existingContainer) {
                        Write-Host "Stopping and removing existing container..."
                        docker stop mlops-app
                        docker rm mlops-app
                    }

                    Write-Host "Pulling the latest Docker image..."
                    docker pull azmeer914/mlops-app:latest

                    Write-Host "Running new container..."
                    docker run -d -p 5000:5000 --name mlops-app --restart always azmeer914/mlops-app:latest
                    '''
                }
            }
        }

    }

    post {
        success {
            script {
                emailext (
                    subject: "Deployment Successful: MLOps App",
                    body: """
                    Hello Admin,

                    The deployment of the MLOps App has been successfully completed.

                    Repository: https://github.com/AzmeerSohail/MLOps_ass1
                    Docker Image: azmeer914/mlops-app:latest

                    You can now access the application at <your-server-ip>:5000.

                    Regards,
                    Jenkins
                    """,
                    to: "azmeersohail03@gmail.com" // Replace with the actual admin email
                )
            }
        }
        failure {
            script {
                emailext (
                    subject: "Deployment Failed: MLOps App",
                    body: """
                    Hello Admin,

                    The deployment of the MLOps App has failed. Please check the Jenkins logs for more details.

                    Repository: https://github.com/AzmeerSohail/MLOps_ass1
                    Docker Image: azmeer914/mlops-app:latest

                    Regards,
                    Jenkins
                    """,
                    to: "azmeersohail03@gmail.com" // Replace with the actual admin email
                )
            }
        }
    }
}
