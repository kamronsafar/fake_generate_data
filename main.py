import psycopg2
from faker import Faker

fake = Faker()

def connect_to_db(db_name, db_user, db_password):
    try:
        connection = psycopg2.connect(
            host="localhost",
            database=db_name,
            user=db_user,
            password=db_password
        )
        print(f"'{db_name}' bazasiga muvaffaqiyatli ulandik!")
        return connection
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None

def create_table(connection):
    table_name = input("Jadval nomini kiriting: ")
    try:
        cursor = connection.cursor()
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            phone VARCHAR(100),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_query)
        connection.commit()
        print(f"'{table_name}' jadvali muvaffaqiyatli yaratildi!")
    except Exception as e:
        print(f"Jadval yaratishda xatolik yuz berdi: {e}")
    finally:
        cursor.close()

def generate_fake_data(num_records):
    fake_data = []
    for _ in range(num_records):
        name = fake.name()
        email = fake.unique.email()
        phone = fake.phone_number()
        address = fake.address()
        fake_data.append((name, email, phone, address))
    return fake_data

def insert_fake_data(connection, table_name, data):
    try:
        cursor = connection.cursor()
        insert_query = f"""
        INSERT INTO {table_name} (name, email, phone, address) VALUES (%s, %s, %s, %s);
        """
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"{len(data)} ta soxta ma'lumot muvaffaqiyatli kiritildi!")
    except Exception as e:
        print(f"Soxta ma'lumot kiritishda xatolik yuz berdi: {e}")
    finally:
        cursor.close()

def fetch_data(connection, table_name):
    try:
        cursor = connection.cursor()
        fetch_query = f"SELECT * FROM {table_name} LIMIT 10;"
        cursor.execute(fetch_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Ma'lumotlarni o'qishda xatolik yuz berdi: {e}")
    finally:
        cursor.close()

def main():
    db_name = input("Ma'lumotlar bazasi nomini kiriting: ")
    db_user = input("Foydalanuvchi nomini kiriting: ")
    db_password = input("Parolni kiriting: ")

    connection = connect_to_db(db_name, db_user, db_password)
    if connection:
        create_table(connection)

        table_name = input("Jadval nomini kiriting: ")
        num_records = int(input("Yaratmoqchi bo'lgan soxta ma'lumotlar sonini kiriting: "))
        fake_data = generate_fake_data(num_records)

        insert_fake_data(connection, table_name, fake_data)
        print(f"'{table_name}' jadvalidan 10 ta yozuv:")
        fetch_data(connection, table_name)
        connection.close()

if __name__ == "__main__":
    main()
