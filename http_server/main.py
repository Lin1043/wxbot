from flask import Flask, request
from absl import logging
from absl import app,flags
import requests
import re
import random
import const
import json

# 创建 Flask 应用程序实例
app = Flask(__name__)
FLAGS = flags.FLAGS

def send_msg(wxid, str):
    data = {
      "wxid": wxid,
      "content": str,
    }
    headers = {
      "Content-Type": "application/json"
    }
    print(data)
    ret = requests.post(url='http://127.0.0.1:8080/api/sendtxtmsg', headers=headers, data=json.dumps(data))
    if ret.status_code == 200:
        print("success: %s" % (ret.text))
    else:
        print("faild: %s" % (ret.text))

def command_dice():
  random_player = random.randint(1, 4)
  random_bot = random.randint(3, 6)
  result_str = "你的点数是 {}，bot的点数是 {}\n".format(random_player , random_bot)
  if random_player > random_bot:
    result_str += "🤫让你一把"
  elif random_player < random_bot:
    result_str += "🤣你输了!"
  else:
    result_str += "🤭平手"
  return result_str
    

def parse_command(user_input):
  pattern = r'(\w+)(?:\s(.*))?'  # 正则表达式模式，匹配命令和可选参数
  match = re.match(pattern, user_input)
  if match:
    command = match.group(1)  # 提取命令
    arguments = match.group(2)  # 提取参数
    if arguments:
      arguments = arguments.split()  # 将参数字符串拆分为参数列表
    else:
      arguments = []
    return command, arguments
  else:
    return None, []

command_dict = {
  'dice': command_dice
}

# 定义路由和处理函数
@app.route('/callback', methods=['POST'])
def callback_main():
  dic = request.get_json()
  if dic['data'][0]['StrContent'][0] == '/':
    command, aruguments = parse_command(dic['data'][0]['StrContent'][1:])
    if command in command_dict:
      command_func = command_dict[command]
      result_str = command_func()
      # print(dic['data'][0])
      send_msg(dic['data'][0]['StrTalker'], result_str)
  return {"code": 200, "msg": "pass"}
  
# 启动应用程序
if __name__ == '__main__':
  app.run(port = 8081)
  