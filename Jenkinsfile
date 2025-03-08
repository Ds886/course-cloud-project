pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Podman') {
            steps {
                script {
                    def osType = sh(script: 'uname -s', returnStdout: true).trim()
                    def isDebian = sh(script: 'test -f /etc/debian_version && echo "true" || echo "false"', returnStdout: true).trim()
                    def isRHEL = sh(script: 'test -f /etc/redhat-release && echo "true" || echo "false"', returnStdout: true).trim()

                    if (isDebian == 'true') {
                        // For Ubuntu/Debian
                        sh '''
                            sudo apt-get update
                            sudo apt-get install -y curl wget gnupg2
                            source /etc/os-release
                            echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
                            curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
                            sudo apt-get update
                            sudo apt-get -y install podman
                        '''
                    } else if (isRHEL == 'true') {
                        // For RHEL/CentOS/Fedora
                        sh '''
                            sudo dnf -y install podman
                        '''
                    } else {
                        error "Unsupported operating system"
                    }

                    // Verify installation
                    sh '''
                        podman --version
                        podman info
                    '''
                }
            }
        }
        
        stage('Build') {
            steps {
                // Your build steps here
                echo 'Building..'
            }
        }
        
        stage('Test') {
            steps {
                // Your test steps here
                echo 'Testing..'
            }
        }
        
        stage('Deploy') {
            steps {
                // Your deployment steps here
                echo 'Deploying....'
            }
        }
    }
}
