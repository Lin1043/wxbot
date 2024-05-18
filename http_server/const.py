from absl import app,flags

flags.DEFINE_string("wxserver", "http://localhost:8080", "Http service address")
flags.DEFINE_string("wxid", "47331170911@chatroom", "Send message recipient's wxid")