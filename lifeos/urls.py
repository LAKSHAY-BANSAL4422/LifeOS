from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard:index') if request.user.is_authenticated else redirect('login')),
    
    # Auth URLs
    path('register/', accounts_views.register_view, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('accounts/', include('accounts.urls')),

    # Modular App URLs (Report Section 4.2 & 4.3)
    path('dashboard/', include('dashboard.urls')),
    path('academics/', include('academics.urls')),
    path('tasks/', include('tasks.urls')),
    path('goals/', include('goals.urls')),
    path('habits/', include('habits.urls')),
    path('finance/', include('finance.urls')),
    path('calendar/', include('planner.urls')),
    path('career/', include('career.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
