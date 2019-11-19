# -*- coding: utf-8 -*-
import vk_api
from variables import login, password

file_list_pp = open("base/list_pp.txt", "r")  # В файле содержится список id "сомнительных" пабликов
list_pp = file_list_pp.read()
list_pp = [int(x) for x in list_pp.split('\n')]
file_list_pp.close()

file_checked_public = open("base/checked_public.txt", "r")  # В файле содержится список id проверенных пабликов
checked_public = file_checked_public.read()
checked_public = [int(x) for x in checked_public.split('\n')]
file_checked_public.close()

# Авторизация в ВК
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()

response = vk.groups.get(user_id=505583844)
difference_groups = set(response['items']).difference(list_pp)
difference_groups = set(difference_groups).difference(checked_public)
x = len(difference_groups)
# print("Сомнительных: ", int(x / response["count"]), "%")

for group_id in difference_groups:
    res_gr = vk.groups.getById(group_id=group_id, fields="description,members_count")
    res_gr = res_gr[0]
    x -= 1
    print("=========================================================================")
    print("Осталось рассмотреть групп:", x)
    print("https://vk.com/public", res_gr['id']," | ", res_gr['name']," | ", sep="", end=" ")
    if res_gr.get('members_count') is not None:
        print(res_gr['members_count'])
    else:
        print("Подписчики отсутсвуют")

    req = str(input())

    if req == "N" or req == "n":
        file_pp = open("base/checked_public.txt", "a")
        file_pp.write("\n" + str(group_id))
        file_pp.close()
        print("Группа пропущена")
    else:
        file_pp = open("base/list_pp.txt", "a")
        file_pp.write("\n" + str(group_id))
        file_pp.close()
        print("Группа добавлена в список")
