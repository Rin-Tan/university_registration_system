from django.contrib import admin
from django.urls import path, include
from main.views import LoginRenderView
from courses import views 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from accounts.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    
    path('', LoginRenderView.as_view()),

    path('admin/', admin.site.urls),
    
    path('courses/', include('courses.urls')), 
    
    path('dashboard/', include('main.urls')),
    
    
    
    path('api/sessions/', CustomLoginView.as_view(), name='token_obtain_pair'),

    path('api/sessions/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #delete for logout
    path('api/sessions/current/', CustomLogoutView.as_view(), name='logout'),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

     path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

]