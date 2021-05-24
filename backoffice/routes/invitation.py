from django.urls import path

from backoffice.view import invitation

invitation_routes = [
    path('user/<str:user_login_code>/group/<str:slug_name>/invitation/', invitation.InvitationView.as_view(
        {'post': 'create',
         'get': 'list'}), name='user_invitation'),
    path('user/<str:user_login_code>/group/<str:slug_name>/invitations/', invitation.InvitationView.as_view(
        {'get': 'list'}), name='user_invitations'),
    path('invitation/activate/<str:invitation_code>/', invitation.InvitationView.as_view(
        {'post': 'activate'}), name='activate_invitation')
    #      'put': 'update',
    #      'delete': 'delete'}), name='user_invitation'),

]
