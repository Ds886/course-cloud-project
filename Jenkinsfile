pipeline {
    agent {
        kubernetes {
            label 'jenkins-agent=true'
            defaultContainer 'my-custom-container'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: some-value
spec:
  containers:
  - name: build
    image: alpine:3.21.3
    command: ["cat"]
    tty: true
  """
        }
    }


    stages {
        stage('Build') {
            steps {
                sh 'echo "Running build steps inside my custom Docker image!"'
                sh 'lsb_release -a' // Example: Check Ubuntu version
                sh 'whoami' //Example: Checking the current user
            }
        }
        // stage('Checkout') {
        //     steps {
        //         checkout scm
        //     }
        // }

        // stage('Install Podman') {
        //     steps {
        //         script {
        //             def osType = sh(script: 'uname -s', returnStdout: true).trim()
        //             def isDebian = sh(script: 'test -f /etc/debian_version && echo "true" || echo "false"', returnStdout: true).trim()
        //             def isRHEL = sh(script: 'test -f /etc/redhat-release && echo "true" || echo "false"', returnStdout: true).trim()

        //             if (isDebian == 'true') {
        //                 // For Ubuntu/Debian
        //                 sh '''
        //                      apt-get update
        //                      apt-get install -y curl wget gnupg2
        //                     source /etc/os-release
        //                     echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" |  tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
        //                     curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" |  apt-key add -
        //                      apt-get update
        //                      apt-get -y install podman
        //                 '''
        //             } else if (isRHEL == 'true') {
        //                 // For RHEL/CentOS/Fedora
        //                 sh '''
        //                      dnf -y install podman
        //                 '''
        //             } else {
        //                 error "Unsupported operating system"
        //             }

        //             // Verify installation
        //             sh '''
        //                 podman --version
        //                 podman info
        //             '''
        //         }
        //     }
        // }
        
        // stage('Build') {
        //     steps {
        //         // Your build steps here
        //         echo 'Building..'
        //     }
        // }
        
        // stage('Test') {
        //     steps {
        //         // Your test steps here
        //         echo 'Testing..'
        //     }
        // }
        
        // stage('Deploy') {
        //     steps {
        //         // Your deployment steps here
        //         echo 'Deploying....'
        //     }
        // }
    }
}
