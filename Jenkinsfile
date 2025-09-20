pipeline {
    agent any
    
    environment {
        PROJECT_NAME = 'bootcamp'
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Build and Deploy') {
            steps {
                echo 'Building and deploying application...'
                script {
                    sh '''
                        cd /workspace
                        docker-compose --project-name ${PROJECT_NAME} down
                        docker-compose --project-name ${PROJECT_NAME} up --build -d
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Checking application health...'
                script {
                    sh '''
                        sleep 10
                        curl -f http://localhost:3001/data || exit 1
                    '''
                }
            }
        }
        
        stage('Run Integration Tests') {
            steps {
                echo 'Running integration tests...'
                script {
                    sh '''
                        docker exec ${PROJECT_NAME}-web-1 python -m pytest tests/ -v
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed!'
        }
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Deployment failed!'
            sh 'docker-compose --project-name ${PROJECT_NAME} logs'
        }
    }
}