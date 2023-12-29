from mcstatus import JavaServer
import os
import sqlite3
import time
import configparser
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

print('Скрипт запущен!')
print('Идет проверка онлайна...')

connection = psycopg2.connect(database="mineshare",
                              user=os.getenv("DATABASE_USER"),
                              password=os.getenv("DATABASE_PASSWORD"),
                              host="mineshare.top",
                              port="5432")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()

delay = 0

while True:

    time.sleep(5)
    print("-" * 20)

    try:
        cursor.execute(f"SELECT ip, port FROM servers_servers")

        lst = cursor.fetchall()

    except Exception as ex:
        print("ERROR")
        break

    for server in lst:
        print(server[0] + ":" + server[1])

        try:

            if int(server[1]) == 25565:
                server_check = JavaServer.lookup(server[0])
            else:
                server_check = JavaServer.lookup(server[0] + ":" + server[1])

            status = server_check.status()

            cursor.execute(
                f"UPDATE servers_servers SET current_players = {int(status.players.online)}, max_players = {int(status.players.max)} , online_status = TRUE"
                f" WHERE ip LIKE '{str(server[0])}'")

            connection.commit()

        except Exception as ex:

            cursor.execute(
                f"UPDATE servers_servers SET current_players = 0, max_players = 10 , online_status = FALSE"
                f" WHERE ip LIKE '{str(server[0])}'")

            connection.commit()

    print("-" * 20)

    '''
    try:
        cursor.execute(f"SELECT id, date FROM party_invitations")

        lst = cursor.fetchall()

    except Exception as ex:
        print("ERROR")
        break

    for party in lst:

        local = pytz.timezone("Europe/Moscow")
        local_dt = local.localize(datetime.datetime.now(), is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        if (utc_dt - party[1]).days >= 2:
            print(str(party[1]) + " [PARTY] [STOP]")

            try:
                cursor.execute(f"DELETE FROM party_invitations WHERE id = {party[0]};")

                connection.commit()

            except Exception as ex:
                break
        else:
            print(str(party[1]) + " [PARTY] [OK]")

    print("-" * 20)
    '''

    try:
        cursor.execute(f"SELECT id, premium_regdate FROM servers_servers")

        lst = cursor.fetchall()

    except Exception as ex:
        print("ERROR")
        break

    for premium in lst:

        local = pytz.timezone("Europe/Moscow")
        local_dt = local.localize(datetime.datetime.now(), is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)

        if (utc_dt - premium[1]).days > 30:
            print(str(premium[1]) + " [PREMIUM] [STOP]")

            try:
                cursor.execute(f"UPDATE servers_servers SET premium_status = FALSE WHERE id = {premium[0]};")

                connection.commit()

            except Exception as ex:
                pass

        else:
            print(str(premium[1]) + " [PREMIUM] [OK]")

    if delay == 1000:
        delay = 0

        try:
            cursor.execute(f"SELECT id, rate FROM servers_servers")

            lst = cursor.fetchall()

        except Exception as ex:
            print("ERROR")
            break

        for server in lst:
            print(server[0] + " [RATE]")

            try:

                cursor.execute(
                    f"UPDATE servers_servers SET rate_old = {int(server[1])}"
                    f" WHERE id LIKE '{server[0]}'")

                connection.commit()

            except Exception as ex:
                pass

        print("-" * 20)

    delay += 1