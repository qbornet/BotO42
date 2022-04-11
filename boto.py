import os
import json
import discord
import time
import queue
import _thread
import threading
from discord.ext import tasks
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

lock = _thread.allocate_lock()
flag = 0
action = 0
chan_id = 0
queue = queue.Queue()
lst_dis = list()
lst_users = list()
users_table = dict()
time_table = dict()
session = dict()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHAN_NAME = os.getenv('CHAN_NAME')
UID_42 = os.getenv('UID_42')
SECRET_42 = os.getenv('SECRET_42')
token_url = "https://api.intra.42.fr/oauth/token"
client = discord.Client()

def for_loop(lst, key):
    j = 0
    for i in lst:
        if i == key:
            return (j)
        j += 1
    return (None)

def flag_is_ok():
    global flag

    lock.acquire()
    if (flag == 0):
        lock.release()
        return (1)
    lock.release()
    return (0)


def start_routine():
    global flag
    global lst_dis
    global chan_id
    global lst_users
    global users_table
    global time_table
    global session

    param = ''
    while (flag_is_ok()):
        pass
    lock.acquire()
    if (flag == 1):
        lock.release()
        # Header with client_id and client_secret easier to send key and fetch token
        auth = HTTPBasicAuth(UID_42, SECRET_42)

        # start client sesssion for OAuth lib and start session
        _client = BackendApplicationClient(client_id=UID_42);
        api42 = OAuth2Session(client=_client)
        time_token = time.localtime()[4]
        day = time.localtime()[2]
        token = api42.fetch_token(token_url=token_url, auth=auth)
        if (token is None):
            print("Didn't receive a token")
            _thread.exit()
        session['token'] = token

        while (1):
            j = 0
            index = -1
            for key in lst_dis:
                count = 0
                index += 1
                lst = users_table[key]
                for i in lst:
                    if (len(i) != 0):
                        count += 1
                    else:
                        break

                if (count > 1):
                    param = ','.join(x for x in lst if x)
                elif (count == 1):
                    param = lst[0]
                else:
                    break

                if (abs(time.localtime()[4] - time_token) >= 10):
                    try:
                        time_token = time.localtime()[4]
                        session['token'] = api42.fetch_token(token_url=token_url, auth=auth)
                    except:
                        print("Error with token")
                        raise

                try:
                    r = api42.get(f'https://api.intra.42.fr/v2/campus/1/users?filter[login]={param}')
                except:
                    print("Error with response")
                    raise

                res = r.json()
                for x in res:
                    if (time_table.get(x['login']) is None):
                        time_table.__setitem__(x['login'], None)

                for user in res:
                    if (time_table[user['login']] is None and user['location'] is not None):
                        time_table.__setitem__(user['login'], time.localtime()[3])
                        queue.put(user)
                        queue.put(index)
                    elif (time_table[user['login']] is not None and user['location'] is None):
                        if ((abs(time.localtime()[3] - time_table[user['login']])) >= 2 or time.localtime()[2] > day):
                            time_table.__setitem__(user['login'], None)
                            day = time.localtime()[2]
                    elif (time_table[user['login']] is not None and user['location'] is not None):
                        time_table.__setitem__(user['login'], time.localtime()[3])
                        print(f'[{j}] {users_table}', end=" : ")
                        print(time_table)
                        j += 1

            if (abs(time.localtime()[4] - time_token) >= 10):
                try:
                    time_token = time.localtime()[4]
                    session['token'] = api42.fetch_token(token_url=token_url, auth=auth)
                except:
                    print("Error with token")
                    raise

            time.sleep(10)
        _thread.exit()

def parser_command(command, dis, _action):
    global users_table
    global action
    index = 0
    start = command.find(" ")
    action = _action

    if (start < 0):
        return (0)

    command = command[start + 1:]
    if (len(command) >= 32):
        return (0)
    if (not command.isalpha()):
        return (0)

    lst_dis = users_table[dis]
    if (action == 1):
        for i in range(0, 10):
            if (lst_dis[i] == command):
                return (0)
            if (lst_dis[i] == ''):
                index = i
                break

    if (action == 1):
        lst_dis.remove('')
        lst_dis.insert(index, command)
    elif ((for_loop(lst_dis, command) >= 0) and action == 2):
        lst_dis.remove(command)
    print(users_table[dis])
    return (1)

def parser(msg):
    global users_table
    global lst_dis
    global lst_user

    author = msg.author
    command_1 = "!add"
    command_2 = "!del"
    command_3 = "!help"
    if (msg.content.find(command_3) >= 0):
        return (3)

    if (users_table.get(author.discriminator) is None):
        users_table.__setitem__(author.discriminator, list())
        list_new = users_table[author.discriminator]
        for i in range(0, 10):
            list_new.append('')

    if (for_loop(users_table[author.discriminator], '') is None):
        return (-1)

    index_1 = msg.content.find(command_1)
    index_2 = msg.content.find(command_2)
    if (index_1 >= 0):
        if (parser_command(msg.content[index_1:], author.discriminator, 1)):
            if (for_loop(lst_dis, author.discriminator) is None):
                lst_dis.append(author.discriminator)
            if (for_loop(lst_users, author.id) is None):
                lst_users.append(author.id)
            return (1)

    elif (index_2 >= 0):
        if (parser_command(msg.content[index_2:], author.discriminator, 2)):
            if (for_loop(lst_dis, author.discriminator) is None):
                lst_dis.append(author.discriminator)
            if (for_loop(lst_users, author.id) is None):
                lst_users.append(author.id)
            return (1)
    return (0)


def init_thread():
    try:
        thread_1 = threading.Thread(target=start_routine)
        return (thread_1)
    except:
        print("Error: at thread creation")
        exit()


def launcher():
    thread_1 = init_thread()
    try:
        thread_1.start()
    except:
        print("Error: at thread starting")
        exit()

    if (thread_1.is_alive() is False):
        exit()
    return (0)

@tasks.loop(seconds=5)
async def alerts_users():
    if (not queue.empty()):
        user = queue.get()
        index = queue.get()
        channel = client.get_channel(chan_id)
        await channel.send(f"<@{lst_users[index]}> {user['login']} in {user['location']}")


@client.event
async def on_ready():
    global chan_id

    for guild in client.guilds:
        if guild.name == GUILD:
            chan = guild.text_channels
            break

    for i in chan:
        if i.name == CHAN_NAME:
            chan_id = i.id
            break

    print(f'Bot start {client.user} connection to {guild.name}(id: {guild.id})\n')
    await client.get_channel(chan_id).send('Hello, command are !add login42, !del login42, !help for futher information')
    alerts_users.start()
    launcher()

@client.event
async def on_message(message):
    global flag
    global users_table

    author = message.author
    channel = client.get_channel(chan_id)
    if (author.bot is True):
        return(0)
    res = parser(message)
    if (res == 1):
        lock.acquire()
        flag = 1
        lock.release()
    elif (res == 3):
        await channel.send(f'<@{author.id}>```\n- !add login42 will add the login to your list and notify you when the login is on campus\
                           \n- !del login42 delete from your list the login\n```')
    elif (res == -1):
        await channel.send(f'<@{author.id}> your list is full, {users_table[author.discriminator]}')

client.run(TOKEN)
