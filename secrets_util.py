# 生成随机密码
import secrets
import string

# 可以用于生成密码的字符
ALPHABET = string.ascii_letters + string.digits + '*_'
# 可以使用的密码前缀
PREFIX = string.ascii_letters + string.digits + '_'


def generate(length, count=1):
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
