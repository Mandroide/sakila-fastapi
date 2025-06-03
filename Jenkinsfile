pipeline {
  agent any

  tools {
    // Requires Jenkins "Poetry" tool or just Python + pip
    python 'Python_3.12'
  }

  environment {
    POETRY_HOME = "${HOME}/.poetry"
    PATH = "${env.POETRY_HOME}/bin:${env.PATH}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Bootstrap Poetry') {
      steps {
        sh '''
          if ! command -v poetry >/dev/null; then
            curl -sSL https://install.python-poetry.org | python -
          fi
          poetry --version
        '''
      }
    }

    stage('Install Deps') {
      steps {
        sh 'poetry install --no-interaction --no-ansi --no-root'
      }
    }

    stage('Lint – Ruff')   { steps { sh 'poetry run ruff check .' } }
    stage('Type – mypy')   { steps { sh 'poetry run mypy .' } }
    //stage('Tests – pytest'){ steps { sh 'poetry run pytest -q -n auto' } }
  }

  post {
    always { junit '**/pytest-*.xml' }   // if you generate XML reports
  }
}
