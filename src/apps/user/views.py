# Import class-based views from submodules
from .auth_views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    HomeView
)

__all__ = [
    'RegisterView',
    'CustomLoginView',
    'CustomLogoutView',
    'HomeView'
]
