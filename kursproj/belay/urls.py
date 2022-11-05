from django.urls import path
from .views import *

urlpatterns = [
    path('', entry, name='entry'),
    path('logout', user_logout, name='logout'),
    path('registration', registration, name='registration'),
    path('profile/<str:username>', profile, name='profile'),
    path('profile/<str:username>/edit_profile/<int:pk>', StaffUpdateView.as_view(), name='edit_profile'),

    path('news/', news, name='news'),
    path('news/add', add_news, name='add_news'),
    path('news/search', search_news, name='search_news'),

    path('pact/', pact, name='pact'),
    path('pact/add', add_pact, name='add_pact'),
    path('pact/search', search_pact, name='search_pact'),

    path('branch/', branch, name='branch'),
    path('branch/add', add_branch, name='add_branch'),
    path('branch/search', search_branch, name='search_branch'),
    path('branch/<int:branch_id>/', get_branch, name='branch'),
    path('branch/<int:branch_id>/search', get_branch_search, name='get_branch_search'),

    path('staff/', staff, name='staff'),
    path('staff/add', add_staff, name='add_staff'),
    path('staff/search', search_staff, name='search_staff'),
    path('staff/archive/search', search_staff_archive, name='search_staff_archive'),
    path('staff/pacts/<int:pk>', staff_pacts, name='staff_pacts'),
    path('staff/pacts/<int:pk>/<int:year>/<int:month>', calendar_staff_pacts, name='calendar_staff_pacts'),
    path('staff/archive', staff_archive, name='staff_archive'),
    path('staff/archive/<int:pk>', staff_return, name='staff_return'),
    path('staff/<int:pk>', hold_staff, name='hold_staff'),
    path('staff/<int:pk>/delete', StaffDeleteView.as_view(), name='staff-delete'),
]
