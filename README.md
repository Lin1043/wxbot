# wxbot - 微信聊天机器人
> 适用于微信（WeChat **3.9.8.25** | 3.9.8.15 | 3.9.7.29）
> 可在Windows PC微信 **设置** - **关于微信** - **版本信息** 中获取您当前的微信版本，如果您当前的微信版本不在上述可用的版本列表中，请至下方 **3、可用版本微信安装包获取** 选择最新版微信重新安装使用

**未经过大量测试，存在封号风险！**

## 免责声明
**本仓库发布的内容，仅用于学习研究，请勿用于非法用途和商业用途！如因此产生任何法律纠纷，均与作者无关！**
**无任何后门、木马，也不获取、存储任何信息，请大家在国家法律、法规和腾讯相关原则下学习研究！**
**不对任何下载和使用者的任何行为负责，请于下载后24小时内删除！**

## 关于免注
> 因注入版本(注入DLL，功能多点)被举报了后续不再更新了，和使用方式（`READNE.md`）一起放在`wxbot-injector`目录下了
> 现在只更新免注版本了 **（免注只是不注入DLL了，并不是真的不需要注入！）**


## 1、运行
bin目录下`wxbot-sidecar.exe`，直接运行即可
* **wxbot-sidecar.exe (bin/wxbot-sidecar.exe)**

多种情况说明：
* 当无微信进程在运行时会主动拉起微信
* 如微信已运行（非多开模式下）会获取当前运行中的微信进程号
* 您也可以使用`-p`参数手动指定微信进程号

```
> .\wxbot-sidecar.exe -p 30568
> .\wxbot-sidecar.exe --help
Usage: wxbot-sidecar.exe [ OPTIONS ] [ VALUE ]

Options:
        -p, --pid  [ pid ]              Specify the process number for injection
        -c, --config  [ path ]          Specify the configuration file path
        -a, --address                   Specify listening address (e.g. 0.0.0.0:8080)
        -w, --wechat                    Ignoring the -p parameter will pull up a WeChat instance. Please use this -w parameter after lifting the multi opening restriction!
        -s, --silence                   Enable silent mode(without popping up the console)
        -m, --multi                     Remove WeChat multi instance restrictions (allowing multiple instances)
        -h, --help                      Output Help Information
```
**目前免注入版本仅支持 3.9.8.25，请务必确认版本号正确**

### Linux下Docker部署
> 在 `Linux` 下使用 `Docker` 部署 `Wechat` + `wxbot` 全部流程已经跑通了，后面我会构建成一个公共镜像供大家使用（但使用 `wine` 运行 `WeChat` 的稳定性如何到时还需要大家帮忙一起测试了）

