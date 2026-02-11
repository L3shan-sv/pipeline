pipeline {
    agent any   // Run on any available Jenkins agent

    environment {
        IMAGE_NAME = "myapp" // Name of the Docker image
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm   // Pull code from Git reponk
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pip install -r requirements.txt'   // Install dependencies
                sh 'pytest'                            // Run tests; pipeline fails if tests fail
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build Docker image and tag it with Jenkins build number
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Scan Docker Image') {
            steps {
                // Scan image for high/critical vulnerabilities
                sh "trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Login to ECR') {
            steps {
                // Use Jenkins credentials to authenticate to AWS ECR
                withCredentials([
                    string(credentialsId: 'aws_access_key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws_secret_key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'aws_region', variable: 'AWS_REGION'),
                    string(credentialsId: 'aws_account_id', variable: 'AWS_ACCOUNT_ID')
                ]) {
                    sh """
                    aws ecr get-login-password --region ${AWS_REGION} \
                    | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    """
                }
            }
        }

        stage('Tag Docker Image for ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws_account_id', variable: 'AWS_ACCOUNT_ID'),
                    string(credentialsId: 'aws_region', variable: 'AWS_REGION')
                ]) {
                    sh """
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} \
                    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws_account_id', variable: 'AWS_ACCOUNT_ID'),
                    string(credentialsId: 'aws_region', variable: 'AWS_REGION')
                ]) {
                    sh """
                    docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws_account_id', variable: 'AWS_ACCOUNT_ID'),
                    string(credentialsId: 'aws_region', variable: 'AWS_REGION'),
                    string(credentialsId: 'eks_cluster', variable: 'EKS_CLUSTER')
                ]) {
                    sh """
                    aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER}
                    kubectl set image deployment/myapp myapp=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}:${BUILD_NUMBER}
                    kubectl rollout status deployment/myapp
                    """
                }
            }
        }
    }

    post {
        success {
            echo " Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs."
        }
    }
}
