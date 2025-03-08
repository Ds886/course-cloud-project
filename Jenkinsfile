pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                // Your build steps here
                echo 'Building..'
            }
        }
        
        stage('Test') {
            steps {
                // Your test steps here
                echo 'Testing..'
            }
        }
        
        stage('Deploy') {
            steps {
                // Your deployment steps here
                echo 'Deploying....'
            }
        }
    }
}
