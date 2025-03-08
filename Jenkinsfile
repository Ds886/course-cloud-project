pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Get code from GitHub repository
                checkout scm
            }
        }

        stage('test'){
            steps {
                script {
                    echo "hello jenkins"
                }
            }
        }

    }
 }
