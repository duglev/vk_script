# -*- coding: utf-8 -*-
import vk_api
from variables import NN, login, password

file_list_pp = open("PP.txt", "r")  # В файле содержится список id "сомнительных" пабликов
list_pp = file_list_pp.read()
list_pp = [int(x) for x in list_pp.split(',')]
file_list_pp.close()

file_user_pp = open("user_pp.txt", "r")
user_pp = file_user_pp.read()
file_user_pp.close()


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
response = vk.groups.getMembers(group_id=NN, count=1000, offset=11295, sort="time_desc")
response_items = response['items']  # Достаём из словаря список ID

for user_id in response_items:
    user_response = vk.users.get(user_id=user_id)
    if user_response[0].get('deactivated') is not None:  # Проверка, не заблокирован ли пользователь
        print("Пользователь с id", user_id, " заблокирован со статусом: ", user_response[0]['deactivated'], sep="")
        if user_response[0]['deactivated'] == "banned":
            vk.groups.removeUser(group_id=NN, user_id=user_id)
            print(user_id, "– удалён из группы.")
    else:
        if user_response[0]["is_closed"] is False:  # Проверка, не закрыт ли профиль пользователя
            if check_pp() > 10:  # Проверка, количества сомнительных подписок
                print("Пользователь с id", user_id, " Сомнительных подписок: ", check_pp(), " %", sep="")
                if user_pp.find(str(user_id)) == -1:
                    file_user_pp = open("user_pp.txt", "a")
                    file_user_pp.write("\n" + str(user_id))
                    file_user_pp.close()
                if check_pp() >= 30:
                    vk.groups.removeUser(group_id=NN, user_id=user_id)
                    print(user_id, "– удалён из группы.")
