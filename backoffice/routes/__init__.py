from .login import login_routes
from .user_login import user_login_router

routes_backoffice = (
        login_routes + user_login_router
)
