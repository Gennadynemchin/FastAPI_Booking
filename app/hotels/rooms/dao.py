from sqlalchemy import select, or_, and_, func
from sqlalchemy.sql.functions import coalesce

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from datetime import date


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_all_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
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

            available_rooms = coalesce(Rooms.quantity - count_booked.c.count_booked, Rooms.quantity).label(
                'available_rooms')

            get_available_rooms = select(Rooms.id,
                                         Rooms.hotel_id,
                                         Hotels.name,
                                         Rooms.description,
                                         Rooms.services,
                                         Rooms.price,
                                         Rooms.quantity,
                                         Rooms.image_id,
                                         available_rooms
                                         ).select_from(
                                                       Rooms
                                                      ).where(
                                                              Rooms.hotel_id == hotel_id
                                                             ).join(
                count_booked,
                count_booked.c.room_id == Rooms.id,
                isouter=True).join(
                                   Hotels,
                                   Hotels.id == Rooms.hotel_id,
                                   isouter=True).group_by(
                                                          Rooms.id,
                                                          Hotels.name,
                                                          available_rooms).having(available_rooms > 0)

            result = await session.execute(get_available_rooms)
            return result.mappings().all()
