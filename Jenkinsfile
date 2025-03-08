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
                      volumeMounts:
                        - name: podman-sock
                          mountPath: /var/run/podman
                volumes:
                    - name: podman-sock
                      hostPath:
                        path: /var/run/podman
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
                        echo "[storage]" > /etc/containers/storage.conf
                        echo 'driver = "vfs"' >> /etc/containers/storage.conf
                        # Configure rootless storage path using echo
                        echo "[rootless]" > /etc/containers/containers.conf
                        printf 'storage_path = "%s/.local/share/containers"' "$HOME" >> /etc/containers/containers.conf
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
