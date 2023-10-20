from aiogram.dispatcher.filters.state import StatesGroup, State


class doctor_update(StatesGroup):
    updating = State()


class doctor_updatephone(StatesGroup):
    updating = State()


class doctor_updatephoto(StatesGroup):
    updating = State()


class doctor_updatelocation(StatesGroup):
    updating = State()


class doctor_updatedecs(StatesGroup):
    updating = State()


class clinic_update(StatesGroup):
    updating = State()


class clinic_updatecity(StatesGroup):
    updating = State()


class clinic_updatelocation(StatesGroup):
    updating = State()


class clinic_updatephoto(StatesGroup):
    updating = State()


class clinic_updatedecs(StatesGroup):
    updating = State()


class clinic_updatetype(StatesGroup):
    updating = State()


class petowner_clinic(StatesGroup):
    type_clin = State()
    city = State()


class doctor_info(StatesGroup):
    updating = State()
    full_name = State()
    number_phone = State()
    photo = State()
    location_to_serve = State()
    clinic_bool = State()
    specialities = State()


class clinic_info(StatesGroup):
    type_clin = State()
    name = State()
    region = State()
    location = State()
    photo = State()
    description = State()


