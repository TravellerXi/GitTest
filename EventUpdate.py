#/usr/bin/env python3
#coding:utf-8
from pyzabbix import ZabbixAPI
import warnings
from python2.CorpInfo import *

def HandleZabbixEventUpdateRequest(EventID:str,Operations:str,Username:str):
    '''
    :param EventID: string, like '3711664'
    :param Operations:string, 'ack'/'close'.
    :param Username: Zabbix Username
    :return:
    '''
    url = URL  # 这里填写url
    zapi = ZabbixAPI(server=url)
    warnings.filterwarnings('ignore')
    zapi.login(user=UserName, password=PassWord)
    if Operations=='ack':
        AckMessage='用户'+Username+'通过企业微信确认问题ID'+str(EventID)
        zapi.event.acknowledge(eventids=str(EventID),action='6',message=AckMessage)
        return ('1')
    if Operations=='close':
        try:
            CloseMessage = '用户' + Username + '通过企业微信关闭问题ID' + str(EventID)
            zapi.event.acknowledge(eventids=str(EventID), action='1', message=CloseMessage)
            return ('1')
        except Exception as e:
            ErrorString = str(e)
            if ErrorString.find('does not allow manual closing'):
                return ('问题ID ' + str(EventID) + ',触发器未允许手动关闭，请登录zabbix修改相应触发器')
            else:
                return ('问题ID ' + str(EventID) + ',关闭失败，请再次尝试')