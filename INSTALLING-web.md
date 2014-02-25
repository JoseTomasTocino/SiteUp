To install the web system, you should first __clone the repo__ somewhere in your server. We'll be working in the `web` folder from now on.

In order to install the proper requirements you need to create a __virtualenv__. I highly recommend using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

With virtualenvwrapper installed, create a new virtualenv and install the requirements using `pip`. Note though that some requirements may need some header files, located in the `python-dev` package in debian-based distributions.

    mkvirtualenv siteup
    sudo apt-get install python-dev
    pip install -r web/requirements.txt

SiteUp needs some kind of AMQP server to store the tasks. Recommended option is RabbitMQ:

    sudo apt-get install rabbitmq-server

Next step is to set up the database. Use the following commands to build the database and the tables. Currently the project uses sqlite for both development and production environments, but this will change in the future.

    ./manage.py syncdb
    ./manage.py migrate siteup_api

You need some way of running [gunicorn](http://gunicorn.org/) (the Python WSGI server) and [celery](http://www.celeryproject.org/) (the task queue that triggers the checks) permanently. I recommend using [supervisord](http://supervisord.org/), it's pretty simple and easier to use than traditional `init.d` scripts. SiteUp includes __two management tasks__ that automatically create the configuration file for supervisord. They're used like this:

    ./manage.py supervisor_gunicorn > sup_gunicorn.conf
    ./manage.py supervisor_celery > sup_celery.conf
    sudo mv sup.*.conf /etc/supervisord/conf.d

Now you need to configure your web server. I'm using __nginx__ because it's very easy to configure as a proxy. A possible configuration could be this (change your paths accordingly):

    server {
        listen 80;
        server_name siteup.josetomastocino.com;
    
        # Static files
        location /static/ {
                root /srv/siteup.josetomastocino.com/siteup/web/siteup_frontend;
                try_files $uri $uri/ =404;
        }
    
    
        location / {
                    proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header Host      $http_host;
            proxy_redirect off;
            if (!-f $request_filename) {
                        proxy_pass       http://127.0.0.1:8000;
                break;
            }
        }
    }

After that you should just restart both supervisord and nginx and you should be good to go:

    sudo service nginx restart
    sudo service supervisord restart

