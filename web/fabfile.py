from fabric.context_managers import prefix
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.user = 'omegote'
env.hosts = ['maquinita']

code_dir = '/srv/siteup.josetomastocino.com/siteup'

def build_supervisor_conf():
    with cd(code_dir):
        with prefix('workon siteup'):
            run("web/manage.py supervisor_conf")
            run("sudo mv web/supervisor-siteup.conf /etc/supervisor/conf.d")
            run("sudo supervisorctl update")


def install():
    with cd(code_dir):
        with prefix('workon siteup'):
            run("mkdir -p logs")

def deploy():
    with cd(code_dir):
        with prefix('workon siteup'):
            run("git checkout .")
            run("git pull")
            run("pip install -r web/requirements.txt")
            run("web/manage.py collectstatic --noinput")
            run("web/manage.py syncdb")
            run("web/manage.py migrate siteup_api")
            run("sudo supervisorctl restart siteup_gunicorn siteup_celery")


def pull():
    with cd(code_dir):
        with prefix('workon siteup'):
            run("git checkout .")
            run("git pull")
            run("web/manage.py collectstatic --noinput")

