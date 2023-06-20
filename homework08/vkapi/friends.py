import dataclasses
import time
import typing as tp
import warnings

import requests  # type: ignore

from vkapi import config, session  # type: ignore
from vkapi.config import VK_CONFIG  # type: ignore

warnings.simplefilter(action="ignore", category=FutureWarning)
QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return self.count


def get_friends(
    user_id: int = 505826062, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = VK_CONFIG["domain"]
    access_token = VK_CONFIG["access_token"]
    v = VK_CONFIG["version"]
    user_id = user_id
    fields = ", ".join(fields) if type(fields) == list else ""  # type: ignore
    columns = ["id"] + fields.split(", ") if fields != "" else ["id"]  # type: ignore
    friends = []

    query = (
        f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&count={count}"
        f"&offset={offset}&fields={fields}&v={v}"
    )

    response = requests.get(query)
    people = response.json()["response"]["items"]

    if fields != "":
        for person in people:
            try:
                person["deactivated"]
            except KeyError:
                new_dict = {key: person[key] for key in columns if key in person}
                friends.append(new_dict)
    else:
        friends = people

    friends_response = FriendsResponse(count=len(friends), items=[friend for friend in friends])
    return friends_response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.List[tp.Optional[int]] = None,  # type: ignore
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя
     с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    query_params = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": ",".join(map(str, target_uids)) if target_uids is not None else None,
        "order": order,
        "count": count,
        "offset": offset,
        "progress": progress,
    }

    if type(target_uid) == int:
        response = session.get("friends.getMutual", **query_params)
        mutual = response.json()["response"]
        return mutual

    else:
        if len(target_uids) > 100:  # type: ignore
            mutual = []  # type: ignore
            performed = 0
            not_performed = len(target_uids)  # type: ignore

            while not_performed > 0:
                response = session.get("friends.getMutual", **query_params)
                new_muts = response.json()
                try:
                    mutual = mutual + new_muts["response"] if new_muts["response"] not in mutual else mutual
                    performed += query_params["offset"]
                except KeyError:
                    performed += query_params["offset"]

                not_performed = len(target_uids) - performed  # type: ignore
                query_params["offset"] += 100
                time.sleep(4)

            mutual = list(filter(lambda d: d["common_friends"] != [], mutual))

            return mutual

        else:
            response = session.get("friends.getMutual", **query_params)
            try:
                check = response.json()
                return check["response"]
            except KeyError:
                return []  # type: ignore


if __name__ == "__main__":
    print(get_friends(user_id=505826062, fields=["first_name"]).items)
