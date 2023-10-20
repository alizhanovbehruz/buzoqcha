from aiogram.dispatcher.filters.state import StatesGroup, State


class doctor_update_(StatesGroup):
    updating = State()


class doctor_updatephone_(StatesGroup):
    updating = State()


class doctor_updatephoto_(StatesGroup):
    updating = State()


class doctor_updatelocation_(StatesGroup):
    updating = State()


class doctor_updatedecs_(StatesGroup):
    updating = State()


class clinic_update_(StatesGroup):
    updating = State()


class clinic_updatecity_(StatesGroup):
    updating = State()


class clinic_updatelocation_(StatesGroup):
    updating = State()


class clinic_updatephoto_(StatesGroup):
    updating = State()


class clinic_updatedecs_(StatesGroup):
    updating = State()


class clinic_updatetype_(StatesGroup):
    updating = State()


class petowner_clinic_(StatesGroup):
    type_clin = State()
    city = State()


class doctor_info_(StatesGroup):
    updating = State()
    full_name = State()
    number_phone = State()
    photo = State()
    location_to_serve = State()
    clinic_bool = State()
    specialities = State()


class clinic_info_(StatesGroup):
    type_clin = State()
    name = State()
    region = State()
    location = State()
    photo = State()
    description = State()


