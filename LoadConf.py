#! python3
# -*- coding:utf-8 -*-

import configparser

# 加载现有配置文件
conf = configparser.ConfigParser()
conf.read("conf.ini")
mysqlHostUrl = conf.get('MySQL', 'hostUrl')
mysqlPort = conf.getint('MySQL', 'port')
mysqlUsername = conf.get('MySQL', 'username')
mysqlPassword = conf.get('MySQL', 'password')
mysqlUseDatabase = conf.get('MySQL', 'useDatabase')
