from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index ),
    url(r'^login/$',views.login),
    url(r'^regist/$',views.regist),
    url(r'^logout/$',views.logout),
    url(r'^changepwd/$',views.changepwd),
    url(r'^createM/$',views.createM),
    url(r'^saveM/$',views.saveM),
    url(r'^latest_msg/$',views.latest_msg),
    url(r'^mes/$',views.mes),


]