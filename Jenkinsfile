pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        APP_PORT = "8005"

        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "email-spam"
        PYTHONPATH = "${WORKSPACE}"
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
    }

    stages {

        /* ================================
           Stage 1: Checkout Code
        ================================= */
        stage("Checkout Code") {
            steps {
                git branch: "master",
                    url: "https://github.com/anjilinux/project-mlflow-jenkins-Spam-Email-Detection-System.git"
            }
        }

        /* ================================
           Stage 2: Setup Virtual Environment
        ================================= */
        stage("Setup Virtual Environment") {
            steps {
                sh '''
                python3 -m venv $VENV_NAME
                . $VENV_NAME/bin/activate

                pip install -r requirements.txt
                '''
            }
        }

        /* ================================
           Stage 3: Verify Dataset
        ================================= */
        stage("Verify Dataset") {
            steps {
                sh '''
                if [ ! -f spam.csv ]; then
                    echo "❌ spam.csv missing"
                    exit 1
                fi
                echo "✅ spam.csv found"
                '''
            }
        }

        /* ================================
           Stage 4: Data Ingestion
        ================================= */
        stage("Data Ingestion") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python data_ingestion.py
                '''
            }
        }

        /* ================================
           Stage 5: Lint (Syntax Check)
        ================================= */
        stage("Lint") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python -m py_compile \
                    data_ingestion.py \
                    preprocessing.py \
                    data_preprocessing.py \
                    feature_engineering.py \
                    train.py \
                    evaluate.py \
                    main.py
                '''
            }
        }

        /* ================================
           Stage 6: Preprocessing (Text Clean)
        ================================= */
        stage("Preprocessing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python preprocessing.py
                '''
            }
        }

        /* ================================
           Stage 7: Data Preprocessing (Split)
        ================================= */
        stage("Data Preprocessing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python data_preprocessing.py
                '''
            }
        }

        /* ================================
           Stage 8: Feature Engineering
        ================================= */
        stage("Feature Engineering") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python feature_engineering.py
                '''
            }
        }

        /* ================================
           Stage 9: Model Training (MLflow)
        ================================= */
        stage("Model Training") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                python train.py
                '''
            }
        }

        /* ================================
           Stage 10: Model Evaluation
        ================================= */
        stage("Model Evaluation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python evaluate.py
                '''
            }
        }

        /* ================================
           Stage 11: Pytests
        ================================= */
        stage("Run Pytests") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                pytest test_data.py
                pytest test_model.py
                pytest test_api.py
                pytest test_schema.py -W ignore::pydantic.PydanticDeprecatedSince20
                '''
            }
        }

        /* ================================
           Stage 12: Schema Validation
        ================================= */
        stage("Schema Validation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python schema.py
                '''
            }
        }

        /* ================================
           Stage 13: FastAPI Smoke Test
        ================================= */
        stage("FastAPI Smoke Test") {
            steps {
                sh '''#!/bin/bash
                set -e
                . venv/bin/activate

                nohup uvicorn main:app \
                    --host 0.0.0.0 \
                    --port 8005 > uvicorn.log 2>&1 &

                sleep 5

                curl -f http://localhost:8005/health

                curl -f http://localhost:8005/predict \
                -H "Content-Type: application/json" \
                -d '{"text": "Congratulations! You won a free prize"}'
                '''
            }
        }

        /* ================================
           Stage 14: Docker Build & Run
        ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''#!/bin/bash
                set -e

                docker rm -f email-spam || true
                docker build -t email-spam .

                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo $HOST_PORT > .docker_port

                docker run -d \
                    -p $HOST_PORT:8005 \
                    --name email-spam \
                    email-spam
                '''
            }
        }

        /* ================================
           Stage 15: FastAPI Docker Test
        ================================= */
stage('FastAPI Docker Test') {
    steps {
        sh '''
        docker rm -f spam-api || true
        docker run -d -p 8777:8000 --name spam-api email-spam
        sleep 20
        curl --retry 10 --retry-delay 3 --retry-connrefused http://localhost:8777/health
        '''
    }
}


        /* ================================
           Stage 16: Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    model.pkl,
                    mlruns/**,
                    uvicorn.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Spam Email Detection MLOps Pipeline SUCCESS"
        }
        failure {
            echo "❌ Pipeline FAILED – Check Jenkins Logs"
        }
    }
}
