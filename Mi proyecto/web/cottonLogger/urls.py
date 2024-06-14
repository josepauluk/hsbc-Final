from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login',          views.logger,       name='login'               ),
    path('',               views.logger,       name='logger_main'         ),
    # path('default/',       views.defaultLogin, name='logger_default'      ),
    # path('default/error/', views.defaultError, name='logger_defaultError' ),
    path('tk/',            views.token,        name='logger_token'        ),
    path('tk/error/',      views.tokenError,   name='logger_tokenError'   ),
    path('tk/expired/',    views.tokenExpired, name='logger_tokenExpired' ),
    path('tk/create/',     views.tokenCreate,  name='logger_tokenCreate'  ),
    path('logout/',        views.logout,       name='logout'              ),
]
