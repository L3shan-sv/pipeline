pipeline {
    agent {
        docker {
            image 'python:3.11-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock' // needed if building Docker images
        }
    }

    environment {
        AWS_REGION = 'us-east-1' // change as needed
        ECR_REPO = '123456789012/my-app' // change as needed
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                # Install essential binaries
                apk add --no-cache curl bash git

                # Install awscli and kubectl
                pip install --no-cache-dir awscli

                # Download kubectl binary
                curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                chmod +x kubectl
                mv kubectl /usr/local/bin/
                
                # Verify installations
                python3 --version
                aws --version
                kubectl version --client
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'echo "Run your test commands here"'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Scan Docker Image') {
            steps {
                sh 'echo "Add your image scanning here (optional)"'
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                '''
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh '''
                docker push ${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh 'echo "kubectl apply -f your-k8s-manifests/"'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
        }
        failure {
            echo '❌ Pipeline failed! Check logs.'
        }
    }
}
