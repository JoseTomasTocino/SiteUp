SiteUp
======

__SiteUp__ is an open source web platform for monitoring Internet services built using [Django](http://djangoproject.com). It's currently running at http://siteup.josetomastocino.com, although that's a __temporary__ location.

SiteUp lets you

* Check if remote servers are alive using __ICMP packets__ (ping).
* Monitor the status of your websites using __HTTP requests__. SiteUp can check both the status code and the content of your websites.
* Review the contents of the __DNS records__ of your domain. Supported types of records include A, AAAA, CNAME, MX and TXT.
* Check services in remote ports using __TCP connections__. SiteUp is able to check whether those ports are open and the content of the received response (if any).

SiteUp can trigger those checks to a frequency of up to 1 minute, and send notifications whenever their status change. Notifications can be sent via e-mail, or using push notifications through the __SiteUp Client__, an open source Android app built along the web platform and also present in this repository.

SiteUp uses __Celery__ and __RabbitMQ__ to handle the periodic tasks that trigger the checks. It also uses __Google Cloud Messaging__ to handle the push notifications to the SiteUp Android client. It also uses, like, a lot of additional packages and libraries to ease the development and avoid reinventing the wheel, like __South__, __requests__ and __django-braces__. Among the debugging utilities that have been used are the __django debug toolbar__ and __django extensions__.

On the front-end, SiteUp uses __Sass__ and __Compass__ to build the CSS, __D3__ to build the graphs and __jQuery__ for some interface-related scripting.

To run the web platform, the recommended setup is using __nginx__, __gunicorn__ and __supervisord__.

This project has been developed as the Final Degree Project for my __MSc in Computer Engineering__ at the [University of Cádiz](http://uca.es), Spain. Public defense is expected to take place the last week of May.

