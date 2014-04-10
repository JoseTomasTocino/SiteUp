# Installing the web app #

## Fetching the code

To install the web system, you should first __clone the repo__ somewhere in your server. 

    git clone https://github.com/JoseTomasTocino/pfc-ii.git siteup

We'll be working in the `web` folder from now on.

    cd siteup/web

## Installing Python environment and dependencies

In order to install the proper requirements you need to create a __virtualenv__. I highly recommend using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) alongside [virtualenv](http://www.virtualenv.org/en/latest/).

    pip install virtualenv
    pip install virtualenvwrapper

Make sure you check [virtualenvwrapper's documentation](http://virtualenvwrapper.readthedocs.org/en/latest/) and follow the steps to fulfill the installation.

With virtualenvwrapper installed, create a new virtualenv and install the requirements using `pip`. Note though that some requirements may need some header files, located in the `python-dev` package in debian-based distributions.

    mkvirtualenv siteup
    sudo apt-get install python-dev
    pip install -r web/requirements.txt

## Building the database

Next step is to set up the database. Use the following commands to build the database and the tables. Currently the project uses sqlite for both development and production environments, but this will change in the future.

    ./manage.py syncdb
    ./manage.py migrate siteup_api

## Installing required services

Any web project built using a Python web framework, such as Django, needs a __WSGI http server__, that will run the python files within the project, and a __HTTP Proxy server__, that will receive the actual requests from the users and route them to the WSGI server. For the first, SiteUp uses [gunicorn](http://gunicorn.org/). It gets installed via `pip` along with the other dependencies in the previous steps.

For the second, I recommend using [nginx](http://nginx.org). It's a powerful HTTP server and reverse proxy, and you can install it easily using the package manager of your distribution

    sudo apt-get install nginx

Additionally, SiteUp needs a way of running tasks asynchronously. For that task we use [celery](http://www.celeryproject.org/), a the task queue that triggers the checks periodically. Celery is also installed automatically along the other python dependencies.

Finally, Siteup needs a [AMQP](http://en.wikipedia.org/wiki/AMQP) server to store the tasks. Recommended option is [RabbitMQ](https://www.rabbitmq.com/):

    sudo apt-get install rabbitmq-server

### Running the services

Usually, both nginx and rabbitmq will run when you the computer starts as they've been installed system-wide. On the other hand, it's necessary to have a way of running gunicorn and celery. The best option I've found is using [supervisord](http://supervisord.org/), it's pretty simple and easier to use than traditional `init.d` scripts. 

SiteUp includes __a management task__ that automatically creates the configuration file for supervisord.

    ./manage.py supervisor_conf
    sudo mv supervisor-siteup.conf /etc/supervisord/conf.d

That task will ask for some variables that SiteUp reads from the environment. 

* `GMAIL_PASS`, used in `siteup/settings/base.py`. Password for the gmail account used to send emails.
* `GCM_API_KEY`, used in `siteup_checker/task_notification.py`. Google Cloud Messaging api key.

In development you won't be using Supervisord, so you should set them up appropiately. A good option is placing them in your virtualenv's `postactivate` script, like this:

    cdvirtualenv
    cd bin
    cat >> postactivate
    export GMAIL_PASS=yourpass
    export GCM_API_KEY=yourkey

Now you need to configure your proxy server. I'm using __nginx__ because it's very easy to configure as a proxy. A possible configuration could be this (change your paths accordingly):

    server {
        listen 80;
        server_name siteup.josetomastocino.com;
    
        # Static files
        location /static/ {
            root /srv/siteup.josetomastocino.com/siteup/web/siteup_frontend;
            try_files $uri $uri/ =404;
        }
    
    
        location / {
            proxy_set_header X-Real-IP        $remote_addr;
            proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
            proxy_set_header Host             $http_host;
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



## Performance issues ##

__Rabbitmq__ default configuration makes it consume a lot of memory and can become a problem in systems with limited resources, such as low-end vps. In order to fix that you can add the following to `/etc/rabbitmq/rabbitmq.config` to limit the max memory to 15% of the total.

    [
        {rabbit, [{vm_memory_high_watermark, 0.15}]}
    ].

If the number of checks in your system is going to be low, you can decrease the number of __celery__ workers by modifying the `sup_celery.conf` file generated before, modifying the `-c 16` parameter in the `command` attribute.