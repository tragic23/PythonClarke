pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Build') {
            steps {
                withCredentials([string(credentialsId: 'discord-bot-token', variable: 'BOT_TOKEN')]) {
                    sh '''
                        set -eu
                        docker compose config --quiet
                        docker compose build
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'discord-bot-token', variable: 'BOT_TOKEN')]) {
                    sh '''
                        set -eu
                        docker compose up --detach --remove-orphans
                    '''
                }
            }
        }
    }
}
