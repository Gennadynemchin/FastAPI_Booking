from app.database import async_session_maker
from sqlalchemy import select, insert, delete

from app.hotels.rooms.models import Rooms


class BaseDAO:
    model = None


    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_bookings(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).subquery('query')
            extended_bookings = select(query,
                                       Rooms.image_id,
                                       Rooms.name,
                                       Rooms.description,
                                       Rooms.services).select_from(query).join(Rooms, query.c.room_id == Rooms.id)
            result = await session.execute(extended_bookings)
            return result.mappings().all()

    @classmethod
    async def add_data(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            return None

    @classmethod
    async def delete_data(cls, **data):
        async with async_session_maker() as session:
            get_booking = select(cls.model).filter_by(**data)
            booking = await session.execute(get_booking)
            booking = booking.scalar_one()
            await session.delete(booking)
            await session.commit()
            return None
