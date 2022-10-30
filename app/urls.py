from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("addProduct", views.add_product, name="add_product"),
    path("addShow", views.add_show, name="add_show"),
    path("remove", views.remove, name="remove"),
    
    path("shows", views.shows, name="shows"),
    path("shops", views.shops, name="shops"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