## 2、使用
> **如果您在使用时遇到了缺少运行库的报错**
> **如：由于找不到 `MSVCP140.dll`，无法继续执行代码。重新安装程序可能会解决此问题**
> **如果您遇到了此类问题可通过文档最下方的网盘链接中下载 *微软常用运行库.exe* 进行安装**
> [或通过此链接下载最新微软常用运行库合集解决](https://www.lanzoux.com/b0dptvb0f)

### 2.1、多开
* 如果您只有一个微信实例在运行并需要注入或快速上手，那么您无需关心其它参数，直接双击运行即可
* 如果您需要多开微信，那么请先使用`wxbot-sidecar.exe -m`解除微信多开限制（执行时机并不重要，您可以在任何情况下去解除多开限制）
* 如果您已经解除了多开限制，并希望对运行中的多个微信实例进行注入，那么现在您使用`-a`参数指定每个实例监听的地址（格式为：`ip:port`）
* **请注意！如果您在多开模式下希望使用`wxbot-sidecar.exe`拉起新的微信实例，那么您需要为每个微信新实例加上`-w`参数，例如：`wxbot-sidecar.exe -w` 或是 `wxbot-sidecar.exe -w -a 0.0.0.0:8081`**

### 2.2、配置文件
> 配置文件支持两种方式分别是：
> * **[wxid].json：** 支持登陆用户wxid的专属配置文件，如你登陆的微信用户wxid是abc，且微信根目录下有abc.json配置文件的话则优先读取此配置文件！
> * **wxbot.json：** 这是默认的配置文件（如果有的话）
>
> **Tips：**
> **配置文件路径为 `wxbot-sidecar.exe` 所在的同级目录，或使用`-c`参数指定配置文件路径**
> **配置文件为json格式，默认不自动创建！**
> **配置文件优先级：[wxid].json > wxbot.json > 无配置文件时的默认值**
> 
> **这样设计配置文件优先级是为了适配微信多开而不那么优雅的实现方式，具体您可以看 `4. 多开高级用法` 了解更多**

#### 2.2.1、配置文件示例
```json
{
    "addr": "0.0.0.0:8080",
    "sync-url": {
        "general-msg": [
            {
                "timeout": 3000,
                "url": "http://localhost:8081/callback"
            }
        ]
    },
    "authorization": {
        "enable": false,
        "users": [
            {
                "user": "admin",
                "password": "123",
                "token": "token123"
            },
            {
                "user": "user",
                "password": "321",
                "token": "token321"
            }
        ]
    },
    "root-dir": "D:\\WeChat",
    "log": {
        "level": "info"
    }
}
```
* **addr:** wxbot服务监听地址（固定为ip:port形式）
* **sync-url：** http回调地址列表（建议通过下面的/sync-url接口修改，不要手动修改）
  * **general-msg：**
    * **url：** 回调url
    * **timeout：** 回调超时时间

**Tips：这里的`http://localhost:8081/callback`只是一个例子，而并非必须的，如果您未启动此回调地址，那么请删除它，否则一个不可达地址将会影响后续每个回调的到达时间！**
* **authorization：** 鉴权 **鉴权使用方法请您至下方 `5、鉴权` 了解更多**
  * **enable：** 是否开启鉴权
  * **users：** 用户列表（这是一个对象数组）
    * **user：** 用户名
    * **password：** 密码
    * **token：** 登陆后的token
* **root-dir：** 发送和获取的泛文件（图片、语音、视频、文件）存放路径，同时也会启动一个文件服务端，默认值是微信安装目录下
* **log** 
  * **level：** 日志级别：分为 **trace**、**debug**、**info**、**warn**

**实际上配置文件中的所有字段都是非必填项，它们都可以独立存在，如果您不需要配置任何项，那么请不要创建它！**

### 2.2、路由列表
> 响应信息
> **固定为JSON格式响应：** {"code": 200, data: xxxx, "message": "xxx"}
> * **code：** 固定200
> * **message：** 成功为success，失败为faild，或是其它错误提示信息
> * **data:**  根据请求接口不同数据不同，无特别描述时下面的请求接口返回字段全部为该data字段的子字段

**路由列表概览：**
* **功能类**
  * **/api/userinfo**          - 获取登陆用户信息
  * **/api/contacts**          - 获取通讯录信息（wxid从这个接口获取）
  * **/api/sendtxtmsg**        - 发送文本消息（好友和群聊组都可通过此接口发送，群聊组消息支持艾特）
  * **/api/sendimgmsg**        - 发送图片消息（支持json和form-data表单上传两种方式，json方式请将二进制数据使用base64编码后发送）
  * **/api/sendfilemsg**       - 发送文件消息（支持json和form-data表单上传两种方式，json方式请将二进制数据使用base64编码后发送）
  * **/api/chatroom**          - 获取群聊组成员列表
  * **/api/accountbywxid**     - WXID反查微信昵称（支持好友和群聊组等）
  * **/api/forwardmsg**        - 消息转发

* **回调注册类（目前仅用来获取微信实时消息 - 同步消息接口，同时支持WebSocket和http两种方式！）**
  * **/ws/generalMsg**             - 注册websocket回调（支持注册多个ws通道）：通用消息回调
  * **/api/syncurl**        - http回调相关（支持注册多个http接口，注册请带上协议头：http/https，注册成功会持久化到配置文件中）

#### 2.2.1、功能类接口
> **以`[]`中括号括起来的字段为可选字段**
> **目前所有请求和响应字段均按大驼峰命名法规范**

##### 2.2.1.1、登陆用户信息
**协议信息**

GET /api/userinfo

**别名**

/api/userInfo

/api/user-info

/api/user_info

**响应字段**

* customAccount *string*: 微信号
* city *string*: 城市
* country *string*：国家
* dbKey *string*：数据库加密key，可解密读取数据库
* nickname *string*： 微信昵称
* phone *string*： 手机号
* phoneSystem *string*： 手机系统
* privateKey *string*：私钥
* profilePicture *string*： 头像
* province *string*：省
* publicKey *string*：公钥
* signature *string*：个性签名
* wxid *string*

##### 2.2.1.2、通讯录
**协议信息**

GET /api/contacts

**响应字段**

* contacts *array*
  * customAccount *string*： 微信号
  * nickname *string*： 昵称
  * v3 *string*
  * note *string*： 备注
  * notePinyin *string*： 备注拼音首字母大写
  * notePinyinAll *string*： 备注拼音全
  * pinyin *string*： 昵称拼音首字母大写
  * pinyinAll *string*： 昵称拼音全
  * profilePicture *string*：头像
  * profilePictureSmall *string*：小头像
  * reserved1 *string*
  * reserved1 *string*
  * type *string*
  * verifyFlag *string*
  * wxid *string*
* total *uint64*： 通讯录成员总数

##### 2.2.1.3、发送文本消息
> 对于群聊组消息发送支持艾特

**协议信息**

POST /api/sendtxtmsg

**别名**

/api/sendTxtMsg

/api/send-txt-msg

/api/send_txt_msg

**请求字段**

* wxid *string*
* content *string*：发送消息内容（如果是群聊组消息并需要发送艾特时，**此content字段中需要有对应数量的`@[自定义被艾特人的昵称，不得少于2个字符] [每个艾特后都需要一个空格以进行分隔（包括最后一个艾特！）]`，这一点很重要！ 如果您不理解，请继续看下面的Tips！**）
* [atlist] *array\<string\>*：如果是群聊组消息并需要发送艾特时，此字段是一个被艾特人的数组

**Tips：如果是群聊艾特消息，那么`content`字段中的`@`艾特符号数量需要和`atlist`中的被艾特人数组长度一致，简单来说，就是`atlist`中有多少个被艾特人的`wxid`，那么`content`字段中就需要有多少个艾特组合，位置随意，例如：**
`{"wxid": "xx@chatroom", "content": "这里@11 只是@22 想告诉你@33 每个被艾特人的位置并不重要", "atlist": ["wxid_a", "wxid_b", "wxid_c"]}`
**每个被艾特人在`content`中 固定为`@[至少两个字符的被艾特人名] + 一个空格`！**
**如果是发送`@所有人`消息，那么请在`atlist`字段中仅传入一个`notify@all`字符串，`content`字段中仅包含一个`@符号规范（最少两字符+一个空格）`， 一般建议是`@所有人`见名知意**

**响应示例**

{"code":200,"msg":"success"}

##### 2.2.1.4、发送图片消息
**协议信息**

POST /api/sendimgmsg

**别名**

/api/sendImgMsg

/api/send-img-msg

/api/send_img_msg

/api/sendimagemsg

/api/sendImageMsg

/api/send-image-msg

/api/send_image_msg
> 支持JSON和form-data表单两种方式提交

**请求头**

* **JSON：`Content-Type: application/json`**
* **form-data表单：`Content-Type: multipart/form-data`**

**请求字段**

* **JSON：**
    * wxid *string*
    * path *string*：图片路径（注意，这里的图片路径是bot登陆系统的路径！）
    * image *string*： 图片二进制数据base64编码后字符串 **（不需要加 `data:image/jpeg;base64,` 前缀）**
    * clear *bool*： 指定图片发送后是否需要删除，默认删除 **（需要注意的是，图片文件保存后并没有后缀，这意味着如果您需要查看历史发送图片，那么您需要至`[微信根目录]/temp`自行查看判断图片格式并添加后缀）**

* **form-data表单**
    符合标准`form-data`数据格式，需要参数分别是`wxid`、`path`和`image`

`path`和`image`二选一即可，当`path`和`image`同时存在时，`path`优先

##### 2.2.1.5、发送文件消息
**协议信息**

POST /api/sendfilemsg

**别名**

/api/sendFileMsg

/api/send-file-msg

/api/send_file_msg
> 支持JSON和form-data表单两种方式提交

**请求头**

* **JSON：`Content-Type: application/json`**
* **form-data表单：`Content-Type: multipart/form-data`**

**请求字段**

* **JSON：**
    * wxid *string*
    * path *string*：文件路径（注意，这里的文件路径是bot登陆系统的路径！）
    * file *string*： 文件二进制数据base64编码后字符串
    * filename *string*： 文件名
* **form-data表单**
    符合标准`form-data`数据格式，需要参数分别是`wxid`、`path`和`image`

**Tips：** 当文件大小大于`5M`时则建议使用`path`文件路径的方式传参，但这并不意味着`file`不支持大文件发送，只是它需要更久的调用时间，可能是分钟级！`path`和`file`二选一即可，当`path`和`file`同时存在时，`path`优先，当使用`JSON`格式和`file`参数直接传递文件数据时`filename`是必填项！

#### 2.2.1.6、获取群聊组成员信息
**协议信息**
> 同时支持GET和POST

GET /api/chatroom?wxid=xxxx
POST /api/chatroom

**别名**

/api/chatRoom

/api/chat-room

/api/chat_room

**请求字段**

* **JSON：**
    * wxid *string*

**响应字段**
* data *map*
  * wxid *string*：
    * customAccount *string*：微信号
    * nickname *string*：昵称
    * note *string*：备注
    * pinyin *string*： 昵称拼音首字母大写
    * pinyinAll *string*： 昵称拼音全
    * profilePicture *string*：头像
    * profilePictureSmall *string*：小头像
    * v3 *string*

#### 2.2.1.7、WXID反查微信昵称
**协议信息**

> 同时支持GET和POST

GET /api/accountbywxid?wxid=xxxx
POST /api/accountbywxid

**别名**

/api/accountByWxid

/api/account-by-wxid

/api/account_by_wxid

**请求字段**

* **JSON：**
    * wxid *string*

**响应字段**

* customAccount *string*：微信号
* nickname *string*：昵称
* note *string*：备注
* pinyin *string*： 昵称拼音首字母大写
* pinyinAll *string*： 昵称拼音全
* profilePicture *string*：头像
* profilePictureSmall *string*：小头像
* v3 *string*

#### 2.2.1.8、转发消息
**协议信息**
> 同时支持GET和POST

GET /api/forwardmsg?wxid=xxxxxxxxxxx&msgId=xxxxxxxxxxxx
POST /api/forwardmsg

**别名**

/api/forwardMsg

/api/forward-msg

/api/forward_msg

**请求字段**
> 这里说明一下，因为前端精度问题，有些大佬可能传递`msgId`字段时存在精度丢失或自动转字符串的问题，所以这里我将`msgId`字段设置为了同时支持`uint64`和`string`两种类型！

* **JSON：**
    * wxid *string*：本次转发消息的接收对象
    * msgId *uint64|string*：消息id（通常可以用消息回调或者`websocket`回调获取到，当前是消息回调中的`MsgSvrID`字段）

#### 2.2.2、回调注册类
> 目前仅用来同步微信消息

**响应字段**
* wxid *string*：当前实例登陆用户的wxid
* total *uint32*：每次回调的消息数量
* data：
  * BytesExtra *string*：BASE64后的二进制数据
  * BytesTrans *string*
  * StrContent *string*：字符串数据，除文本消息以为大部分均为XML数  据
  * CompressContent *string*：`StrContent`以外的BASE64二进制数  据，例如引用的消息等
  * CreateTime *string*：秒级时间戳
    * 从PC登陆微信上发出的消息：标记代表的是每个消息点下发送按钮的那  一刻
    * 从其它设备上发出的/收到的来自其它用户的消息：标记的是本地从服 务器接收到这一消息的时间
  * DisplayContent *string*：拍一拍，邀请入群等消息
  * IsSender *string*：是否是自己发出的消息（0：非自己发送、1：自 己发送）
  * StrTalker *string*：消息发送者微信ID（wxid）
  * SubType *string*：消息类型子类，例如视频消息大类下可能存在小程  序等小类的区分
  * Type *string*：消息类型
  * localId *string*：本地数据库ID，目前来看是一个自增ID
  * MsgSvrID *string*：消息id
  * StatusEx、FlagEx、Status、MsgServerSeq、MsgSequence、Reserved0-6、TalkerId 未知

##### 2.2.2.1、websocket协议消息
**协议信息**

GET ws://xxxxx/ws/general-msg

> websocket没什么好说的，基本上第三方库都有直接可用的实现，协议升级后就是一条全双工通道，目前只用来接收同步微信的实时消息，不要发送消息到服务端，服务端不会响应。

##### 2.2.2.2、http协议
> 需要你自己起一个Http Server服务用来接收微信的实时消息，你自己的Http Server启动之后通过接口注册到wxbot即可

##### 2.2.2.2.1、注册接口
POST /api/syncurl

**别名**

/api/syncUrl

/api/sync-url

/api/sync_url

**请求字段**

* url *string*： 你自己启动的Http Server地址路由（**ip:port/[subpath]**）
* timeout *int*： 超时时间（当有一条新消息通过wxbot发送到你的回调地址时的最长连接等待时间）
* *type： string*
  * `general-msg`：为通用消息回调，目前仅有这一类型

##### 2.2.2.2.2、获取已注册接口列表
GET /api/syncurl

**别名**

/api/syncUrl

/api/sync-url

/api/sync_url

##### 2.2.2.2.3、删除接口
DELETE /api/syncurl

**别名**

/api/syncUrl

/api/sync-url

/api/sync_url

**请求字段**

* url： 已注册的Http Server地址（**ip:port/[subpath]**）
* *type： string* 此版本开始同时支持`msg`和`msg2`两种回调（默认值：`msg`）

### 2.3、接口使用例子
**Windows**
**所有`powershell`或者是使用`cmd`测试发送的例子都可能有编码问题！建议直接用程序测试！**
```powershell
# 发送文本
curl -Method POST -ContentType "application/json" -Body '{"wxid":"47331170911@chatroom", "content": "测试内容\nhello world!"}' http://127.0.0.1:8080/sendtxtmsg

# 发送艾特消息
curl -Method POST -ContentType "application/json" -Body '{"wxid":"47331170911@chatroom", "content": "测试内容\nhello world!", "atlist": ["被艾特人的wxid"]}' http://127.0.0.1:8080/sendtxtmsg
```

**Linux**
```bash
# 获取登陆用户信息
curl 127.0.0.1:8080/userinfo

# 获取通讯录信息
curl 127.0.0.1:8080/contacts

# 发送文本消息
curl -XPOST -H "Content-Type: application/json" -d'{"wxid": "47331170911@chatroom", "content": "测试内容\nHello World"}' 127.0.0.1:8080/sendtxtmsg

# 发送图片消息1（使用form-data表单方式提交）
curl -XPOST -F "wxid=47331170911@chatroom" -F "image=@/home/jwping/1.jpg" 127.0.0.1:8080/sendimgmsg
# 发送图片消息2（使用json方式提交）
curl -XPOST -H "Content-Type: application/json" -d'{"wxid": "47331170911@chatroom", "image": "R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="}' 127.0.0.1:8080/sendimgmsg

# 发送文件消息1（使用form-data表单方式提交）
curl -XPOST -F "wxid=47331170911@chatroom" -F "file=@/home/jwping/1.txt" 127.0.0.1:8080/sendfilemsg
# 发送文件消息2（使用json方式提交）
curl -XPOST -H "Content-Type: application/json" -d'{"wxid": "47331170911@chatroom", "filename": "1.txt", "file": "aGVsbG8gd29ybGQh"}' 127.0.0.1:8080/sendfilemsg

# 注册ws回调
# 使用任意程序websocket客户端连接127.0.0.1:8080/ws

# 注册http回调（http协议头不能少！）
curl -XPOST -d'{"url": "http://127.0.0.1:8081/callback", "timeout": 6000}' 127.0.0.1:8080/sync-url

# 获取当前已注册的http回调
curl 127.0.0.1:8080/sync-url

# 删除一个已注册的http回调
curl -XDELETE -d'{"url": "http://127.0.0.1:8081/callback"}' 127.0.0.1:8080/sync-url
```

## 3、赞助码
**如果觉得本项目对你有帮助，可以打赏一下作者，毕竟开源不易**

<img src=https://raw.githubusercontent.com/jwping/wxbot/main/public/wechat_collection.jpg width=40% />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src=https://raw.githubusercontent.com/jwping/wxbot/main/public/alipay_collection.jpg width=40% />

## 4、微信多开高级用法
这里仅仅给出一种为每个wxbot指定端口和回调地址等使用思路：
当您使用`wxbot-sidecar.exe -m`解开微信多开限制后，可以在`wxbot-sidecar.exe`的同级目录下为每个wxbot生成一个[wxid].json的配置文件，以此来为不同的wxbot定义不同的监听地址，或者使用`-a`参数来为每个wxbot指定一个监听地址，配置文件方式例如：

假设您有两个wxid为`wxid_a`和`wxid_b`的两个微信号希望实现多开注入，
那么您可以在您的微信根目录下分别生成`wxid_a.json`和`wxid_b.json`两个配置文件：
```powershell
# wxid_a.json配置文件内容如下：
{"addr": "0.0.0.0:8080"}

# wxid_b.json配置文件内容如下：
{"addr": "0.0.0.0:8081"}

# 配置文件生成好之后，您可以使用注入器对两个微信bot分次注入
# 第一次运行
wxbot-sidecar.exe -p [wxid_a的微信PID]

# 第二次运行
wxbot-sidecar.exe -p [wxid_b的微信PID]
```
至此，您就完成了对两个微信号wxbot运行，并且这两个wxbot分别监听在`8080`和`8081`端口
其中`wxid_a`监听在`8080`端口
其中`wxid_b`监听在`8081`端口

## 5、鉴权
> 当您在配置文件中开启了鉴权之后则 **您后续的每个api请求都需要包含鉴权信息！**
> 这里使用的是`Http Basic Authentication`，您可以先百度去了解一下它，当然，如果您不想了解也没关系，因为它真的很简单

```json
# 假设您定义一个如下用户：
{
    "user": "user2",
    "password": "321",
    "token": "token321"
}
```
那么您需要在您后续的每次请求的请求头中加上`Authorization`字段：`Authorization: Basic base64(username:password)`
例如用curl命令请求的话，它可能长这样：
```bash
curl -H "Authorization: Basic dXNlcjI6MzIx" 127.0.0.1:8080/login -v

# response：
{"code":200,"data":{"token":"token321","user":"user2"},"msg":null}
```
这里**引入了一个新的路由`/login`**，但我并不想将他写到上面的路由列表中，因为它真的没什么用，仅仅是在您登陆成功之后返回一个当前的登陆用户名和`token`
**您在以后每个请求都加上`Authorization: Basic dXNlcjI6MzIx`这个请求头就可以了！**

如果您希望使用`cookie`的方式，那么您可以在`cookie`中指定`token`
例如，您也可以这样做：
```bash
curl --cookie "access_token=token321" 127.0.0.1:8080/userinfo -v
```
**如果您不想用设置请求头的方式，那么您也可以在后续的所有请求的`cookie`中指定`access_token`字段即可。** *实际上`cookie`也是`request header`中的一个字段*


## 6、wxbox、可用版本微信安装包等获取
* **阿里网盘：**
https://www.aliyundrive.com/s/4eiNnE4hp4n
提取码: rt25

* **百度网盘：**
https://pan.baidu.com/s/1cmzXe8AxYvzXWW2WTVCdxQ?pwd=l671 
提取码：l671

## 7、交流
### 7.1、微信
请添加微信：**Anshan_PL**，备注 **wxbot** 拉微信交流群

**Tips：此群仅限学习和交流，无其他用处**

### 7.2、TG
Android端下载地址： https://telegram.org/android 其他客户端从这个网址找过去

安装后复制下面的链接到tg中打开： https://t.me/+DVigUtfAIOthNmNl

**Tips：此TG群同样仅限学习和交流，无其他用处**
