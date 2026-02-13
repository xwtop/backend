import pymysql

def execute_sql_file(sql_file_path):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='campus_portal',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor = connection.cursor()
        
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    connection.commit()
                    print(f"执行成功: {statement[:50]}...")
                except Exception as e:
                    print(f"执行失败: {e}")
                    print(f"SQL: {statement[:100]}...")
                    connection.rollback()
        
        cursor.close()
        connection.close()
        print("SQL 脚本执行完成！")
        
    except Exception as e:
        print(f"数据库连接失败: {e}")

if __name__ == '__main__':
    execute_sql_file('sql/create_notification_tables.sql')
