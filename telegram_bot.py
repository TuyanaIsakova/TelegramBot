from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor 
from datetime import datetime
import os 
import mysql.connector


class Users:
    def __init__(self):
        self.users = {}
        self.host="localhost"
        self.user_name="root"
        self.password="17022009Mysql"
        self.connection = self.get_connection()
        self.db_cursor = self.connection.cursor()
        self.token = "6802410302:AAGx_fgsySpTy5yCtZN35weSp-gnpFaV2pc"

    def get_connection(self):
        return mysql.connector.connect(
                    host= self.host,
                    user=self.user_name,
                    password=self.password
                )

    def __str__(self):
        return str(self.__dict__)
    
    def add_user(self, user):
        print(f"Adding user {user}")
        if not self.get_user(user):
            self.users[user] = {}

    def get_user(self, user):
        print(f"Getting user {user}")
        user_exists = False
        if user in self.users:
            user_exists = True
        return user_exists
    
    def add_expence(self, user, transaction, dt):
        print("Parsing expences")
        self.users[user][dt] = {}
        self.users[user][dt]['money'] = transaction.split()[0]
        reason = transaction.split()[1:]
        self.users[user][dt]['reason'] = 'Other' if len(reason) == 0 else ' '.join([i for i in reason])

        self.write_db(user, dt, self.users[user][dt]['money'], str(self.users[user][dt]['reason']))

    def write_db(self, user, dt, money, reason):
        print("Writing to DataBase")
        session_id = self.get_session_id()

        try:
            sql = """
                INSERT INTO product.transactions (
                    session_id,
                    name,
                    dt,
                    money,
                    reason
                    ) 
                VALUES (%s, %s, %s, %s, %s)
                """
            val = (session_id, user,dt, money, reason)
            self.db_cursor.execute(sql, val)

            self.connection.commit()
        except Exception as e:
            print(f"Cant write to db: {e}")

    def get_total_by_users(self, type):
        print("Getting total sum")
        session_id = self.get_session_id()
        self.db_cursor.execute(f"""
            SELECT  {type},
                    sum(money) as total
            FROM    product.transactions
            WHERE   session_id = {session_id}
            GROUP BY {type}
            """)
        return self.db_cursor.fetchall()
    
    def get_total(self):
        print("Getting total sum")
        session_id = self.get_session_id()
        self.db_cursor.execute(f"""
            SELECT  sum(money) as total
            FROM    product.transactions
            WHERE   session_id = {session_id}                               
            """)
        return self.db_cursor.fetchall()    
    
    def create_session(self, session_name = ""):
        print("Creating session")
        if session_name == "":
            session_name = f"Travel {datetime.now().strftime('%Y-%m-%d')}"
        try:
            sql = f"""
                UPDATE product.sessions 
                SET    is_active = False,
                       dt_end = '{datetime.now().strftime("%Y-%m-%d")}'
                WHERE  is_active = True
                """
            self.db_cursor.execute(sql)

            self.connection.commit()
        except Exception as e:
            print(f"Cant update session: {e}")

        try:    
            sql = """
                INSERT INTO product.sessions (
                    session_name,
                    is_active,
                    dt_start
                    ) 
                VALUES (%s, %s, %s)
                """
            val = (session_name, True, datetime.now().strftime("%Y-%m-%d"))
            self.db_cursor.execute(sql, val)

            self.connection.commit()
        except Exception as e:
            print(f"Cant create session: {e}")

        return self.get_active_session_id()

    def get_active_session_id(self):
        print("Getting active session")
        self.db_cursor.execute("""
            SELECT  id
            FROM    product.sessions
            WHERE   is_active = True
            """)
        return self.db_cursor.fetchall()
    
    def get_session_id(self):
        print("Getting session_id")
        session_list = self.get_active_session_id()

        if len(session_list) > 0:
            session_id, = session_list[0]
        else:
            session_id, = self.create_session()[0]

        return session_id      

if __name__=="__main__":
    u = Users()

    bot = Bot(token=u.token)
    dp = Dispatcher(bot)


    @dp.message_handler()
    async def echo_send(message : types.Message):
 
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        skip_message = False
        txt = ""
        if message.text.lower() == 'Hi'.lower():
            txt = 'You too'
        elif message.text.lower() == 'total'.lower():
            for i in u.get_total_by_users('name'):
                txt += f"{i[0]}: {i[1]}\n"
            for i in u.get_total():
                txt += f"\nTotal: {i[0]}"
        elif message.text.lower() == 'details'.lower():
            for i in u.get_total_by_users('reason'):
                txt += f"{i[0]}: {i[1]}\n"
            for i in u.get_total():
                txt += f"\nTotal: {i[0]}"
        elif 'start' in message.text.lower():
            session_name = message.text.replace('start','')
            u.create_session(session_name)    
            txt = "Travel session created"         
        else:
            skip_message = True
            u.add_user(message.from_user.full_name) 
            u.add_expence(message.from_user.full_name, message.text, dt)

        if not skip_message:
            await message.answer(txt)	

    executor.start_polling(dp, skip_updates=True)
