import bcrypt
from typing import TYPE_CHECKING, Optional, Tuple

from graphql import GraphQLError
from sqlalchemy import Select, select
from veecert_backend.config.database import async_db_session

if TYPE_CHECKING:
    from ..graphql.types.inputs import EmailPasswordSignUpInput


if TYPE_CHECKING:
    from ..models import User


class UserManager:
    @classmethod
    async def new_from_email_password(cls, args: "EmailPasswordSignUpInput") -> "User":
        from ..models import User

        if not (args.password1 == args.password2):
            raise GraphQLError("Passwords do not match")
        async with async_db_session() as session:
            stmt = select(User).where(User.email == args.email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is not None:
                raise GraphQLError("email already exists")
            user = User(
                email=args.email,
                password_hash=bcrypt.hashpw(
                    args.password1.encode(), bcrypt.gensalt()
                ).decode(),
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        from ..models import User

        stmt = select(User).where(User.email == email)
        return await cls.__exec_get_user_stmt__(stmt)

    @classmethod
    async def one_by_email(cls, email: str) -> "User":
        user = await cls.get_by_email(email)
        if user is None:
            raise GraphQLError(f"User with email {email} does not exist")
        return user

    @classmethod
    async def one_by_id(cls, user_id: int) -> "User":
        from ..models import User

        stmt = select(User).where(User.id == user_id)
        user = await cls.__exec_get_user_stmt__(stmt)
        if user is None:
            raise GraphQLError(f"User with id {user_id} does not exist")
        return user

    @classmethod
    async def __exec_get_user_stmt__(
        cls, stmt: Select[Tuple["User"]]
    ) -> Optional["User"]:
        async with async_db_session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
