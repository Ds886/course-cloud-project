pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: podman-agent
                    image: quay.io/podman/podman-docker
                    command: ["cat"]
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
        stage('Test Podman') {
            steps {
                sh 'podman --version'
                sh 'podman run -d --name test-container busybox sleep 3600'
                sh 'podman ps -a'
                sh 'podman rm test-container'
            }
        }
    }
}

