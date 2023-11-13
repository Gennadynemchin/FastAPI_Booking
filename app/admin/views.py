from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from sqladmin import ModelView


class UsersAdmin(ModelView, model=Users):
    name_plural = 'Users'
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]
    column_list = [Users.id, Users.email]


class BookingsAdmin(ModelView, model=Bookings):
    name_plural = 'Bookings'
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]


class HotelsAdmin(ModelView, model=Hotels):
    name_plural = 'Hotels'
    can_delete = False
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.name]


class RoomsAdmin(ModelView, model=Rooms):
    name_plural = 'Rooms'
    can_delete = False
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.id]