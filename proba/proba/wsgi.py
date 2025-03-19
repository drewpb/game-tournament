"""
WSGI config for proba1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/

IMP: wsgi.py se usa para ayudar a la aplicación Django a comunicarse con el servidor web.
Puedes tratarlo como código base que puedes utilizar de plantilla.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proba1.settings")

application = get_wsgi_application()
