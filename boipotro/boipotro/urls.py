"""boipotro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include,url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from books.views import home,author_detail,all_author


urlpatterns = [

    url(r'^$', home, name='home'), #This will be our home page
    url(r'^admin/', admin.site.urls),
    # url(r'^accounts/profile/^$', home, name='home'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^author/(?P<slug>[\w|\W]+)/$', author_detail, name='author_detail'),
    url(r'^authors/$', all_author, name='all_author'),
    url(r'^books/', include("books.urls",namespace='books')),
    url(r'^carts/', include("carts.urls",namespace='carts')),
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
