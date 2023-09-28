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
from sqlalchemy import select
from datetime import date


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_available(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            get_hotels_by_location = select(cls.model.__table__.columns).where(cls.model.location.contains(location))

            subquery = select(Bookings.room_id, func.count(Bookings.room_id).label('count_booked')).where(
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
            ).group_by(Bookings.room_id).cte('subquery')

            subquery2 = select(Rooms.id, coalesce(Rooms.quantity - subquery.c.count_booked, Rooms.quantity).label('test')).select_from(Rooms).join(subquery, subquery.c.room_id == Rooms.id, isouter=True).group_by(Rooms.id, 'test')

            subquery_result = await session.execute(subquery2)
            return subquery_result.mappings().all()
