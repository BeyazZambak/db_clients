import psycopg2

def create_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers(
        client_id SERIAL UNIQUE PRIMARY KEY,
        first_name VARCHAR(60),
        last_name VARCHAR(60),
        email VARCHAR(60)
        );
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES customers(client_id),
        phone VARCHAR(12)
        );
        """)
    conn.commit()

def drop_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE phones;
        DROP TABLE customers;
        """)
    print('таблицы удалены')
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO customers(first_name, last_name, email) 
    VALUES(%s, %s, %s);
    """, (first_name, last_name, email))
    cur.execute("""
    INSERT INTO phones(client_id, phone) 
    VALUES((SELECT client_id from customers
    where email = %s), %s);
    """, (email, phones))
    conn.commit()
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())


def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
    UPDATE phones SET phone=%s 
    WHERE client_id=%s;
    """, (phone, client_id))
    conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    cur = conn.cursor()
    cur.execute("""
    UPDATE customers SET first_name=%s, last_name=%s, email=%s 
    WHERE client_id=%s;
    """, (first_name, last_name, email, client_id))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())
    cur.execute("""
    UPDATE phones SET phone=%s 
    WHERE client_id=%s;
    """, (phones, client_id))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())


def delete_phone(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
    UPDATE phones SET phone=%s 
    WHERE client_id=%s;
    """, ('Null', client_id))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())


def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM phones 
    WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM phones;
    """)
    print(cur.fetchall())
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM customers 
    WHERE client_id=%s;
    """, (client_id,))
    cur.execute("""
    SELECT * FROM customers;
    """)
    print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM customers c 
    JOIN phones p ON c.client_id = p.client_id 
    WHERE first_name=%s OR last_name=%s OR email=%s OR p.phone=%s;
    """, (first_name, last_name, email, phone))
    print(cur.fetchall())


with psycopg2.connect(database="db_custumers", user="postgres", password="12345") as conn:
    drop_tables(conn)
    create_db(conn)
    add_client(conn, 'Anna', 'Ann', 'a1@mail.com', '111222334')
    add_client(conn, 'Boris', 'Bori', 'b2@mail.com', '+2223334455')
    add_client(conn, 'Celen', 'Cele', 'cel3@mail.com')
    add_client(conn, 'Dima', 'Dim', 'd4@mail.com')
    add_client(conn, 'Ivan', 'Iva', 'i5@mail.com', '+55556432221')
    print("Stop--------------------------------------creation")
    add_phone(conn, 3, '+3345643211')
    add_phone(conn, 4, '+444555543')
    change_client(conn, 1, 'Artem', 'Arte', 'a2@mail.com', '+11234567')
    change_client(conn, 4, first_name='Ivan', last_name='Petrov', email='ivan.petrov@gmail.com', phones='+456789')
    delete_phone(conn, 1)
    delete_client(conn, 4)
    print("Start--------------------------------------finding")
    find_client(conn, first_name='Celen')
    find_client(conn, last_name='Dim')
    find_client(conn, email='b2@mail.com')
    find_client(conn, phone='+55556432221')