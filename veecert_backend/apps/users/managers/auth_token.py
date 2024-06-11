import jwt
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING
from veecert_backend.config.settings import settings

from sqlalchemy import delete
from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..models import AuthToken


class AuthTokenManager:
    @classmethod
    async def new(cls, email: str) -> "AuthToken":
        from ..models import AuthToken, User

        async with async_db_session() as session:
            user = await User.manager.one_by_email(email)
            await session.execute(delete(AuthToken).where(AuthToken.user_id == user.id))
            payload = {
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
                "email": email,
            }
            token = jwt.encode(payload, settings.secret_key, algorithm="HS256")
            auth_token = AuthToken(auth_token=token, user=user)
            session.add(auth_token)
            await session.commit()
            await session.refresh(auth_token)
            return auth_token
