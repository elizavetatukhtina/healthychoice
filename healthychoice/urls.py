from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from healthychoiceapp import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.home, name='home'),
    path('facts/', views.facts, name='facts'),
    path('news/', views.news, name='news'),
    path('recipes/', views.recipes, name='recipes'),
    path('facts/<str:slug>/', views.product, name = 'product'),
    path('recipes/<str:slug>/', views.recipe, name='recipe'),
    path('news/<str:slug>/', views.article, name='article'),
    path('login/', auth_views.LoginView.as_view(template_name="eater_user/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('eater/', views.eater_profile, name='eater-profile'),
    path('search/', views.search_titles)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
