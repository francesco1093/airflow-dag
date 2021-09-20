pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building from git repo..'
                sh '''
                        for filename in ./dags/*
                        do
                        echo $filename
                        done;
                '''

            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                mv ./dags /opt/jenkins/dags
                '''
            }
        }
    }
}