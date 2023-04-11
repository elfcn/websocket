bind = '127.0.0.1:23446' #gunicorn监控的接口
workers = 1 #进程数
threads = 5 #每个进程开启的线程数


proc_name = 'app'
#gunicorn进程id，kill掉该文件的id，gunicorn就停止
# pidfile = '/data1/test/app.pid'
loglevel = 'debug'
# logfile = '/data1/test/debug.log'
#错误信息日志
# errorlog = '/data/test/error.log'
timeout = 10

#https://github.com/benoitc/gunicorn/issues/1194
keepalive = 75 # needs to be longer than the ELB idle timeout
# worker_class = 'gevent' # 工作模式协程
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
##about timeout issuses
#https://github.com/benoitc/gunicorn/issues/1440
#https://github.com/globaldigitalheritage/arches-3d/issues/54
#https://github.com/benoitc/gunicorn/issues/588
#https://github.com/benoitc/gunicorn/issues/1194
#https://github.com/benoitc/gunicorn/issues/942
#https://stackoverflow.com/questions/10855197/gunicorn-worker-timeout-error


worker_connections = 2000

#access日志配置，更详细配置请看：https://docs.gunicorn.org/en/stable/settings.html#logging
#`%(a)s`参考示例：'%(a)s "%(b)s" %(c)s' % {'a': 1, 'b' : -2, 'c': 'c'}
#如下配置，将打印ip、请求方式、请求url路径、请求http协议、请求状态、请求的user agent、请求耗时
#示例：[2020-08-19 19:18:19 +0800] [50986]: [INFO] 127.0.0.1 POST /test/v1.0 HTTP/1.1 200 PostmanRuntime/7.26.3 0.088525
access_log_format="%(h)s %(r)s %(s)s %(a)s %(L)s"

#https://github.com/benoitc/gunicorn/issues/2250
logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    #在最新版本必须添加root配置，否则抛出Error: Unable to configure root logger
    "root": {
          "level": "DEBUG",
          "handlers": ["console"] # 对应handlers字典的键（key）
    },
    'loggers':{
        "gunicorn.error": {
            "level": "DEBUG",# 打日志的等级；
            "handlers": ["error_file"], # 对应handlers字典的键（key）；
            #是否将日志打印到控制台（console），若为True（或1），将打印在supervisor日志监控文件logfile上，对于测试非常好用；
            "propagate": 0, 
            "qualname": "gunicorn_error"
        },

        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "access"
        }
    },
    'handlers':{
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*100,# 打日志的大小（此处限制100mb）
            "backupCount": 1,# 备份数量（若需限制日志大小，必须存在值，且为最小正整数）
            "formatter": "generic",# 对应formatters字典的键（key）
            "filename": "/usr/local/websocket/logs/error.log" #若对配置无特别需求，仅需修改此路径
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*100,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "/usr/local/websocket/logs/access.log", #若对配置无特别需求，仅需修改此路径
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
        },

    },
    'formatters':{
        "generic": {
            "format": "%(asctime)s [%(process)d]: [%(levelname)s] %(message)s", # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",# 时间显示格式
            "class": "logging.Formatter"
        }
    }
}