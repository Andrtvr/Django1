from django.conf.urls import url
from django.contrib import admin
from qa.views import qa

urlpatterns = [
    url(r'^', qa, name='qa'),
    #url(r'^admin/', admin.site.urls),
]
