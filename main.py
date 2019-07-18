# -*- coding: utf-8 -*-
import setting
import time
import random
# 引入时间调度器 apscheduler 的 BlockingScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# 实例化 BlockingScheduler
sched = BlockingScheduler()

# 定时函数
def addAtc():
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
      for idol in item['idol']:
          idol['battle'] = 1
      for idol in item['otherIdol']:
          idol['battle'] = 1
    setting.writejson(userAll,'chess/user')

# 定时函数
def on_time():
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
        item["gold"] = item["gold"]+1 if item["gold"]<6 else item["gold"]
    setting.writejson(userAll,'chess/user')

# 开始定时任务
sched.add_job(addAtc, 'cron', minute = '*/59')
sched.add_job(on_time, 'cron', minute = '*/10')
# 开始调度任务
sched.start()