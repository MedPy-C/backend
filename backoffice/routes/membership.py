from django.urls import path

from backoffice.view import membership

members_routes = [
    path('user/<str:user_login_code>/group/<str:slug_name>/members/', membership.MembershipView.as_view(
        {'get': 'list'}), name='group_membership')]
