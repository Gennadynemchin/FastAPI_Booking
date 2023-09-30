from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import text
from sqlalchemy.sql.functions import coalesce

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from sqlalchemy import select, distinct, cast, String
from datetime import date


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_available(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # get_hotels_by_location = select(cls.model.__table__.columns).where(cls.model.location.contains(location))

            count_booked = select(Bookings.room_id, func.count(Bookings.room_id).label('count_booked')).where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
            ).group_by(Bookings.room_id).cte('count_booked')

            available_rooms = coalesce(Rooms.quantity - count_booked.c.count_booked, Rooms.quantity).label('available_rooms')

            get_available_rooms = select(Rooms.id, Rooms.hotel_id, available_rooms).select_from(Rooms).join(
                count_booked, count_booked.c.room_id == Rooms.id, isouter=True).group_by(Rooms.id, available_rooms).having(available_rooms > 0).cte('get_available_rooms')

            get_available_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                func.sum(get_available_rooms.c.available_rooms).label('rooms_left'),
                Hotels.image_id
            ).select_from(
                Hotels
            ).where(
                Hotels.location.contains(location)
            ).join(
                get_available_rooms,
                get_available_rooms.c.hotel_id == Hotels.id).group_by(Hotels.id)

            result = await session.execute(get_available_hotels)
            return result.mappings().all()
