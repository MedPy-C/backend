from .login import login_routes
from .user_login import user_login_routes

routes_backoffice = (
        login_routes + user_login_routes
)
