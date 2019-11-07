# -*- coding: utf-8 -*-
import vk_api
from variables import NN, login, password


def check_pp(pp_id, pp_count):  # Данная функция ищет количество совпадений среди групп пользователя
    pp_list_id = open("PP.txt", "r")  # В файле содержится список id "сомнительных" пабликов
    pp_list_id = pp_list_id.read()
    pp_list_id = [int(x) for x in pp_list_id.split(',')]
    groups_response = vk.groups.get(user_id=pp_id)
    return len(set(groups_response['items']).intersection(pp_list_id)) > pp_count


# Авторизация в ВК
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()
# Запрашиваем список поступивших заявок в группу
response = vk.groups.getRequests(group_id=NN, count=200)
response = response['items']  # Достаём из словаря список ID

for user_id in response:
    user_response = vk.users.get(user_id=user_id)
    if user_response[0].get('deactivated') is not None:  # Проверка, не заблокирован ли пользователь
        vk.groups.removeUser(group_id=NN, user_id=user_id)
    else:
        if user_response[0]["is_closed"]:  # Проверка, не закрыт ли профиль пользователя
            vk.groups.approveRequest(group_id=NN, user_id=user_id)
        else:
            if check_pp(user_id, 7):  # Проверка, количества сомнительных подписок
                vk.groups.removeUser(group_id=NN, user_id=user_id)
            else:
                vk.groups.approveRequest(group_id=NN, user_id=user_id)
