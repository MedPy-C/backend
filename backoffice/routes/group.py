from django.urls import path

from backoffice.view import group

group_routes = [
    path('user/<str:user_login_code>/group/', group.GroupView.as_view(
        {'post': 'create',
         'get': 'list'}), name='user_groups'),

    path('user/<str:user_login_code>/group/<str:group_code>/', group.GroupView.as_view(
        {'get': 'retrieve'}), name='get_group'),
    path('user/<str:user_login_code>/group/<str:group_code>/', group.GroupView.as_view(
        {'put': 'update'}), name='update_group'),
    path('user/<str:user_login_code>/group/<str:group_code>/', group.GroupView.as_view(
        {'delete': 'delete'}), name='delete_group')

]
