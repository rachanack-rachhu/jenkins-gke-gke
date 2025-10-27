pipeline {
    agent {
        docker {
            image 'gcr.io/google.com/cloudsdktool/cloud-sdk:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        PROJECT_ID = "crested-polygon-472204-n5"
        REGION = "us-west1"     // ✅ match Artifact Registry region
        ZONE = "us-west3-c"     // ✅ GKE zone
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
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Trivy Scan (Optional)') {
            steps {
                sh '''
                docker run --rm \
                -v /var/run/docker.sock:/var/run/docker.sock \
                aquasec/trivy:latest image ${IMAGE_NAME}:latest || true
                '''
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
                gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${PROJECT_ID}

                # If deployment does not exist, create it
                if ! kubectl get deployment python-app-deployment --namespace default > /dev/null 2>&1; then
                  kubectl create deployment python-app-deployment --image=${IMAGE_NAME}:latest --namespace default
                  kubectl expose deployment python-app-deployment --type=LoadBalancer --port 80 --target-port 5000 --namespace default
                else
                  kubectl set image deployment/python-app-deployment python-app-container=${IMAGE_NAME}:latest --namespace default
                fi
                '''
            }
        }
    }
}
