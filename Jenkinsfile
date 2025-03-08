pipeline {
    agent {
     kubernetes {
        inheritFrom 'default'
        }
    }
    stages {
        stage('Setup Podman') {
            steps {
                sh '''
                    ls /usr/bin
                    # Install necessary packages
                    /usr/bin/apk add --no-cache podman
                    # Verify Podman installation
                    /usr/bin/podman --version
                '''
            }
        }
        stage('Test Podman') {
            steps {
                sh '''
                    # Run a test container
                    /usr/bin/podman run -d --name test-container busybox sleep 3600
                    /usr/bin/podman ps -a
                    /usr/bin/podman rm test-container
                '''
            }
        }
    }
}
