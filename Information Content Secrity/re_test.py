import re

email_re = """^[\w\.-]+@[\w\.-]+.[\w\.-]+"""
ipv4_re = """((\d{1,2})|(1\d{2})|(2[0-4]\d)|( 25[0-5]))(.(\d{1,2})|(1\d{2})|(2[0-4]\d)|( 25[0-5])){3,}"""

my_email = '0505yahweh@gmail.com'
my_ipv4 = '192.168.10.334'

def re_email():
    print(re.match(email_re,my_email).group())

def re_ipv4():
    print(re.match(ipv4_re,my_ipv4).group())

if __name__ =='__main__':
    re_ipv4()