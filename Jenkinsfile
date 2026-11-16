pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    parameters {
        choice(name: 'ACTION', choices: ['Deploy', 'Delete'], description: 'Choose whether to deploy or remove the app')
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
