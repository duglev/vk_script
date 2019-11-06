# -*- coding: utf-8 -*-
import vk_api
from variables import *

PP = open("PP.txt", "r")
PP = PP.read()
PP = [int(x) for x in PP.split(',')]


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def main():
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    response = vk.groups.getRequests(group_id=vk_id, count=200, offset=0)
    sum_add_users = 0

    for id in response['items']:
        response = vk.users.get(user_id=id)
        if response[0].get('deactivated') == 'deleted' or response[0].get("deactivated") == "banned":
            vk.groups.removeUser(group_id=vk_id, user_id=id)
            print("Отклонено: ", id, "(Учётная запись заблокирована)")
        else:
            if response[0]["is_closed"]:
                vk.groups.approveRequest(group_id=vk_id, user_id=id)
                sum_add_users += 1
            else:
                response = vk.groups.get(user_id=id)
                response = response['items']
                if len(set(response).intersection(PP)) < 7:
                    vk.groups.approveRequest(group_id=vk_id, user_id=id)
                    sum_add_users += 1
                else:
                    vk.groups.removeUser(group_id=vk_id, user_id=id)
                    print("Отклонено: ", id)

    print("Добавленно: ", sum_add_users, " учётных записей", sep="")


if __name__ == '__main__':
    main()
