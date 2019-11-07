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
response_items = response['items']  # Достаём из словаря список ID

log_view = 2   # Режим вывода логов: 0 – без логов, 1 - только итоги, 2 - все логи
remove_user = 0
approve_user = 0

for user_id in response_items:
    user_response = vk.users.get(user_id=user_id)
    if user_response[0].get('deactivated') is not None:  # Проверка, не заблокирован ли пользователь
        vk.groups.removeUser(group_id=NN, user_id=user_id)
        if log_view == 2:
            print("Пользователь с id", user_id, " заблокирован. Отклонён.", sep="")
        remove_user += 1
    else:
        if user_response[0]["is_closed"]:  # Проверка, не закрыт ли профиль пользователя
            vk.groups.approveRequest(group_id=NN, user_id=user_id)
            approve_user += 1
            if log_view == 2:
                print("Пользователь с id", user_id, " закрыт. Добавлен.", sep="")
        else:
            if check_pp(user_id, 7):  # Проверка, количества сомнительных подписок
                vk.groups.removeUser(group_id=NN, user_id=user_id)
                remove_user += 1
                if log_view == 2:
                    print("Пользователь с id", user_id, " имеет сомнительный подписки. Отклонён.", sep="")
            else:
                vk.groups.approveRequest(group_id=NN, user_id=user_id)
                approve_user += 1
                if log_view == 2:
                    print("Пользователь с id", user_id, " нормальный. Добавлен.", sep="")

if log_view > 0:
    print("Выполнение скрипта завершено!")
    if response['count'] == 0:
        print("Заявки в группу отсутствуют.")
    else:
        if approve_user > 0:
            print("Добавлено записей: ", approve_user)
        if remove_user > 0:
            print("Отклонено записей: ", remove_user)
    if response['count'] > 200:
        print("")
        print("Внимание! Обработаны не все заявки. Запустите скрипт ещё раз.")
