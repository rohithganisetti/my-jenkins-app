pipeline {
    agent any

    environment {
        AWS_REGION = "eu-north-1"
        ECR_REPO = "417744795688.dkr.ecr.eu-north-1.amazonaws.com/sns-py-api"
        IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Clone Git Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/rohithganisetti/my-jenkins-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Push to AWS ECR') {
            steps {
                withAWS(credentials: 'RohithGanisetti', region: "${AWS_REGION}") {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} \
                        | docker login --username AWS --password-stdin ${ECR_REPO}
                        docker push ${ECR_REPO}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['SSH-RohithGanisetti']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ec2-user@51.21.192.234 "
                            docker stop \$(docker ps -q --filter ancestor=${ECR_REPO}:${IMAGE_TAG}) || true &&
                            docker rm \$(docker ps -aq --filter ancestor=${ECR_REPO}:${IMAGE_TAG}) || true &&
                            aws ecr get-login-password --region ${AWS_REGION} \
                            | docker login --username AWS --password-stdin ${ECR_REPO} &&
                            docker pull ${ECR_REPO}:${IMAGE_TAG} &&
                            docker run -d -p 5000:80 ${ECR_REPO}:${IMAGE_TAG}
                        "
                    '''
                }
            }
        }
    }
}