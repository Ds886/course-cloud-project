pipeline {
    agent {
     kubernetes {
        inheritFrom 'default'
         yaml '''
            spec:
                containers:
                    - name: alpine
                      image: quay.io/podman/stable
                      securityContext:
                        privileged: true
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
