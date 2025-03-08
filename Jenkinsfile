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
                    volumeMounts:
                    - name: podman-sock
                      mountPath: /var/run/podman
                  volumes:
                  - name: podman-sock
                    hostPath:
                      path: /var/run/podman
            """
        }
    }
    stages {
        stage('Setup Podman') {
            steps {
                sh '''
                    # Install necessary packages
                    apk add --no-cache podman
                    # Verify Podman installation
                    podman --version
                '''
            }
        }
        stage('Test Podman') {
            steps {
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
