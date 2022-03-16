import psycopg2
import datetime


def create_table():
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id BIGSERIAL  PRIMARY KEY,
    telegram_id integer ,
    full_name VARCHAR (60),
    phone_number VARCHAR (25)
    )
    """)

    conn.commit()
create_table()
def create_table_category():
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS category(
    category_id BIGSERIAL  PRIMARY KEY, 
    name Varchar (255)
    )
    """)

    conn.commit()
create_table_category()
def create_table_products():
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
    product_id BIGSERIAL  PRIMARY KEY, 
    name Varchar (255),
    category_id INTEGER, 
    image VARCHAR (255)
    )
    """)

    conn.commit()
create_table_products()
def create_table_savatcha():
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savatcha(
    savatcha_id BIGSERIAL  PRIMARY KEY, 
    product_id  integer ,
    user_id INTEGER, 
    soni INTEGER , 
    status VARCHAR (25)
    )
    """)

    conn.commit()
create_table_savatcha()
def add_savatcha(user_id, product_id, soni, status):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO savatcha (product_id, user_id, soni, status)
    VALUES (%s, %s, %s, %s)
    """, (product_id, user_id,soni, status))
    conn.commit()


def add_product(product_name, narxi, category):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    INSERT INTO products (name, price, category_id)
    VALUES (%s, %s, (select category_id from category
where name = '{category}'))
    """, (product_name, narxi))
    conn.commit()




def add_users(full_name, phone_number, telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (full_name,phone_number, telegram_id)
    VALUES (%s, %s, %s)
    """, (full_name, phone_number, telegram_id))
    conn.commit()
def get_savatcha(user_id, status):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        select savatcha_id, soni, products.name, products.price from savatcha 
        join products on savatcha.product_id = products.product_id
        where savatcha.status = '{status}' and user_id = {user_id}
        ORDER BY savatcha_id
        """)
    data = cursor.fetchall()
    return data
def minus_savatcha(savatcha_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        update savatcha
        set soni = soni-1
        where savatcha_id = {savatcha_id} 
        
        """)
    conn.commit()
def get_savatcha_quantity(savatcha_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        select soni from savatcha
        where savatcha_id = {savatcha_id} 
        
        """)
    data = cursor.fetchone()
    return data
def delete_savatcha(savatcha_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        delete from savatcha
        where savatcha_id = {savatcha_id} 
        """)
    conn.commit()
def change_savatcha_status(savatcha_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        update savatcha
        set status = 'zakaz'
        where savatcha_id = {savatcha_id} 
        """)
    conn.commit()
def plus_savatcha(savatcha_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        update savatcha
        set soni = soni+1
        where savatcha_id = {savatcha_id} 
        
        """)
    conn.commit()
def add_category(name):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO category (name)
    VALUES (%s)
    """, (name,))
    conn.commit()


def get_categories():
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * from category
        """)
    data = cursor.fetchall()
    return data
def get_products(category_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * from products
        where category_id = {category_id}
        """)
    data = cursor.fetchall()
    return data
def get_product(product_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * from products
        where product_id = {product_id}
        """)
    data = cursor.fetchone()
    return data

def check_user(telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT * from users
    WHERE telegram_id ={telegram_id}
    """)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False
def check_admin(telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT status from users
    WHERE telegram_id ={telegram_id}
    """)
    data = cursor.fetchone()
    if data[0]=='admin':
        return True
    else:
        return False
def check_category(name):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT name from category
    WHERE name ='{name}'
    """)
    data = cursor.fetchone()
    if data:
        return True
    else:
        return False

def get_user(telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT * from users
    WHERE telegram_id ={telegram_id}
    """)
    data = cursor.fetchone()
    return data

def add_achko(telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
        update users
        set achko = achko+1
        where telegram_id = {telegram_id}
        """)
    conn.commit()
def get_achko(telegram_id):
    conn = psycopg2.connect(
        host="ec2-34-192-83-52.compute-1.amazonaws.com",
        database="deqtghb1d51pfq",
        user="pcrkryogpainva",
        password="5e3ecfe5802ff28526a7a9d946df8ed006dca620b87b37579ba5ccbc792a2bf5",
        port="5432"
    )

    cursor = conn.cursor()

    cursor.execute(f"""
    select achko from users
    where telegram_id = {telegram_id}
        """)
    data = cursor.fetchone()
    print(data)
    return data



