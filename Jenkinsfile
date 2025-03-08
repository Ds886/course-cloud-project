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
                        sh '''
                        yum update -y
                        yum install -y git tree
                        '''

                        checkout scm
                }
            }
        }
        stage('Producer - Build and Publish'){
            steps {
                withCredentials([usernamePassword(credentialsId: '7d236aad-d44f-43d3-89f7-137591bb8097', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    container('alpine'){
                        sh '''
                            cd repos/producer
                            VERSION=$(cat VERSION)
                            echo "${PASSWORD}"| podman login docker.com -u "${USERNAME}" --password-stdin
                            podman build -t "docker.com/dash886/course-rabbitprod:${VERSION}" -t "docker.com/dash886/course-rabbitprod:latest" .
                            podman push "docker.com/dash886/course-rabbitprod:${VERSION}"
                            podman push "docker.com/dash886/course-rabbitprod:latest"
                        '''
                    }
                }
            }
        }
    }
}
