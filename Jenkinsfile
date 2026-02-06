pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        APP_PORT = "8005"

        // Safer for CI (no external dependency)
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "email-spam"
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
           Stage 3: Data Ingestion
        ================================= */
        stage("Data Ingestion") {
            steps {
                sh '''
                
                . $VENV_NAME/bin/activate
                python data_ingestion.py
                '''
            }
        }

stage('Lint') {
  steps {
    sh 'venv/bin/python -m py_compile data_ingestion.py'
  }
}

        /* ================================
           Stage 4: Feature Engineering
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
           Stage 5: Data Preprocessing
        ================================= */
        stage("Data Preprocessing") {
            steps {
                sh '''

                . $VENV_NAME/bin/activate
                python preprocessing.py
                '''
            }
        }

        /* ================================
           Stage 6: Model Training (MLflow)
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
           Stage 7: Model Evaluation
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
           Stage 8: Pytests (Unit + API)
        ================================= */
stage("Run Pytests") {
    steps {
        sh '''
        . $VENV_NAME/bin/activate
        export PYTHONPATH=$(pwd)

        pytest test_data.py
        pytest test_model.py
        pytest test_api.py
        pytest test_schema.py -W ignore::pydantic.PydanticDeprecatedSince20
        '''
    }
}

        /* ================================
           Stage 9: Schema Validation
        ================================= */
stage("Schema Validation") {
    steps {
        sh '''
        . $VENV_NAME/bin/activate
        export PYTHONPATH=$(pwd)

        python schema.py
        '''
    }
}

        /* ================================
           Stage 10: FastAPI Local Smoke Test
        ================================= */
      
        stage("FastAPI Smoke Test") {
        steps {
            sh '''#!/bin/bash
        set -e

        . venv/bin/activate
        export PYTHONPATH=$WORKSPACE

        echo "🚀 Starting FastAPI..."

        nohup uvicorn main:app \
        --host 0.0.0.0 \
        --port 8005 \
        > uvicorn.log 2>&1 &

        echo "⏳ Waiting for FastAPI..."
        i=0
        while [ $i -lt 20 ]; do
        if curl -s http://localhost:8005/health | grep -q ok; then
            echo "✅ FastAPI is up"
            break
        fi
        sleep 1
        i=$((i+1))
        done

        if ! curl -s http://localhost:8005/health | grep -q ok; then
        echo "❌ FastAPI failed to start"
        echo "📄 Uvicorn log:"
        cat uvicorn.log
        exit 1
        fi

        echo "📡 Testing /predict..."
        curl -f http://localhost:8005/predict \
        -H "Content-Type: application/json" \
        -d '{"V1":0.1,"V2":0.1,"V3":0.1,"V4":0.1,"V5":0.1,
            "V6":0.1,"V7":0.1,"V8":0.1,"V9":0.1,"V10":0.1,
            "V11":0.1,"V12":0.1,"V13":0.1,"V14":0.1,"V15":0.1,
            "V16":0.1,"V17":0.1,"V18":0.1,"V19":0.1,"V20":0.1,
            "V21":0.1,"V22":0.1,"V23":0.1,"V24":0.1,"V25":0.1,
            "V26":0.1,"V27":0.1,"V28":0.1,"Amount":0.5}'
        '''
        }
        }

        stage("Docker Build & Run") {
        steps {
            sh '''#!/bin/bash
        set -e

        # 🧹 Remove old container by ID
        OLD_ID=$(docker ps -aq --filter "name=email-spam")
        if [ -n "$OLD_ID" ]; then
        docker rm -f $OLD_ID
        fi

        # 🏗 Build image
        docker build -t email-spam .

        # 🎯 Random port
        HOST_PORT=$(shuf -i 8000-8999 -n 1)
        echo $HOST_PORT > .docker_port

        # 🚀 Run container
        CONTAINER_ID=$(docker run -d \
        -p $HOST_PORT:8005 \
        --name email-spam \
        email-spam)

        echo $CONTAINER_ID > .docker_container_id

        echo "🐳 Docker running"
        echo "🆔 Container ID: $CONTAINER_ID"
        echo "🌐 Port: $HOST_PORT"
        '''
        }
        }

        stage("FastAPI Docker Test") {
        steps {
            sh '''#!/bin/bash
        set -e

        HOST_PORT=$(cat .docker_port)
        CONTAINER_ID=$(cat .docker_container_id)

        echo "⏳ Waiting for Docker FastAPI on port $HOST_PORT..."

        i=0
        while [ $i -lt 30 ]; do
        if curl -s http://localhost:$HOST_PORT/health | grep -q ok; then
            echo "✅ Docker API is up"
            break
        fi
        sleep 1
        i=$((i+1))
        done

        curl -f -s http://localhost:$HOST_PORT/predict \
        -H "Content-Type: application/json" \
        -d '{"V1":0.1,"V2":0.1,"V3":0.1,"V4":0.1,"V5":0.1,
            "V6":0.1,"V7":0.1,"V8":0.1,"V9":0.1,"V10":0.1,
            "V11":0.1,"V12":0.1,"V13":0.1,"V14":0.1,"V15":0.1,
            "V16":0.1,"V17":0.1,"V18":0.1,"V19":0.1,"V20":0.1,
            "V21":0.1,"V22":0.1,"V23":0.1,"V24":0.1,"V25":0.1,
            "V26":0.1,"V27":0.1,"V28":0.1,"Amount":0.5}'

        # 🧹 Cleanup
        docker rm -f $CONTAINER_ID
        '''
        }
        }

        /* ================================
           Stage 13: Archive Artifacts
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
            echo "✅ Credit Card Fraud MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Jenkins Logs"
        }

    }
}