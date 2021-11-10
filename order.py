import json
from datetime import datetime, timedelta
from pydantic import BaseModel, validator, constr, EmailStr


class Order(BaseModel):
    coffee_house_id: int
    order_content: constr(max_length=150)
    time: datetime
    order_number: int = 0
    email: EmailStr = None
    phone_number: int = None

    class Config:
        json_dumps = lambda v, *, default: json.dumps(v, ensure_ascii=False, default=default)

    @classmethod
    @validator('time')
    def time_validator(cls, future: datetime):
        min_time = timedelta(minutes=15)
        max_time = timedelta(hours=5)
        now = datetime.now()
        assert now < future and min_time <= future - now <= max_time, \
            "Неверное время заказа. Разрешенное время от 15 минут до 5 часов"
        return future


# input_json = """{
#     "coffee_house_id": "1234",
#     "order_content": "Ванильный Раф + клубничный сироп",
#     "time": "2021-11-10T18:45",
#     "phone_number": "9143332211",
#     "email": "test@gmail.com"
# }"""
#
# try:
#     order = Order.parse_raw(input_json)
# except ValidationError as e:
#     print(e)
# else:
#     print("Заказ принят")
