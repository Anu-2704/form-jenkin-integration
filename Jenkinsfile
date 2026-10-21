
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat 'python --version'
                bat 'where python'
            }
        }

        stage('Setup Environment') {
            steps {
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python.exe -m pip install pytest'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat 'venv\\Scripts\\python.exe -m pytest -v --junitxml=test-results.xml'
            }
        }
    }

    post {
        always {
            script {
                if (fileExists('test-results.xml')) {
                    junit testResults: 'test-results.xml'
                } else {
                    echo 'Test report unavailable; checkout or setup may have failed.'
                }
            }
        }

        success {
            echo 'All HTML form tests passed!'
        }

        failure {
            echo 'Build failed. Check the stage that failed in Console Output.'
        }
    }
}
