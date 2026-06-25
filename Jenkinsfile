pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t helios-x .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker stop helios-x || ver > nul'
                bat 'docker rm helios-x || ver > nul'
                bat 'docker run -d --name helios-x -p 8081:80 helios-x'
            }
        }

    }

    post {
        success {
            echo 'HELIOS-X Pipeline Executed Successfully!'
        }

        failure {
            echo 'Pipeline Failed!'
        }
    }
}