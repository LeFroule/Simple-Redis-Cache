import psycopg2
import redis
from config import password, host, user, db_name
import json

def get_my_friends():
    try:
        with psycopg2.connect(
            host=host,
            password=password,
            user=user,
            database=db_name
        ) as connection:
            connection.autocommit = True

            with redis.Redis() as redis_client:
                cache_value = redis_client.get('user_friends')
                if cache_value is not None:
                    print('Взято из кеша')
                    return json.loads(cache_value.decode('utf-8'))

                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT id, name from my_friends;"""
                    )
                    result = cursor.fetchall()
                result_json = json.dumps(result)
                redis_client.set('user_friends', result_json, ex=300)
                print('Взято из БД')
                return result
    except Exception as ex:
        print("[ERROR] An error occurred:", ex)

if __name__ == '__main__':
    print(get_my_friends())
