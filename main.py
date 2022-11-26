#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py: This script unfollows from all users you have been following.
"""


from multiprocessing import Process
from os.path import exists
from vk_api import vk_api


def init_bot() -> None:
    """
    init_bot: Initializes bot via entering login and password, getting
    access token, saving it into file 'access_token.txt'.
    """
    while True:
        try:
            session = vk_api.VkApi(
                login=input('Login: '),
                password=input('Password: '),
                scope=65538  # 65536 for non-expiring token, 2 for friends
            )

            session.auth(token_only=True)

            with open('access_token.txt', 'w') as ftoken:
                ftoken.write(session.token.get('access_token'))

        except Exception:
            print('Wrong Login or Password.')

        else:
            break


def remove_requests(offset) -> None:
    while True:
        try:
            requests = method.friends.getRequests(out=1, offset=offset)

            if not len(requests.get('items')):
                break

            for request in requests.get('items'):
                method.friends.delete(user_id=request)

        except Exception:
            ...


if __name__ == '__main__':
    if not exists('access_token.txt'):
        init_bot()

    access_token = open('access_token.txt').readline()
    session = vk_api.VkApi(token=access_token)
    method = vk_api.VkApiMethod(session)

    threads = [
        Process(target=remove_requests, args=(i * 20,))
        for i in range(4)
    ]

    for thread in threads:
        thread.start()
