pipeline {
    agent any

    environment {
        PROJECT_ID = "crested-polygon-472204-n5"
        REGION = "us-west3"
        REPO_NAME = "python-app-repo"
        IMAGE_NAME = "us-west1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/python-app"
        GCP_SA_KEY = credentials('gke-sa-key')
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rachanack-rachhu/jenkins-gke-gke.git'
            }
        }

        stage('Auth to GCP') {
            steps {
                sh '''
                echo "$GCP_SA_KEY" > sa.json
                gcloud auth activate-service-account --key-file=sa.json
                gcloud config set project ${PROJECT_ID}
                gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push to Artifact Registry') {
            steps {
                sh '''
                docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to GKE (kubectl)') {
            steps {
                sh '''
                gcloud container clusters get-credentials cluster-ci --zone us-west3-c --project ${PROJECT_ID}
                kubectl set image deployment/python-app-deployment python-app-container=${IMAGE_NAME}:latest --namespace default || echo "Deployment not found, will be created"
                '''
            }
        }
    }
}
