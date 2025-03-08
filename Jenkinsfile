pipeline {
    agent {
     kubernetes {
        inheritFrom 'default'
         yaml '''
      spec:
        containers:
        - name: alpine
          image: alpine:3.19
          command: ["sh", "-c"]
          args: ["while true; do sleep 30; done"]
'''
        }
    }
    stages {
        stage('Setup Podman') {
            steps {
                container('alpine'){
                    sh '''
                        ls /usr/bin
                        # Install necessary packages
                        apk add --no-cache podman
                        # Verify Podman installation
                        podman --version
                    '''
                    
                }
            }
        }
        stage('Test Podman') {
            steps {
                container('alpine'){
                    sh '''
                        # Run a test container
                        podman run -d --name test-container busybox sleep 3600
                        podman ps -a
                        podman rm test-container
                    '''
                }
            }
        }
    }
}
