pipeline {
    agent any

    environment {
        PYTHON = "py"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat '%PYTHON% -m pip install --upgrade pip'
                bat '%PYTHON% -m pip install -r requirements.txt'
            }
        }

        stage('Run Streamlit App') {
            steps {
                echo "Starting Streamlit app..."
                bat '%PYTHON% -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0'
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
