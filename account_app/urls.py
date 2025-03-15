from django.urls import path
from .views import user_profile_list, logout, start_matching,update_preferred_education, update_preferred_location, find_matches_allDetails, last_joined_user_view, user_profile_detail, user_preferences, user_registration, user_login, explore_other_users, find_matches

urlpatterns = [
    path('api/register/', user_registration, name='user-registration'),
    path("api/login/", user_login, name="user-login"),
    
    path("users/", explore_other_users, name="list-other-users"),
    
    path('profiles/', user_profile_list, name='user-profile-list'),
    path('profiles/<int:pk>/', user_profile_detail, name='user-profile-detail'),
    path('preferences/', user_preferences, name='user-preferences'),
    
    path('api/matching/', find_matches, name='find_matches'),
    path('start_matching/', start_matching, name='start_matching'),
    
    path('api/last_joined_user/', last_joined_user_view, name='last_joined_user'),
    path('api/find_matches_with_all_percentise/', find_matches_allDetails, name='find_matches_with_all_percentise'),
    path('update_preferred_education/', update_preferred_education, name='update_preferred_education'),
    path('update_preferred_location/', update_preferred_location, name='update_preferred_location'),
    path('api/logout/', logout, name='logout'),
]
