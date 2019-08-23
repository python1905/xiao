from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^verify_login/$', views.verify_login, name='verify_login'),
    url(r'^enroll/$', views.user_enroll, name='enroll'),
    url(r'^is_sms/$', views.is_sms, name='is_sms'),
    url(r'^password/$', views.password, name='password'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user1/$', views.user1, name='user1'),

    url(r'^$', views.index, name='index'),
    url(r'^list$',views.list,name='list'),
    url(r'^detail$',views.detail,name='detail'),
    url(r'^shopping_cart$',views.shopping_cart,name='shopping_cart'),
    url(r'^settlement$',views.settlement,name='settlement'),
    url(r'^search$', views.search, name='search'),
    url(r'^delete$', views.delete, name='delect'),
    url(r'^ali_buy$',views.ali_buy, name='ali_buy'),
]