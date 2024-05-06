import sqlite3, sys


# a comment
print("Start of script")

DB = './sqlite0.db'
conn = sqlite3.connect(DB)

cursor = conn.cursor()

# print(len(sys.argv))
# print(sys.argv[1])
# print(sys.argv[1] == "create")

if sys.argv[1] == "create":
    # Create tables for database
    print("Creating tables...")
    create_user_sql = "CREATE TABLE user (id INTEGER PRIMARY KEY, username text, password text , forename text, surname text)"
    result = cursor.execute(create_user_sql)

    create_avail_service = "CREATE TABLE avail_service (id INTEGER PRIMARY KEY, name text, description text, image_name text, thumbpath text)"
    result = cursor.execute(create_avail_service)

    create_user_service_sql = "CREATE TABLE user_service (id INTEGER PRIMARY KEY, id_user number, id_avail_service number, container_id text, state text, port number, ip text, subdomain text)"
    result = cursor.execute(create_user_service_sql)

    # I think this is needed to write the data to the database?
    conn.commit()

    print("...done!")

if sys.argv[1] == "insert":
    print("Inserting test data...")

    insert_user_sql = "INSERT INTO user VALUES(NULL, 'me@me.com', 'wordpass', 'Arthur', 'Pewty')"
    cursor.execute(insert_user_sql)

    insert_avail_service_sql = "INSERT INTO avail_service VALUES(NULL, 'WordPress', 'The leading blogging and CMS platform on the Internet', 'wordpress', 'wordpress(1).svg')"
    cursor.execute(insert_avail_service_sql)

    conn.commit()

    getuserid = "SELECT id from user where username = 'me@me.com'"
    useridrecord = cursor.execute(getuserid)
    userid = useridrecord.fetchone()
    print( "User id: " + str(userid[0]) )

