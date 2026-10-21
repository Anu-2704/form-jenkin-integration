pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                // Downloads the code from the GitHub repository
                // configured in the Jenkins job.
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                // Create a virtual environment and install pytest into it.
                bat 'python --version'
                bat 'python -m venv venv'
                bat 'venv\\Scripts\\python -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                // If any test fails, pytest returns a non-zero code
                // and Jenkins marks the build as FAILED.
                bat 'venv\\Scripts\\python -m pytest -v --junitxml=test-results.xml'
            }
        }
    }

    post {
        always {
            // Show the test results in Jenkins (even when tests fail).
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        success {
            echo 'All tests passed. Build successful!'
        }
        failure {
            echo 'Build failed. Check the Console Output and Test Result.'
        }
    }
}
