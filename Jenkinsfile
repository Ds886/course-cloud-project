pipeline {
  agent {
    kubernetes {
      inheritFrom 'mypod'
    }
  }
  stages {
    stage('Build') {
      steps {
        sh 'ls /usr/bin'
        sh 'whoami' //Example: Checking the current user
      }
    }
  }
}
