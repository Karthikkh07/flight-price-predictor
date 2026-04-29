pipeline {
    agent any

    environment {
        PYTHON = "py"
    }

    stages {

        stage('Clone Code') {
            steps {
                echo "Cloning repository..."
                git 'https://github.com/Karthikkh07/flight-price-predictor'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing requirements..."
                bat '%PYTHON% -m pip install --upgrade pip'
                bat '%PYTHON% -m pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                echo "Training model..."
                bat '%PYTHON% train.py'
            }
        }

        stage('Test Model') {
            steps {
                echo "Testing model..."
                bat '%PYTHON% predict.py'
            }
        }

        stage('Run Streamlit App') {
            steps {
                echo "Starting app..."
                bat 'start /B %PYTHON% -m streamlit run app.py --server.port 8501 --server.headless true'
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
