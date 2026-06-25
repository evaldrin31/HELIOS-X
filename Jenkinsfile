pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t helios-x .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker rm -f helios-x || exit 0'
                bat 'docker run -d --name helios-x -p 8080:80 helios-x'
            }
        }
    }
}