from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('account/',views.show_account,name='account'),
    path('logout/',views.sign_out,name='logout'),
    path('login/',views.login_view,name='login'),
    path('my-profile/', views.user_profile, name='my_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)