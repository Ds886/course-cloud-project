pipeline {
  agent {
    kubernetes {
      inheritFrom 'mypod'
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
  }
}
