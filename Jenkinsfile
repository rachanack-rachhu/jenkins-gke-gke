pipeline {
    agent {
        docker {
            image 'gcr.io/cloud-builders/docker'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        PROJECT_ID = "crested-polygon-472204-n5"
        REGION = "us-west1"
        ZONE = "us-west3-c"
        REPO_NAME = "python-app-repo"
        IMAGE_NAME = "us-west1-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/python-app"
        CLUSTER_NAME = "cluster-ci"
        GCP_SA_KEY = credentials('gke-sa-key')
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rachanack-rachhu/jenkins-gke-gke.git'
            }
        }

        stage('Install gcloud') {
            steps {
                sh '''
                apt-get update && apt-get install -y curl apt-transport-https ca-certificates gnupg
                curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts
                export PATH=$PATH:/root/google-cloud-sdk/bin
                '''
            }
        }

        stage('Auth to GCP') {
            steps {
                sh '''
                export PATH=$PATH:/root/google-cloud-sdk/bin
                echo "$GCP_SA_KEY" > sa.json
                gcloud auth activate-service-account --key-file=sa.json
                gcloud config set project ${PROJECT_ID}
                gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Artifact Registry') {
            steps {
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh '''
                export PATH=$PATH:/root/google-cloud-sdk/bin
                gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${PROJECT_ID}

                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }
}
