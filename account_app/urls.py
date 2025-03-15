from django.urls import path
from .views import user_profile_list,start_matching, user_profile_detail, user_preferences, user_registration, user_login, explore_other_users, find_matches

urlpatterns = [
    path('api/register/', user_registration, name='user-registration'),
    path("api/login/", user_login, name="user-login"),
    
    path("users/", explore_other_users, name="list-other-users"),
    
    path('profiles/', user_profile_list, name='user-profile-list'),
    path('profiles/<int:pk>/', user_profile_detail, name='user-profile-detail'),
    path('preferences/', user_preferences, name='user-preferences'),
    
    path('api/matching/', find_matches, name='find_matches'),
    path('start_matching/', start_matching, name='start_matching'),
]
