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
                        cat << EOF > /etc/containers/storage.conf
                        [storage]
                        driver = "vfs"
                        EOF
                        # Configure rootless storage path using cat
                        cat << EOF > /etc/containers/containers.conf
                        [rootless]
                        storage_path = "$HOME/.local/share/containers"
                        EOF
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
