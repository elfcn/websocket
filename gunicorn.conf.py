bind = '127.0.0.1:23446' #gunicorn��صĽӿ�
workers = 1 #������
threads = 5 #ÿ�����̿������߳���


proc_name = 'app'
#gunicorn����id��kill�����ļ���id��gunicorn��ֹͣ
# pidfile = '/data1/test/app.pid'
loglevel = 'debug'
# logfile = '/data1/test/debug.log'
#������Ϣ��־
# errorlog = '/data/test/error.log'
timeout = 10

#https://github.com/benoitc/gunicorn/issues/1194
keepalive = 75 # needs to be longer than the ELB idle timeout
# worker_class = 'gevent' # ����ģʽЭ��
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
##about timeout issuses
#https://github.com/benoitc/gunicorn/issues/1440
#https://github.com/globaldigitalheritage/arches-3d/issues/54
#https://github.com/benoitc/gunicorn/issues/588
#https://github.com/benoitc/gunicorn/issues/1194
#https://github.com/benoitc/gunicorn/issues/942
#https://stackoverflow.com/questions/10855197/gunicorn-worker-timeout-error


worker_connections = 2000

#access��־���ã�����ϸ�����뿴��https://docs.gunicorn.org/en/stable/settings.html#logging
#`%(a)s`�ο�ʾ����'%(a)s "%(b)s" %(c)s' % {'a': 1, 'b' : -2, 'c': 'c'}
#�������ã�����ӡip������ʽ������url·��������httpЭ�顢����״̬�������user agent�������ʱ
#ʾ����[2020-08-19 19:18:19 +0800] [50986]: [INFO] 127.0.0.1 POST /test/v1.0 HTTP/1.1 200 PostmanRuntime/7.26.3 0.088525
access_log_format="%(h)s %(r)s %(s)s %(a)s %(L)s"

#https://github.com/benoitc/gunicorn/issues/2250
logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    #�����°汾�������root���ã������׳�Error: Unable to configure root logger
    "root": {
          "level": "DEBUG",
          "handlers": ["console"] # ��Ӧhandlers�ֵ�ļ���key��
    },
    'loggers':{
        "gunicorn.error": {
            "level": "DEBUG",# ����־�ĵȼ���
            "handlers": ["error_file"], # ��Ӧhandlers�ֵ�ļ���key����
            #�Ƿ���־��ӡ������̨��console������ΪTrue����1��������ӡ��supervisor��־����ļ�logfile�ϣ����ڲ��Էǳ����ã�
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
            "maxBytes": 1024*1024*100,# ����־�Ĵ�С���˴�����100mb��
            "backupCount": 1,# ��������������������־��С���������ֵ����Ϊ��С��������
            "formatter": "generic",# ��Ӧformatters�ֵ�ļ���key��
            "filename": "/usr/local/websocket/logs/error.log" #�����������ر����󣬽����޸Ĵ�·��
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*100,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "/usr/local/websocket/logs/access.log", #�����������ر����󣬽����޸Ĵ�·��
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
        },

    },
    'formatters':{
        "generic": {
            "format": "%(asctime)s [%(process)d]: [%(levelname)s] %(message)s", # ����־�ĸ�ʽ
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",# ʱ����ʾ��ʽ
            "class": "logging.Formatter"
        }
    }
}