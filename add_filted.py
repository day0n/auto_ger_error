
import mysql.connector


conn = mysql.connector.connect(
    host='101.132.102.164',
    user='being_filtered',
    password='nzj0721',
    database='being_filtered',
)

cursor = conn.cursor()


str = input('请输入已经被过滤的包（该包已被解决或者该包无法解决）：')


sql = "INSERT INTO table_name(str) VALUES (%s)"
cursor.execute(sql, (str,))
conn.commit()

cursor.close()
conn.close()
