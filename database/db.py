import pymysql


# connection to db


def connection(host, user, password, db):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except Exception as e:
        print(f"Error occured {e}")

    return connection
