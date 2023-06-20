import datetime as dt
import statistics
import typing as tp

import numpy as np
from homework08.vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    year = dt.date.today().year
    age = []

    friends = get_friends(user_id=user_id, fields=["bdate"])
    for friend in friends:
        try:
            bday = int(friend["bdate"].split(".")[2])
            age.append(year - bday)
        except (AttributeError, IndexError, KeyError):
            pass

    if np.isnan(round(float(np.median(np.array(age))), 1)):
        return None
    return round(float(np.median(np.array(age))), 1)


if __name__ == "__main__":
    print(age_predict(user_id=505826062))
