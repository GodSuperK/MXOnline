__author__ = "GodSuperK"
__date__ = "18-10-18 上午9:04"

from django.core import mail

from users.models import EmailVerifyCode
from utils.basic_settings import EMAIL_FROM
import random


def send_email(email, send_type="register"):
    """ 发送邮箱链接
    激活链接原理：
    1. Server 随机生成一段随即字符串，并保存到数据库，将其和url地址连接起来
    2. 将邮箱验证链接发送到用户的邮箱
    3. 当用户点击 url 链接后，进入到 Server 的路由匹配，Server 提取出随机字符串
    4. 将邮箱和随机字符串和数据库中的字段进行对比
    5. 如果一致，则邮箱激活成功
    6. 如果不一致，则邮箱激活失败
    :param email: 目标邮箱
    :param send_type: `register` 表示是激活链接 `forget` 表示是找回密码链接
    :return:
    """
    # 1. 先实例化一个EmailVerifyCode对象，将其保存到数据库，供后面验证一致性
    email_record = EmailVerifyCode()
    email_record.email = email
    if send_type in ["register", "forget"]:
        email_record.send_type = send_type
    email_record.code = generate_random_str()
    email_record.save()

    # 2. 定义邮件 e 的主题和消息
    e_subject = ""
    e_message = ""

    if send_type == "register":
        e_subject = "慕学在线网注册激活链接"
        e_message = "请点击下面的链接激活您的账户 http://127.0.0.1:8000/active/{}/".format(email_record.code)
    elif send_type == "forget":
        # TODO 找回密码链接
        pass
    else:
        pass

    # 3. 使用django提供的发送邮件函数 django.core.mail.send_mail
    # 需要提前配置好 邮件发送者的信息
    send_status = mail.send_mail(subject=e_subject,
                                 message=e_message,
                                 from_email=EMAIL_FROM,
                                 recipient_list=[email, ])
    return send_status


def generate_random_str(length=8):
    """
    生成随机字符串
    :param length: int 随机字符串字符串长度
    :return: str s
    """

    # 生成chars可选字符序列的算法
    # chars_li = [chr(i) + chr(i).lower() for i in range(65, 91)]
    # chars_li += [str(i) for i in range(10)]
    # chars_str = ''.join(chars)
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"

    # 每次循环随机生成一个整数（避免出界，需要在chars的长度范围内）
    # 然后索引取出，循环次数由随机字符串长度决定
    s = ''.join([chars[random.randint(0, len(chars) - 1)] for i in range(length)])
    return s
