from fastapi import Depends
from sqlmodel import Session
from ..database.connection import get_session
from ..models.user import User
from ..security import get_current_user


# Dependency to get database session
get_db_session = Depends(get_session)

# Dependency function to get current authenticated user
def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    return current_user