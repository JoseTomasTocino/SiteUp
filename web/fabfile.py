from fabric.api import run, env
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

env.user = 'omegote'
env.hosts = ['maquinita']

def host_type():
    run('uname -s')

def deploy():
    code_dir = '/srv/siteup.josetomastocino.com/siteup'
    with cd(code_dir):
        run("git pull")

