"""
URL configuration for proba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

IMP: urls.py define los mapeos url-vistas.
A pesar de que éste podría contener todo el código del mapeo url,
es más común delegar algo del mapeo a las propias aplicaciones, como verás más tarde.
"""
from django.contrib import admin
from django.urls import path

# Use include() to add paths from the catalog application (1)
from django.urls import include
#Add URL maps to redirect the base URL to our application (2)
from django.views.generic import RedirectView
# Use static() to add url mapping to serve static files during development (only) (3)
from django.conf import settings
from django.conf.urls.static import static
# 8036
""" Lo siguiente es una manera de incluir las rutas con '+='. 
Lo dejo comentado porque lo haré de una manera mas directa
urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += [
    path('catalog/', include('catalog.urls')),
]
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
# Esta es la opción mas directa
urlpatterns = [path('admin/', admin.site.urls),
               path('catalog/', include('catalog.urls')),  # (1)
               path('', RedirectView.as_view(url='/catalog/', permanent=True)),  # (2)
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # (3)
