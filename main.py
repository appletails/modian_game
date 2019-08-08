# -*- coding: utf-8 -*-
import setting
import time
import random
# 引入时间调度器 apscheduler 的 BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# 实例化 BlockingScheduler
sched = BlockingScheduler()

# 增加攻击次数
def addAtc():
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
      for idol in item['idol']:
          idol['battle'] = 1
      for idol in item['otherIdol']:
          idol['battle'] = 1
    setting.writejson(userAll,'chess/user')

# 增加招募值
def addGold():
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
        item["gold"] = item["gold"]+1 if item["gold"]<6 else item["gold"]
    setting.writejson(userAll,'chess/user')

# 重置仇人 恢复生命
def reset():
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for user in userAll:
      user["revenge"] = []
      for item in user['idol']:
        if item["life"] < item['alllife']:
          item["life"] = item['alllife']
          
      for item in user['otherIdol']:
        if item["life"] < item['alllife']:
          item["life"] = item['alllife']
      addUser = 6 - len(user['idol'])
      if addUser:
          user['idol'] = user['idol']+user['otherIdol'][:addUser]
          user['otherIdol'] = user['otherIdol'][addUser:]
    setting.writejson(userAll,'chess/user')

# 开始定时任务
sched.add_job(addAtc, 'cron', minute = '*/59')
sched.add_job(addGold, 'cron', minute = '*/10')
sched.add_job(reset, 'cron', hour = 6)
# 开始调度任务
sched.start()