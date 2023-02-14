# Client's personal account

Personal account for courier service clients

## Quickstart

***Run the following commands to bootstrap your environment:***

    sudo apt install software-properties-common -y  
    sudo add-apt-repository ppa:deadsnakes/ppa  
    sudo apt install python3.10
    
    sudo apt install git python3-dev python3-venv python3-pip nginx postgresql postgresql-contrib redis-server tmux
    
    git clone https://github.com/NickJoyce/ExcelUpload
    cd ExcelUpload
    
    scp /home/user/.env main@45.141.77.146:~/ExcelUpload
    
    python3.10 -m venv venv  
    . venv/bin/activate  
    pip install --upgrade pip  
    pip install -r requirements.txt
    
    set project.settings.prod instead project.settings in manage.py, project/celery.py, project/wsgi.py
    
    python manage.py makemigrations
    python manage.py migrate
    
    python manage.py collectstatic --settings=project.settings.prod
    
    tmux new -s celery_admin
    . venv/bin/activate
    celery -A project worker -l info
    ^b + d to exit


***Run the app locally***

    python3 manage.py runserver 0.0.0.0:8000 --settings=project.settings.dev

***Run the app with Gunicorn***

    gunicorn project.wsgi -b 0.0.0.0:8001
