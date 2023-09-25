from sqlalchemy import select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from sqlalchemy import and_, or_, func, insert

from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add_booking(cls, user_id: int, room_id: int, date_from, date_to):
        async with async_session_maker() as session:
            '''
            with booked_rooms as 
            (
            select * from bookings where room_id = 1 and (date_from >= '2023-05-15' and date_from <= '2023-06-20')
            or 
            date_from <= '2023-05-15' and date_to > '2023-05-15'
            )
            '''
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
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
                )
            ).cte('booked_rooms')

            '''
            select rooms.quantity - count(booked_rooms.room_id) from rooms left join booked_rooms on 
            booked_rooms.room_id = rooms.id where rooms.id = 1 group by rooms.quantity, booked_rooms.room_id
            '''
            get_available_rooms = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('available_rooms')
            ).select_from(Rooms).join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True).where(
                Rooms.id == room_id).group_by(Rooms.quantity, booked_rooms.c.room_id)
            # print(available_rooms.compile(engine, compile_kwargs={'literal_binds': True}))
            available_rooms = await session.execute(get_available_rooms)
            if available_rooms.scalar() > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(room_id=room_id,
                                                      user_id=user_id,
                                                      date_from=date_from,
                                                      date_to=date_to,
                                                      price=price).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None
