## realbio_ctns
锐翌集群温度报警系统


#### 项目简介
>结合阿里大于短信平台，读取集群温度配置文件，当集群进气口/出气口温度超出预定温度时，发
>出短信/语音/邮件预警，及时通知相关责任人


#### 运行配置
##### STEP 0. 配置短信/邮件API的帐户，密码，短信/语音/邮件接收人，温度限制值等相关信息
>$ vim conf/settings.py

##### STEP 1. 复制阿里大于短信SDK至项目的core目录下
>$ cp -r /path/to/top core/

##### STEP 2. 在项目根目录下运行main.py
>$ python main.py


#### 更新日志
##### v2.0.2 (07/02/2018)
>1. 增加设置项`settings.EMAIL_PORT`（SMTP端口） 

##### v2.0.1 (06/30/2018)
>1. 增加引入阿里大于旧版SDK的注释说明（重要）   

##### v2.0.0 (06/29/2018)
>1. 新增发送邮件功能   
>2. 大幅重构代码，项目结构更清晰   
>3. `幸福感`大幅提高:P，可以回家

##### v1.0.0（06/28/2018）
>1. 短信和语音提醒功能  
>2. 可自定义发送短信列表  
>3. 自动扫描温度日志文件  
