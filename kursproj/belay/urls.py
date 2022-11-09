from django.urls import path
from .views import *

urlpatterns = [
    path('', entry, name='entry'),
    path('logout', user_logout, name='logout'),
    path('registration', registration, name='registration'),
    path('profile/<str:username>', profile, name='profile'),
    path('profile/<str:username>/edit_profile/<int:pk>', UpdateProfile.as_view(), name='edit_profile'),

    path('news/', ViewSearchNews.as_view(), name='news'),
    path('news/add', AddNews.as_view(), name='add_news'),

    path('pact/', ViewSearchPact.as_view(), name='pact'),
    path('pact/add', AddPact.as_view(), name='add_pact'),
    path('pact/staff/<int:pk>', ViewSearchPact.as_view(), name='staff_pacts'),

    path('branch/', ViewSearchBranch.as_view(), name='branch'),
    path('branch/add', AddBranch.as_view(), name='add_branch'),

    path('staff/', ViewSearchStaff.as_view(extra_context={'archive': 0}), name='staff'),
    path('staff/archive/', ViewSearchStaff.as_view(extra_context={'archive': 1}), name='staff_archive'),
    path('staff/branch/<int:branch_id>/', ViewSearchStaff.as_view(extra_context={'archive': 0}), name='staff_branch'),
    path('staff/branch/<int:branch_id>/archive/', ViewSearchStaff.as_view(extra_context={'archive': 1}), name='staff_archive_branch'),

    path('staff/add', AddStaff.as_view(), name='add_staff'),
    path('staff/pacts/<int:pk>/<int:year>/<int:month>', calendar_staff_pacts, name='calendar_staff_pacts'),
    path('staff/<int:pk>', hold_staff, name='hold_staff'),
    path('staff/archive/<int:pk>', staff_return, name='staff_return'),
    path('staff/<int:pk>/delete', DeleteStaff.as_view(), name='staff-delete'),
]
