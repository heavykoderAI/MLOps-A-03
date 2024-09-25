pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('i210327@nu.edu.pk') 
        DOCKER_IMAGE = "heavykoderAI/Car-Price-Predictor" 
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/heavykoderAI/MLOps-A-03.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'DOCKERHUB_CREDENTIALS') {
                        docker.image("${DOCKER_IMAGE}").push("latest")
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Docker Image pushed to Docker Hub successfully.'
        }
        failure {
            echo 'Failed to push Docker Image.'
        }
    }
}
