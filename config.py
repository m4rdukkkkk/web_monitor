host = '127.0.0.1'
port = 3306
user='root'
password='123456'
db='web_monitor'

#运用特殊的配合活用phantomjs  是否缓存，是否加载图片

SERVICE_ARGS = ['--disk-cache=true',"--load-images=false"]