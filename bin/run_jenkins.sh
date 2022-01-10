#!/bin/bash
# from https://blog.juanwolf.fr/fr/posts/programming/integration-continue-django-jenkins/
#python3 -m venv ~/pyenv/venv_djcan # Création de l'environnement virtuel s'il n'existe pas

source /home/tomcat/pyenv/py3/bin/activate # Activation de l'environnement virtuel



#pip install -r ./djcan/requirements.txt # Installation des dépendances pour l'application
cd agstream
#python -m unittest discover project_directory "*_test.py"

rm .coverage
coverage run --source='.' -m unittest discover agstream  "*_test.py" # lancement des test
coverage xml -o "reports/coverage.xml"  --omit "*test*","*migrations","*/commands*"
coverage html  --directory reports  --omit="*test*","*migrations","*/commands*"

deactivate # On sort de l'environnement virtuel