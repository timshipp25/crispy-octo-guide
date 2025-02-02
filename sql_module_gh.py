import aiomysql
import os
from datetime import datetime

DB_SECRET = os.environ["DB_SECRET"]
US_SECRET = os.environ["US_SECRET"]
PW_SECRET = os.environ["PW_SECRET"]

async def update_last_used(inip):
    connection = await aiomysql.connect(
        host='185.127.17.25',
        port=3306,
        user=US_SECRET,
        password=PW_SECRET,
        db=DB_SECRET
    )
    
    async with connection.cursor() as cursor:
        query = "UPDATE ip_addresses SET last_used = %s WHERE ip_address = %s"
        current_datetime = datetime.now()
        await cursor.execute(query, (current_datetime, inip))
        await connection.commit()
        
    connection.close()

async def update_ip_success_fail(inip,type):
    connection = await aiomysql.connect(
        host='185.127.17.25',
        port=3306,
        user=US_SECRET,
        password=PW_SECRET,
        db=DB_SECRET
    )
    
    async with connection.cursor() as cursor:
        if type == "success":
            query = "UPDATE ip_addresses SET success = success + 1, fail_streak = 0 WHERE ip_address = %s"
        if type == "fail":
            query = "UPDATE ip_addresses SET fail = fail + 1, fail_streak = fail_streak + 1 WHERE ip_address = %s"
        current_datetime = datetime.now()
        await cursor.execute(query, (inip))
        await connection.commit()
        
    connection.close()

async def fetch_ip_addresses(fail_streak):
    print("Fail Streak: ",fail_streak)

    connection = await aiomysql.connect(
        host='185.127.17.25',
        port=3306,
        user=US_SECRET,
        password=PW_SECRET,
        db=DB_SECRET
    )
    
    async with connection.cursor() as cursor:
        #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' order by last_used asc limit 1"
        #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND (fail/success)*100 < 50 order by last_used asc limit 1"
        #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 1 AND (fail/success)*100 < 50 order by last_used asc limit 1"
        if fail_streak == 0:
            #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak = 0 AND (fail/success)*100 < 50 order by last_used asc limit 1"
            #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 2 AND (fail/success)*100 < 50 order by fail_streak ASC, last_used asc limit 1"
            #query = ("SELECT ip_address"
            #         " FROM ip_addresses"
            #         " WHERE current_flag = 'Y'" 
            #         " AND fail_streak <= 2"
            #         " AND SUBSTRING_INDEX(ip_address, '.', 1) = (SELECT first_octet FROM ("
            #         " SELECT SUBSTRING_INDEX(ip_address, '.', 1) as first_octet, sum(fail_streak) AS sumstreak, COUNT(*) AS cnt"
            #         " FROM ip_addresses"
            #         " WHERE current_flag = 'Y'"
            #         " GROUP BY first_octet"
            #         " order by sumstreak ASC, cnt DESC"
            #         " LIMIT 1) xxx)"
            #         " order by fail_streak ASC, last_used asc limit 1")
            query = ("SELECT ip_address FROM ("
                     " SELECT ip_address, last_used, (fail/success)*100 AS pct, fail_streak"
                     " FROM ip_addresses"
                     " WHERE current_flag = 'Y'"
                     " AND fail_streak <= 2"
                     " ORDER BY fail_streak ASC, last_used DESC"
                     " LIMIT 1) xxx")
        else:
            #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 2 AND (fail/success)*100 < 50 order by last_used asc limit 1"
            #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 2 AND (fail/success)*100 < 50 AND last_used < NOW() - INTERVAL 65 MINUTE order by fail_streak DESC, last_used ASC LIMIT 1"
            #query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 2 AND last_used < NOW() - INTERVAL 65 MINUTE order by fail_streak DESC, last_used ASC LIMIT 1"
            query = "SELECT ip_address FROM ip_addresses WHERE current_flag = 'Y' AND fail_streak <= 2 ORDER BY last_used ASC LIMIT 1"
        print("IP Query: ", query)
        await cursor.execute(query)
        results = await cursor.fetchall()
        
    connection.close()
    return results

async def fetch_user_agents():

    connection = await aiomysql.connect(
        host='185.127.17.25',
        port=3306,
        user=US_SECRET,
        password=PW_SECRET,
        db=DB_SECRET
    )
    
    async with connection.cursor() as cursor:
        query = "SELECT user_agent FROM user_agents WHERE current_flag = 'Y' ORDER BY RAND() * UNIX_TIMESTAMP() LIMIT 1"
        #print("IP Query: ", query)
        await cursor.execute(query)
        results = await cursor.fetchall()
        
    connection.close()
    return results[0]
