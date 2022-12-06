
import mysql.connector


conn = mysql.connector.connect(
    host='101.132.102.164',
    user='being_filtered',
    password='nzj0721',
    database='being_filtered',
)


cursor = conn.cursor()


str = input('请输入包名，用于删除已经添加的包：')


sql = "DELETE FROM table_name WHERE str = %s"
cursor.execute(sql, (str,))
conn.commit()

cursor.close()
conn.close()
