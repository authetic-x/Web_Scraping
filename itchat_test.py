import itchat
import time


itchat.auto_login(hotReload=True)


boom_name = input('Input the target name: ')
message = input('Input the message you wanna send: ')

boom_obj = itchat.search_friends(remarkName=boom_name)[0]['UserName']

while True:
    time.sleep(0.5)
    print('booming...')
    itchat.send_msg(msg=message, toUserName=boom_obj)