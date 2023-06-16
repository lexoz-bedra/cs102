import datetime as dt
import statistics
import typing as tp

import numpy as np
from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    year = dt.date.today().year
    age = []

    friends = get_friends(user_id=user_id)
    for friend in friends:
        try:
            bday = int(friend["bdate"].split(".")[2])
            age.append(year - bday)
        except (AttributeError, IndexError, KeyError):
            pass

    if np.isnan(round(np.median(np.array(age)), 1)):
        return None
    return round(np.median(np.array(age)), 1)
