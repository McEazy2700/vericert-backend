from typing import TYPE_CHECKING, Literal, Tuple, Union

from graphql import GraphQLError
from sqlalchemy import Select, select
from veecert_backend.config.database import async_db_session


if TYPE_CHECKING:
    from ..models import Client


class ClientManager:
    @classmethod
    async def one(cls, client_id: int) -> "Client":
        from ..models import Client

        stmt = select(Client).where(Client.id == client_id)
        return await cls.__exec_one_select_stmt__(stmt, "id", client_id)

    @classmethod
    async def one_by_user_id(cls, user_id: int) -> "Client":
        from ..models import Client

        stmt = select(Client).where(Client.user_id == user_id)
        return await cls.__exec_one_select_stmt__(stmt, "user_id", user_id)

    @classmethod
    async def __exec_one_select_stmt__(
        cls,
        stmt: Select[Tuple["Client"]],
        select_metric: Literal["id", "user_id"],
        select_metric_value: Union[str, int],
    ) -> "Client":
        async with async_db_session() as session:
            result = await session.execute(stmt)
            client = result.scalar_one_or_none()
            if client is None:
                raise GraphQLError(
                    f"Client with {select_metric} {select_metric_value} does not exist"
                )
            return client
