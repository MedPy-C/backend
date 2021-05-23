from django.urls import path

from backoffice.view import group

group_routes = [
    path('user/<str:user_login_code>/group/', group.GroupView.as_view(
        {'post': 'create',
         'get': 'list'}), name='user_groups'),

    path('user/<str:user_login_code>/group/<str:group_code>/', group.GroupView.as_view(
        {'get': 'retrieve',
         'put': 'update',
         'delete': 'delete'}), name='user_group'),

]
