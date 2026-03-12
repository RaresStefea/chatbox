from .core import router as core_router
from .auth import router as auth_router
from .users_DELETE import router as users_router
from .files import router as files_router

__all__ = ["core_router", "auth_router", "users_router", "files_router"]
