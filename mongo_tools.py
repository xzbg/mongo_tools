# ！/usr/bin/python3
# 管理mongo数据的备份、还原、删除
import os
import re
import sys
import shutil

from pymongo import database, MongoClient


class MongoUrl:
    """
       解析数据库配置文件
    """

    def __init__(self, filename):
        self.uri = None
        self.user = None
        self.pwd = None
        self.primary_ip = None
        self.dbname = None
        self.parse(filename)

    def parse(self, opts):
        """
        解析数据库配置文件
        :param opts:
        :return:
        """
        file = open(opts, mode='r')
        lines = file.readlines()
        opts_cfg = ""
        for line in lines:
            opts_cfg += line.strip()
        self.uri = re.findall(r'<<"(.+)">>', opts_cfg)[0]
        # 找到主节点的ip，还原只能使用主节点连接
        r_idx = self.uri.find('mongodb://')
        ip_info = None
        if r_idx != - 1:
            ip_info = self.uri[r_idx + len('mongodb://'):]
        # 这里找最后一个，因为密码中可能会包含特殊字符@
        r_idx = ip_info.rfind('@')
        if r_idx != -1:
            user_info = ip_info[0:r_idx]
            ip_info = ip_info[r_idx + 1:]
            user_info_list = user_info.split(':')
            self.user = user_info_list[0]
            self.pwd = user_info_list[1]
        r_idx = ip_info.rfind('?')
        if r_idx != -1:
            ip_info = ip_info[0:r_idx]
        r_idx = ip_info.find(',')
        if r_idx != -1:
            ip_info = ip_info[r_idx:]
        info_list = re.findall(r'(.+:\d+)/(\w+)', ip_info)[0]
        print(info_list)
        self.primary_ip = info_list[0]
        self.dbname = info_list[1]


def dump(uri: str, backup_dir: str):
    """
    数据库备份
    :param uri: 数据库链接的路径
    :param backup_dir: 数据库备份的目录
    :return:
    """
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    command = f'mongodump -vvvv --uri="{uri}" --out={backup_dir} && echo dump finished'
    os.system(command)


def restore(uri: str, backup_dir: str, user: str, pwd: str, dbname: str):
    """
    数据库还原
    :param uri: 数据库链接的路径，这里只能向数据库主节点进行数据还原，不然会出错
    :param backup_dir: 数据库备份的目录
    :param user: 还原使用的用户名
    :param pwd: 用户名密码
    :param dbname: 需要还原到的数据库名
    :return:
    """
    command = f'mongorestore --drop -vvvvv -h "{uri}"' \
              f' -u "{user}" -p "{pwd}" ' \
              f'--authenticationDatabase admin ' \
              f'--objcheck --nsInclude={dbname}.* ' \
              f'--dir="{backup_dir}"'
    print("数据库恢复开始！", command)
    os.system(command)
    print("数据库恢复完成")


class MongoConnect:
    """
    数据库连接对象
    """

    def __init__(self, uri: str):
        """
        初始化数据库链接
        :param uri: 数据库连接url，格式为mongodb://<user>:<pwd>@uri”
        """
        try:
            self.con: MongoClient = MongoClient(uri)
        except ConnectionError as err:
            print("数据库连接失败！", err)

    def close(self):
        """
        断开数据库链接
        :return:
        """
        try:
            self.con.close()
        except Exception as e:
            print("数据库连接断开失败", e)

    def get_database(self, dbname: str = None) -> database.Database:
        """
        得到指定的数据库
        :param dbname:
        :return:database.Database
        """
        if dbname is None:
            return self.con.get_default_database()
        else:
            return self.con.get_database(dbname)

    def drop_database(self, dbname: str = None):
        """
        销毁数据库
        :param dbname: 数据库名称
        :return:
        """
        if dbname is None:
            db = self.get_database()
            self.con.drop_database(db)
        else:
            self.con.drop_database(dbname)


if __name__ == '__main__':
    # 需要输入一个项目目录
    project_path = sys.argv[1]
    url_file = f"{project_path}/boot/mongo.opts"
    backup_path = f"{project_path}/_mongodump"
    url = MongoUrl(url_file)  # 默认的连接路径
    print(r'Please choose the type of need operation')
    print(r'0. drop database')
    print(r'1. dump database')
    print(r'2. restore database')
    operate = input('input:')
    if operate == '0':
        con = MongoConnect(url.uri)
        con.drop_database()
        con.close()
        print("drop database success!")
    elif operate == '1':
        dump(url.uri, backup_path)
    elif operate == '2':
        restore(url.primary_ip, backup_path, url.user, url.pwd, url.dbname)
