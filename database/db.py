import pymysql


# connection to db
def db_connection(host, user, password, db):
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
