#!/usr/bin/python3
# 初始化mongo数据库
# 创建需要的用户
import os
import secrets
import string

# 可以使用的密码前缀
import sys

PREFIX = string.ascii_letters + string.digits + '_'
# 可以用于生成密码的字符
ALPHABET = PREFIX + '*_'


def generate_pwd(length, count=1):
    """
    生成几组随机字符串
    :param length:随机字符串的长度
    :param count:默认生成一组，可以设置生成多组
    :return:
    """
    res = []
    for cnt in range(count):
        while True:
            prefix = secrets.choice(PREFIX)
            password = prefix + ''.join(secrets.choice(ALPHABET) for i in range(length - 1))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 2
                    and not password.isalnum()):
                res.append(password)
                break
    return res


def generate_sql(sql_filename):
    """
    生成一个临时的执行sql.js
    :return:
    """
    pwd_list = generate_pwd(10, 4)

    sql = f'''
db.createUser({{
    user: "user_admin",
    pwd: "{pwd_list[0]}",
    roles: [
        {{ role: "userAdminAnyDatabase", db: "admin" }}
    ]
}});

db.createUser({{
    user: "db_reader",
    pwd: "{pwd_list[1]}",
    roles: [
        {{ role: "readAnyDatabase", db: "admin" }}
    ]
}});

db.createUser({{
    user: "P32",
    pwd: "{pwd_list[2]}",
    roles: [
        {{ role: "readWrite", db: "P32" }},
        {{ role: "dbAdmin", db: "P32" }}
    ]
}});

db.createUser({{
    user: "P32_CENTER",
    pwd: "{pwd_list[3]}",
    roles: [
        {{ role: "readWrite", db: "P32_CENTER" }},
        {{ role: "dbAdmin", db: "P32_CENTER" }}
    ]
}});
    '''
    # 生成sql文件
    with open(sql_filename, 'w+') as f:
        f.write(sql)
        f.close()


if __name__ == '__main__':
    sql_name = 'init_mongo.js'
    generate_sql(sql_name)
