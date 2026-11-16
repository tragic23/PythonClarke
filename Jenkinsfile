pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    parameters {
        choice(name: 'ACTION', choices: ['Deploy', 'Delete'], description: 'deploy or delete app')
    }

    stages {
        stage('Build') {
            when {
                expression { params.ACTION == 'Deploy' }
            }
            steps {
                withCredentials([string(credentialsId: 'discord-bot-token', variable: 'BOT_TOKEN')]) {
                    sh '''
                        set -eu
                        echo "token length: ${#BOT_TOKEN}"
                        docker compose config --quiet
                        docker compose build
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                expression { params.ACTION == 'Deploy' }
            }
            steps {
                withCredentials([string(credentialsId: 'discord-bot-token', variable: 'BOT_TOKEN')]) {
                    sh '''
                        set -eu
                        docker compose up --detach --remove-orphans
                    '''
                }
            }
        }

        stage('Delete') {
            when {
                expression { params.ACTION == 'Delete' }
            }
            steps {
                withCredentials([string(credentialsId: 'discord-bot-token', variable: 'BOT_TOKEN')]) {
                    sh '''
                        set -eu
                        docker compose down --remove-orphans
                    '''
                }
            }
        }
    }
}
