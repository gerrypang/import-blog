#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import pymysql
import logging.config
import LoadConf
from bs4 import BeautifulSoup


# log配置
logging.config.fileConfig('logger.conf')
logger = logging.getLogger('importLogger')


# 打开数据库连接
def get_mysql_sql_conn():
    mysqlDb = pymysql.connect(host=LoadConf.mysqlHostUrl, port=LoadConf.mysqlPort, user=LoadConf.mysqlUsername,
                              passwd=LoadConf.mysqlPassword, db=LoadConf.mysqlUseDatabase, charset="utf8")
    return mysqlDb


# 查询Mysql多条数据
def query_all_mysql(querySQL, isPrintLog=True, msg="mysql fetch result data length: %d "):
    try:
        mysqlDb = get_mysql_sql_conn()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = mysqlDb.cursor()
        cursor.execute('SET NAMES UTF8')
        mysqlDb.commit()
        cursor.execute(querySQL)
        # 执行 SQL 查询
        result = cursor.fetchall()
        if isPrintLog:
            logger.info(msg % len(result))
        return result
    except Exception as e:
        logger.error('Insert operation error：%s' % str(e))
        raise
    finally:
        # 关闭数据库连接
        cursor.close()
        mysqlDb.close()


# mysql单条查询
def query_one_mysql(querySQL, isPrintLog=False, msg="mysql fetch one result data "):
    try:
        mysqlDb = get_mysql_sql_conn()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = mysqlDb.cursor()
        cursor.execute('SET NAMES UTF8')
        mysqlDb.commit()
        cursor.execute(querySQL)
        # 执行 SQL 查询
        result = cursor.fetchone()
        if isPrintLog:
            logger.info(msg)
        return result
    except Exception as e:
        logger.error('Error: query operation exception ：%s' % str(e))
        raise
    finally:
        # 关闭数据库连接
        cursor.close()
        mysqlDb.close()


# 更新Mysql数据
def updateMysql(updateSQL, isPrintLog=True, msg="Update success, Affect row: %d"):
    try:
        mysqlDb = get_mysql_sql_conn()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = mysqlDb.cursor()
        cursor.execute('SET NAMES UTF8')
        mysqlDb.commit()
        # 使用 execute()  方法执行 SQL 查询
        rowcount = cursor.execute(updateSQL)
        mysqlDb.commit()
        if isPrintLog:
            logger.info(msg % (int(rowcount)))
    except Exception as e:
        logger.error("Error: unable to update mysql data：%s" % str(e))
        mysqlDb.rollback()
        raise
    finally:
        # 关闭数据库连接
        cursor.close()
        mysqlDb.close()        


logger.info("======================= start to do ")
fo = open("./blogs_20180204.html", "r", encoding='UTF-8')
context = fo.read()
soup = BeautifulSoup(context, "lxml")
all_indexs = soup.ol.find_all("li")
for index in all_indexs:
    query_id_sql = '''SELECT auto_increment FROM information_schema.tables 
        where table_schema='wordpress' and table_name='wd_posts' '''
    inc_id = query_one_mysql(query_id_sql)
    id = str(index.a['href']).replace('#', '')
    a_blog = soup.find('a', attrs={"name": id}).parent.parent
    a_blog_title = a_blog.find('a', attrs={"name": id}).get_text()
    a_blog_date = a_blog.find('div', attrs={"class": "date"}).get_text().replace("时间：", "")
    a_blog_tag = a_blog.find('div', attrs={"class": "catalog"}).get_text().replace("分类：", "")
    a_blog_context = a_blog.find('div', attrs={"class": "content"}).get_text()
    a_blog_guid = "http://127.0.0.1/wordpress/?page_id=" + str(inc_id[0])
    sql = ''' INSERT INTO wd_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, 
        post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, 
        post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, 
        comment_count) 
        VALUES ('1', '%s', '%s' , '%s', '%s', '', 'publish','open', 'open', '', '%s', '', '', '%s', '%s', '' , 
        0, '%s', 0, 'post', '', 0) ''' % (a_blog_date, a_blog_date,
                                          pymysql.escape_string(a_blog_context),
                                          pymysql.escape_string(a_blog_title),
                                          pymysql.escape_string(a_blog_title),
                                          a_blog_date, a_blog_date, a_blog_guid)
    #print(sql)
    updateMysql(sql)
fo.close()
logger.info("======================= finish ")