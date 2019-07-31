# -*- coding: utf-8 -*-
import json
import codecs
import time
import random

# ------------------------usersetting-------
# 打开json文件
def openjson(path):
    fb = open('jsons/'+path+'.json','rb')
    data = json.load(fb)
    fb.close()
    return data

# 写入json文件
def writejson(data,path):
    fb = codecs.open('jsons/'+path+'.json','w', 'utf-8')
    fb.write(json.dumps(data,indent=4,ensure_ascii=False))
    fb.close()

# 将日期转换为时间戳
def timeStamp(dt):
    timeStamp = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
    return timeStamp

# 将时间轴转换时间格式(2016-05-05 20:28:54)
def timeDate(dt):
    timeDate = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(dt))
    return timeDate
    

# qq群id
def groupid():
    data = openjson('ini')
    id = data['QQqun']['id']
    return id

star = "[CQ:emoji,id=127775]"
moon = "[CQ:emoji,id=127769]"
sun = "[CQ:emoji,id=9728]"
crown = "[CQ:emoji,id=128081]"

def levelN(num):# 计算星
    starN = num % 4
    moonN = int(num/4)
    sunN = int(moonN/4)
    crownN = int(sunN/4)
    return crownN * crown + sunN % 4 * sun + moonN % 4 * moon + starN * star

def dataUp(level):
  linkData = {
    "N":{
      "attack":[2,5],
      "defense":[1,2],
      "life":[1,5]
    },
    "R":{
      "attack":[3,7],
      "defense":[1,3],
      "life":[2,7]
    },
    "SR":{
      "attack":[5,12],
      "defense":[2,5],
      "life":[3,10]
    },
    "SSR":{
      "attack":[7,15],
      "defense":[3,6],
      "life":[4,12]
    },
    "UR":{
      "attack":[9,17],
      "defense":[4,8],
      "life":[5,13]
    }
  }
  attack = random.randint(linkData[level]["attack"][0],linkData[level]["attack"][1])
  defense = random.randint(linkData[level]["defense"][0],linkData[level]["defense"][1])
  life = int((linkData[level]["attack"][1]/attack) + (linkData[level]["defense"][1]/defense)*random.randint(linkData[level]["life"][0],linkData[level]["life"][1]))
  return [attack,defense,life]