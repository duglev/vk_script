# -*- coding: utf-8 -*-
import vk_api
from variables import NN, login, password

file_list_pp = open("PP.txt", "r")  # В файле содержится список id "сомнительных" пабликов
list_pp = file_list_pp.read()
list_pp = [int(x) for x in list_pp.split(',')]
file_list_pp.close()


# Функция ищет количество совпадений среди подписок пользователя.
# Результат – процент сомнительных подписок от общего числа подписок.
def check_pp():
    groups_response = vk.groups.get(user_id=user_id)
    if groups_response["count"] > 0:
        return int((len(set(groups_response['items']).intersection(list_pp)) / groups_response["count"]) * 100)
    else:
        return 0


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

if log_view > 0 and response['count'] > 0:
    print("Скрипт запущен. Заявок в группу:", response['count'])

for user_id in response_items:
    user_response = vk.users.get(user_id=user_id)
    if user_response[0].get('deactivated') is not None:  # Проверка, не заблокирован ли пользователь
        vk.groups.removeUser(group_id=NN, user_id=user_id)
        remove_user += 1
        if log_view == 2:
            print("Пользователь с id", user_id, " заблокирован. Отклонён.", sep="")
    else:
        if user_response[0]["is_closed"]:  # Проверка, не закрыт ли профиль пользователя
            vk.groups.approveRequest(group_id=NN, user_id=user_id)
            approve_user += 1
            if log_view == 2:
                print("Пользователь с id", user_id, " закрыт. Добавлен.", sep="")
        else:
            if check_pp() > 20:  # Проверка, количества сомнительных подписок
                vk.groups.removeUser(group_id=NN, user_id=user_id)
                remove_user += 1
                if log_view == 2:
                    print("Пользователь с id", user_id, " Сомнительных подписок: ", check_pp(), " %", sep="")
            else:
                vk.groups.approveRequest(group_id=NN, user_id=user_id)
                approve_user += 1
                if log_view == 2:
                    print("Пользователь с id", user_id, " нормальный. Добавлен.", sep="")

if log_view > 0:
    if response['count'] == 0:
        print("Заявки в группу отсутствуют.")
    else:
        print("\nВыполнение скрипта завершено!")
        if approve_user > 0:
            print("Добавлено записей: ", approve_user)
        if remove_user > 0:
            print("Отклонено записей: ", remove_user)
    if response['count'] > 200:
        print("\nВнимание! Обработаны не все заявки. Запустите скрипт ещё раз.")
