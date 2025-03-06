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
                    def buildStatus = sh(script: 'docker build -t azmeer914/mlops-app:latest .', returnStatus: true)
                    if (buildStatus != 0) {
                        error("Docker build failed!")
                    }
                }
            }
        }

       stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }


        stage('Push to Docker Hub') {
            steps {
                script {
                    sh 'docker push azmeer914/mlops-app:latest'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh '''
                    docker stop mlops-app || true
                    docker rm mlops-app || true
                    docker pull azmeer914/mlops-app:latest
                    docker run -d -p 5000:5000 --name mlops-app --restart always azmeer914/mlops-app:latest
                    '''
                }
            }
        }
    }
}
