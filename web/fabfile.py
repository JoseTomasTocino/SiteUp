from fabric.context_managers import prefix
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

env.user = 'omegote'
env.hosts = ['maquinita']

def deploy():
    code_dir = '/srv/siteup.josetomastocino.com/siteup'
    with cd(code_dir):
        with prefix('workon siteup'):
            run("git pull")
            run("web/manage.py syncdb")
            run("web/manage.py migrate siteup_api")
            run("sudo supervisorctl restart all")

