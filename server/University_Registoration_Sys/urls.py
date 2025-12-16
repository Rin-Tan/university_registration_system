from django.contrib import admin
from django.urls import path, include

from accounts.views import (
    LoginRenderView, 
    dashboard_view, 
    logout_view, 
    CustomLoginView, 
    CustomLogoutAPIView 
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    
    
    path('', LoginRenderView.as_view(), name='login'),
    path('dashboard/', dashboard_view, name='dashboard'), 
    path('logout/', logout_view, name='logout'),
    
    
    path('api/sessions/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/sessions/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/sessions/current/', CustomLogoutAPIView.as_view(), name='api_logout'),

    
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')), 
    
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

]