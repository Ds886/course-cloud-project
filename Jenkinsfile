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
        stage('Checkout') {
                steps {
                    container('alpine'){
                        '''
                        yum update -y
                        yum install -y git
                        '''
                }
                steps {
                    container('alpine'){
                        checkout scm
                }
            }
        }
        stage('Producer - Build and Publish'){
            steps {
                container('alpine'){
                    sh '''
                    tree .
                    '''
                }
            }
        }
    }
}
