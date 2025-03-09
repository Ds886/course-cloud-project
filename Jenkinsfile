pipeline {
    agent {
     kubernetes {
        inheritFrom 'default'
         yaml '''
            spec:
                containers:
                    - name: podman
                      image: quay.io/podman/stable
                      securityContext:
                        privileged: true
                      command: ["sh", "-c"]
                      args: ["while true; do sleep 30; done"]
'''
        }
    }
    stages {
        stage('prepare') {
                steps {
                    container('podman'){
                        sh '''
                        yum update -y
                        yum install -y git tree curl
                        '''

                        checkout scm

                        sh ```
                        curl -Lo helm.tgz "https://get.helm.sh/helm-v3.17.1-linux-amd64.tar.gz"
                        tar xf helm.tgz
                        install -Dvm755 "linux-amd64/helm" "/usr/bin"
                        ```
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
                            echo "${PASSWORD}"| podman login docker.io -u "${USERNAME}" --password-stdin
                            podman build -t "docker.io/dash886/course-rabbitprod:${VERSION}" -t "docker.io/dash886/course-rabbitprod:latest" .
                            podman push "docker.io/dash886/course-rabbitprod:${VERSION}"
                            podman push "docker.io/dash886/course-rabbitprod:latest"
                        '''
                    }
                }
            }
        }
        stage('Consumer - Build and Publish'){
            steps {
                withCredentials([usernamePassword(credentialsId: '7d236aad-d44f-43d3-89f7-137591bb8097', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    container('alpine'){
                        sh '''
                            cd repos/consumer
                            VERSION=$(cat VERSION)
                            echo "${PASSWORD}"| podman login docker.io -u "${USERNAME}" --password-stdin
                            podman build -t "docker.io/dash886/courserabbit-consume:${VERSION}" -t "docker.io/dash886/courserabbit-consume:latest" .
                            podman push "docker.io/dash886/courserabbit-consume:${VERSION}"
                            podman push "docker.io/dash886/courserabbit-consume:latest"
                        '''
                    }
                }
            }
        }
        stage('Producer - deploy'){
            steps {
                withCredentials([usernamePassword(credentialsId: '7d236aad-d44f-43d3-89f7-137591bb8097', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    container('alpine'){
                        sh '''
                            cd repos/producer/chart
                            helm upgrade --install -n  project-cloud-arch producer .
                        '''
                    }
                }
            }
        }
        stage('Consumer - Deploy'){
            steps {
                withCredentials([usernamePassword(credentialsId: '7d236aad-d44f-43d3-89f7-137591bb8097', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    container('alpine'){
                        sh '''
                            cd repos/consumer/chart
                            helm upgrade --install -n  project-cloud-arch consumer .
                        '''
                    }
                }
            }
        }
    }
}
