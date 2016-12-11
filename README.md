# GoHome
Help the missing children to go home.

# Auther
Yi Huang        (titushuang@tencent.com)
Zhuowen Deng    (mikedeng@tencent.com)
Linqiang Wang   (brandonwang@tencent.com)
Junhao Lin      (junhaolin@tencent.com)


#愿景
基于庞大的微信用户群体，众人共同参与不再让失踪发生。

#程序说明
本程序分为基于微信小程序开发的前端和基于Flask框架的后台框架。
小程序负责数据交互和展示，后台通过提供封装的cgi来为前端提供服务。


#目录结构及说明
GoHome/
|-- README.md
|-- libi     //相关使用的库
|-- m.gohomehackathon.club.crt
|-- m.gohomehackathon.club.key
|-- m.gohometencent-hackathon.club.crt
|-- m.gohometencent-hackathon.club.key
|-- main.py  //程序的主入口
|-- model    //负责数据库的访问
`-- photos   //存储上传的图片


#主要功能
1:爱心人士可以通过手机采集疑似失踪人员的照片和位置，并上报到后台服务器。
2:失踪人员的亲属可以在平台发布走失信息，上传失踪人员的资料。
3:后台服务器根据失踪人员的资料进行实时匹配，并将可能的结果及时通知给失踪人员亲属。

#优势
1:数量庞大的信息采集源
2:数据处理的实时性
3:及时的结果反馈
