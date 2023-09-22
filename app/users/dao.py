from sqlalchemy import select

from app.database import async_session_maker
from app.users.models import Users
from app.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_user_safe(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            output_result = result.scalar_one_or_none()
            print(output_result)
            return output_result
