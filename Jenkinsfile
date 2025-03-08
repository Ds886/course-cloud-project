pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: podman-agent
                    image: alpine:3.19
                    command: ["sh", "-c"]
                    args: ["while true; do sleep 30; done"]
            """
        }
    }
    stages {
        stage('Setup Podman') {
            agent {
                kubernetes {
                    yaml """
                        apiVersion: v1
                        kind: Pod
                        spec:
                          containers:
                          - name: podman-agent
                            image: alpine:3.19
                            command: ["sh", "-c"]
                            args: ["while true; do sleep 30; done"]
                    """
                }
            }
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
            agent {
                kubernetes {
                    yaml """
                        apiVersion: v1
                        kind: Pod
                        spec:
                          containers:
                          - name: podman-agent
                            image: alpine:3.19
                            command: ["sh", "-c"]
                            args: ["while true; do sleep 30; done"]
                    """
                }
            }
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
