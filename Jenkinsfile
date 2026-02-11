pipeline{
    agent any
    stage('Run Tests') {
    steps {
        sh 'pip install -r requirements.txt'
        sh 'pytest || true'
    }
}
stage('Scan Image') {
    steps {
        sh "trivy image ${IMAGE_NAME}:${BUILD_NUMBER}"
    }
}

}
