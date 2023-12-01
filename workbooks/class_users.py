from datetime import datetime
import mysql.connector


class Users:
    def __init__(self):
        self.users = {}
        self.host="localhost"
        self.user_name="root"
        self.password="17022009Mysql"
        self.connection = self.get_connection()
        self.db_cursor = self.connection.cursor()

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
        self.users[user][dt]['reason'] = 'Other' if len(reason) == 0 else reason

        self.write_db(user, dt, self.users[user][dt]['money'], str(self.users[user][dt]['reason']))

    def write_db(self, user, dt, money, reason):
        print("Writing to DataBase")
        try:
            sql = """
                INSERT INTO product.transactions (
                    name,
                    dt,
                    money,
                    reason
                    ) 
                VALUES (%s, %s, %s, %s)
                """
            val = (user,dt, money, reason)
            self.db_cursor.execute(sql, val)

            self.connection.commit()
        except Exception as e:
            print(f"Cant write to db: {e}")


if __name__=="__main__":
    u = Users()
    u.add_user("Andrei")
    u.add_user("Tuyana")

    u.add_expence('Andrei', '100 hotel', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    u.add_expence('Andrei', '200 hotel', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    u.add_expence('Andrei', '300', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    u.add_expence('Andrei', '-300', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    u.add_expence('Tuyana', '300', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    u.add_expence('Tuyana', '300', datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))