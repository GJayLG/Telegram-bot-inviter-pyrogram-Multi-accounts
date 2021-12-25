import pyrogram
from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler
from time import sleep
from os import system

ids = []
old_ids = []
my_apps = []
settings = {'channel_to_invite':'invitechannel','parse_channel_ids': 'gg', 'delay_msg': 10, 'count_users_send': 20,"numbers": "+7900000000, +7900000100", "log": 1}

try:
    with open('settings.ini', 'rt', encoding='UTF8') as (f):
        file = f.readlines()
        for line in file:
            if '\n' in line:
                line = line[:-1]
            line = line.split(' = ')
            settings[line[0]] = line[1]

except:
    with open('settings.ini', 'wt', encoding='UTF8') as (f):
        for key in settings:
            f.write(f"{key} = {settings[key]}\n")
        
        print(f'Fill in the settings.ini file!')
        system('pause')
        exit(-1)

#vars
api_id = input(">Enter api_id: ").split(', ')
api_hash = input(">Enter api_hash: ").split(', ')
channel_to_invite = settings['channel_to_invite']
channel_id = settings['parse_channel_ids'].split(', ')
delay_msg = float(settings['delay_msg'])
numbers = settings['numbers'].split(', ')
log = int(settings['log'])
count_users_send = int(settings['count_users_send'])
#----

for i in range(0, len(numbers)):
    my_apps.append(Client(f"app{i}"))
    
    with Client(f"app{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
        pass

def log_txt(m):
    if log == 1:
        print(m)

def get_online_members():
    with Client(f"app{numbers[0]}", api_id[0], api_hash[0]) as my_apps[0]:
        app1 = my_apps[0]
        for k in channel_id:
            log_txt('получаем участников...')
            users = app1.iter_chat_members(k)
            for i in range(0,len(users)):
                ids.append(str(users[i]['user']['id']))
    for i in range(1, len(my_apps)):
        with Client(f"app{numbers[i]}", api_id[i], api_hash[i]) as my_apps[i]:
            my_apps[i].iter_chat_members(k)

def inviter(app):
    old_s = ''
    s = ''
    count = 0
    for g in old_ids:
        try:
            ids.remove(g)
        except:
            pass
    while True:
        for v in ids:
            s = v
            del ids[:1]
        
            if old_s != s:
                if count != count_users_send:
                    try:
                        app.add_chat_members(channel_to_invite, s)
                        count += 1
                    except pyrogram.errors.exceptions.forbidden_403.UserPrivacyRestricted:
                        print(f'У пользователя: {s} ограничение! Продолжаем!')
                    except pyrogram.errors.exceptions.bad_request_400.PeerFlood:
                        print('У этого аккаунта лимит!')
                        break
                else:
                    print(f'Пользователи подошли к концу: {count_users_send}')
                    count = 0
                    break
            else:
                print('Все сделанно!')
                break
            
            old_s = s

            log_txt(f"left: {len(ids)}")
            log_txt(f"user_send: {s}")
            sleep(delay_msg)
        else:
            continue
        break


if __name__ == "__main__":
    get_online_members()
    for i in range(0, len(my_apps)):
        print(f'Аккаунтов всего: {len(my_apps)}')
        with Client(f"app{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
            inviter(my_apps[i])