# -*- coding: utf-8 -*-
import random
import setting
import skill
import copy

gong = "[CQ:emoji,id=9876]️"
fang = "[CQ:emoji,id=128737]️"
xue = "[CQ:emoji,id=9829]"

def DrawCard(user_id, nickname):# 最终调用的招募函数
    # 不管金额多少都要入库，首先判断是否入库
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 过滤出含有 user_id的对象数组
    user = list(filter(lambda item: item['user_id'] == int(user_id), userAll))
    if len(user):  # 判断是否存在对象 长度为0则不存在
        # 用户存在
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        msg = "次数已耗尽，等待恢复。"
        if "nickname" not in user:
            user["nickname"] = [nickname]
        if user["gold"]:
            msgArr = card(user)
            msg = msgArr['msg']
            user = msgArr['user']
            user["gold"] -= 1
    else:
        # 用户不存在
        data = setting.openjson('chess/ssr')  # 打开本地user缓存到 userAll
        idol = random.choice(list(filter(lambda item: item['level'] == "SSR", data)))
        user = {
            "user_id": user_id,
            "nickname": [nickname],
            "gold": 5,
            "uninstall": False,
            "power": 0,
            "package":[],
            "revenge":[],
            "idol": [idol],
            "otherIdol": [],
            "KO":100
        }
        userAll.append(user)
        msg = "恭喜你招募到了【SSR】的新角色【%s】！\n初次招募必得SSR，后续招募脸。" % idol["nickname"]
    userAll = levelProtect(userAll)  # 计算战斗力
    # 新用户添加到缓存的数据里去
    setting.writejson(userAll, 'chess/user')
    return msg


def card(user):# 纯招募函数
    msg = ''
    # 获取一个随机概率 n
    n = random.uniform(1, 100)
    if n <= 2:
        # ur
        idols = setting.openjson("chess/ur")
        idol = random.choice(idols)
    elif n <= 10:
        # ssr
        idols = setting.openjson("chess/ssr")
        idol = random.choice(idols)
    elif n <= 24:
        # sr
        idols = setting.openjson("chess/sr")
        idol = random.choice(idols)
    elif n <= 52:
        # r
        idols = setting.openjson("chess/r")
        idol = random.choice(idols)
    else:
        # n
        idols = setting.openjson("chess/n")
        idol = random.choice(idols)

    # 判断角色是否存在
    userAllIdol = user["idol"] + user["otherIdol"]
    hasIdol = list(
        filter(lambda item: item['nickname'] == idol["nickname"], userAllIdol))
    if len(hasIdol):
        hasIdol = hasIdol[0]
        hasIdol["num"] += 1
        msg += "【%s】: 【%s】" % (hasIdol["level"], hasIdol["nickname"])
        # 判断是否升级
        if hasIdol["num"] >= 4:
            hasIdol["star"] += 1
            hasIdol["num"] -= 4
            [attack,defense,life] = setting.dataUp(hasIdol["level"])
            hasIdol["attack"] += attack
            hasIdol["life"] += life
            hasIdol["alllife"] += life
            hasIdol["defense"] += defense
            msg += "\n【%s】升星！\n星级：%s \n[CQ:emoji,id=9876]️%s ↑ %s\n[CQ:emoji,id=128737]️%s ↑ %s\n[CQ:emoji,id=9829]%s ↑ %s" % (
                hasIdol["nickname"], setting.levelN(hasIdol["star"]), hasIdol["attack"], attack, hasIdol["defense"], defense, hasIdol["life"], life)
            if hasIdol["level"] in ["SR","R","N"]:
                hasIdol["lock"] = True
                msg += "\n状态：[CQ:emoji,id=128274]上锁"
            if hasIdol["level"] in ["N","R","SR"] and hasIdol["star"] >= 4 and hasIdol["skill"] == "未知": # 获得技能
                skill = list(filter(lambda x:x["study"], setting.openjson("chess/skill")))
                hasIdol["skill"] = random.choice(skill)["name"]
                msg += '\n获得技能：%s' % hasIdol["skill"]
    else:
        userAllIdol.append(idol)
        msg += "【%s】: 【%s】NEW！" % (idol["level"], idol["nickname"])
    # userAllIdol = sorted(userAllIdol, key=lambda x: x['attack'], reverse=True)
    user["idol"] = userAllIdol[:6]
    user["otherIdol"] = userAllIdol[6:]
    msgArr = {"user": user, "msg": msg}
    return msgArr


def suoha(user_id):# 梭哈
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 过滤出含有 user_id的对象数组
    user = list(filter(lambda item: item['user_id'] == int(user_id), userAll))
    if not len(user):
        return "请先招募一次"
    user = user[0]
    if user["uninstall"]:
        return "你已卸载退游"
    msg = "梭哈信息如下："
    if not user['gold']:
        return "招募次数不足"
    while user['gold']:
        user['gold'] -= 1
        msgArr = card(user)
        user = msgArr["user"]
        msg += '\n%s' % msgArr["msg"]
    # 新用户添加到缓存的数据里去
    userAll = levelProtect(userAll)  # 计算战斗力
    setting.writejson(userAll, 'chess/user')
    return msg


def seachMy(user_id):# 我的信息
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
            # 过滤出含有 nick_name的对象数组
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        nickname = "你" if "nickname" not in user else user['nickname']
        msg = "%s一共招募了%d个角色，当前阵容(%d)：" % (nickname[0], len(userAllIdol), len(user["idol"]))
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],setting.levelN(item["star"]), item["level"], item["nickname"],"*"+item["skill"]+"*" if item["skill"] != "未知" else '', item["attack"], item["defense"], item["life"], item["alllife"])
        msg += "\n剩余招募值：%s" % str(user['gold'])
    return msg


def idolhMy(user_id,level):# 我的角色
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
            # 过滤出含有 nick_name的对象数组
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        lvIdol = list(
            filter(lambda item: item['level'] == level, userAllIdol))
        allN = len(setting.openjson("chess/%s" % level))
        msg = "你的%s（%d/%d）：" % (level, len(lvIdol), allN)
        for idol in lvIdol:
            msg += "%s *%s、" % (idol["nickname"], idol["num"])
    return msg


def battle(user_id, nickname, types = False,re = True):# 进攻 types为True时全军出击
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return False
        if nickname in user["nickname"]:
            return False
        # 过滤出对手
        otherUser = list(filter(
            lambda item: nickname in item['nickname'], userAll))
        if not len(otherUser):
            return False
        # 判断对手是否弱小
        # 1.获取进攻列表 2.看看对手在不在列表
        otherUser = otherUser[0]
        # otherUsers = battlelist(user_id,True)
        # if otherUser not in otherUsers:
        #     return "禁止欺负弱小！"

        # 过滤出一个可进攻角色
        # 进攻
        if re:
            atc = list(filter(
                lambda item: item['battle'], user['idol']))
        else:
            atc = copy.deepcopy(user['idol'])
        if not len(atc):
            return "没有可攻击的角色"
        # 这里开始是战斗片段
        msg = "【%s】对战【%s】：\n" % (user["nickname"][0], nickname)
        num = 1
        if types:
            num = len(atc)
        while num:
            # 如果是进攻的话
            if re:
                # 开始计数
                revenge = list(filter(lambda item: item['user_id'] == user_id, otherUser["revenge"]))
                if len(revenge):
                    if revenge[0]["num"] >= 6:
                        msg = "仇恨值已满，不可进攻"
                        break
                    else:
                        revenge[0]["num"] += 1
                else:
                    otherUser["revenge"].append({
                        "user_id":user_id,
                        "nickname":user["nickname"],
                        "num":1,
                        "revenge":0
                    })
            else:
                # 开始计数
                revenge = list(filter(lambda item: nickname in item["nickname"], user["revenge"]))
                if len(revenge):
                    if revenge[0]["revenge"] >= revenge[0]["num"]:
                        msg += "\n已完成复仇"
                        break
                    else:
                        revenge[0]["revenge"] += 1
                else:
                     return "没有仇怨"
            [msgs,atc,user,otherUser] = sBattle(atc,user,otherUser)
            msg += msgs
            num -= 1
        userAll = levelProtect(userAll)  # 计算战斗力
        setting.writejson(userAll, "chess/user")
    return msg

def sBattle(atc,user,otherUser): # 进攻部分
    msgs = ''
    userIdol = random.choice(atc)
    otherUserIdol = random.choice(otherUser['idol'])
    battleSkill = True
    # 进入战斗
    if userIdol["skill"] != "未知" or otherUserIdol["skill"] != "未知":
        # 技能战斗部分
        if otherUserIdol["skill"] == "绝对领域" and random.uniform(1, 100)<=15:
            msgs += "\n【%s】VS【%s *绝对领域*】未能造成伤害" % (
                userIdol["nickname"], otherUserIdol["nickname"])
            battleSkill = False

        elif userIdol["skill"] == "一击致命" and random.uniform(1, 100)<=10:
            [msgs,user,userIdol,otherUser,otherUserIdol] = skill.BlastABall(user,userIdol,otherUser,otherUserIdol)
            battleSkill = False

        elif userIdol["skill"] == "背刺" and random.uniform(1, 100)<=30:
            [msgs,user,userIdol,otherUser,otherUserIdol] = skill.Backstab(user,userIdol,otherUser,otherUserIdol)
            battleSkill = False

        elif userIdol["skill"] == "觉醒" and userIdol['attack'] > otherUserIdol['defense'] and random.uniform(1, 100)<=15:
            # 确定会造成伤害
            [msgs,user,userIdol,otherUser,otherUserIdol] = skill.awaken(user,userIdol,otherUser,otherUserIdol)
            battleSkill = False

        elif userIdol["skill"] == "嗜血" and userIdol['attack'] > otherUserIdol['defense'] and random.uniform(1, 100)<=30:
            # 确定会造成伤害
            life = userIdol['attack'] - otherUserIdol['defense']
            msgs += "\n【%s *嗜血*】VS【%s】造成%s点伤害，恢复%s生命" % (
                userIdol["nickname"], otherUserIdol["nickname"], life, life)
                
            otherUserIdol['life'] -= life  # 剩余生命值
            userIdol['life'] += life  # 剩余生命值
            [msga,user,userIdol,otherUser,otherUserIdol] = skill.DeathNot(user,userIdol,otherUser,otherUserIdol)
            msgs += msga
            battleSkill = False
            
    if battleSkill: 
        # 正常战斗部分
        if userIdol['attack'] < otherUserIdol['defense']:  # 攻小于防
            msgs += "\n【%s】VS【%s】无功而返" % (
                userIdol["nickname"], otherUserIdol["nickname"])
        elif userIdol['attack'] == otherUserIdol['defense']:  # 攻等于防
            msgs += "\n【%s】VS【%s】旗鼓相当" % (
                userIdol["nickname"], otherUserIdol["nickname"])
        elif userIdol['attack'] > otherUserIdol['defense']:  # 攻大于防
            life = userIdol['attack'] - otherUserIdol['defense']
            msgs += "\n【%s】VS【%s】造成%s点伤害" % (
                userIdol["nickname"], otherUserIdol["nickname"], life)
                
            otherUserIdol['life'] -= life  # 剩余生命值
            [msga,user,userIdol,otherUser,otherUserIdol] = skill.DeathNot(user,userIdol,otherUser,otherUserIdol)
            msgs += msga
    userIdol['battle'] -= 1  # 可攻击次数减一
    atc.remove(userIdol)
    return [msgs,atc,user,otherUser]

def reset():# 重置
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
        item["gold"] = 6
        for idol in item['idol']:
            idol['battle'] = 1
    setting.writejson(userAll, 'chess/user')
    return "已经重置"


def battlelist(user_id=False,reDict = False):# 攻击列表
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    if not len(userAll):
        return msg
    userAll = levelProtect(userAll)  # 计算战斗力
    setting.writejson(userAll, 'chess/user')
    if user_id:
        # 判断用户在不在
        user = list(filter(lambda item: item['user_id'] == user_id, userAll))
        if not len(user):
            return msg
        # 判断退游
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        power = user["power"]
        users = userAll[:4]
        userAll = list(filter(lambda x: power - x["power"] < 300, userAll))
        # 至少允许攻击后三位
        if len(userAll)<4:
            userAll = users
        if reDict:
            return userAll
    msg = ''
    for item in userAll:
        msg += '%s[%s]  %d\n' % (item["nickname"][0],item["nickname"][-1], item["power"])
    return msg

def goBattle(user_id, idolList):# 派出阵容
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        # 判断角色是否拥有
        idolList = list(set(idolList.split(" ")))
        if len(idolList) != 6:
            return "角色不可重复且数量必须为6"
        # 判断角色是否存在
        userAllIdol = user["idol"] + user["otherIdol"]
        user["idol"] = []
        for idol in idolList:
            has = list(
                filter(lambda item: item['nickname'] == idol, userAllIdol))
            if not len(has):
                return "你没有%s" % idol
            # 判断血量
            for i in has:
                if i["life"] <= 0:
                    return "你的%s已经阵亡，重选" % idol
            userAllIdol.remove(has[0])
            user["idol"].append(has[0])
        user["idol"] = sorted(
            user["idol"], key=lambda x: x['attack'], reverse=True)
        user["otherIdol"] = sorted(
            userAllIdol, key=lambda x: x['attack'], reverse=True)
        msg = "%s的当前阵容(前六位)：" % user["nickname"][0]
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],setting.levelN(item["star"]), item["level"], item["nickname"],"*"+item["skill"]+"*" if item["skill"] != "未知" else '', item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg


def changeBattle(user_id, idolList):# 替换角色
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        # 判断角色是否拥有
        idolList = list(set(idolList.split(" ")))
        if len(idolList) != 2:
            return "角色不可重复且数量必须为2"
        userAllIdol = user["idol"] + user["otherIdol"]
        for idol in idolList:
            has = list(
                filter(lambda item: item['nickname'] == idol, userAllIdol))
            if not len(has):
                return "你没有%s" % idol
            # 判断血量
            for i in has:
                if i["life"] <= 0:
                    return "你的%s已经阵亡，重选" % idol
        # 判断第一个在不在
        hasGo = list(
            filter(lambda item: item['nickname'] == idolList[0], user["idol"]))
        if len(hasGo):
            hasGo = hasGo[0]
            hasT = list(
                filter(lambda item: item['nickname'] == idolList[1], user["otherIdol"]))[0]
        else:
            hasGo = list(
                filter(lambda item: item['nickname'] == idolList[1], user["idol"]))[0]
            hasT = list(
                filter(lambda item: item['nickname'] == idolList[0], user["otherIdol"]))[0]
        user["otherIdol"].remove(hasT)
        user["otherIdol"].append(hasGo)
        user["idol"].remove(hasGo)
        user["idol"].append(hasT)
        user["idol"] = sorted(
            user["idol"], key=lambda x: x['attack'], reverse=True)
        user["otherIdol"] = sorted(
            user["otherIdol"], key=lambda x: x['attack'], reverse=True)
        msg = "%s的当前阵容：" % user["nickname"][0]
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],setting.levelN(item["star"]), item["level"], item["nickname"],"*"+item["skill"]+"*" if item["skill"] != "未知" else '', item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg

def attack(user_id,typs = False):# 攻击阵容 typs 防御阵容
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        if typs: # 防御姿态
            userAllIdols = sorted(
                list(filter(lambda x: x["life"] > 0, userAllIdol)),
                key=lambda x: x['defense'], reverse=True)
        else: # 攻击姿态
            userAllIdols = sorted(
                list(filter(lambda x: x["life"] > 0, userAllIdol)),
                key=lambda x: x['attack'], reverse=True)
        if len(userAllIdols)<6: # 存活角色不足6个时候的操作
            user["idol"] = userAllIdols
            user["otherIdol"] = list(filter(lambda x: x["life"] <= 0, userAllIdol))
        else:
            # 将0血角色滞后
            userAllIdol = userAllIdols + list(filter(lambda x: x["life"] <= 0, userAllIdol))
            user["idol"] = userAllIdol[:6]
            user["otherIdol"] = userAllIdol[6:]
        msg = "当前阵容(%d)：" % len(user["idol"])
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],setting.levelN(item["star"]), item["level"], item["nickname"],"*"+item["skill"]+"*" if item["skill"] != "未知" else '', item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg


def nchange(user_id, m="N"):# 融化
    if m == "N":
        n = 10
    elif m == "R":
        n = 5
    elif m == "SR":
        n = 2
    else:
        return ''
    msg = "\n请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "\n你已卸载退游"
        nCard = list(
            filter(lambda x: x["level"] == m and not x["lock"], user["otherIdol"]))
        user["otherIdol"] = list(
            filter(lambda x: x["level"] != m or x["lock"], user["otherIdol"]))
        nCard = sorted(
            nCard, key=lambda x: x['num'], reverse=True)
        # 开始计算
        alln = sum([(i["num"]) for i in nCard])
        if alln < n:
            return "\n不足%d个%s不可融合" % (n, m)
        num = int(alln/n)
        ind = alln % n
        user["gold"] += num
        # 获取剩余的
        surplus = []
        if ind:
            i = 0
            while ind:
                if nCard[i]["num"] >= ind:
                    nCard[i]["num"] = ind
                    surplus.append(nCard[i])
                    ind = 0
                else:
                    surplus.append(nCard[i])
                    ind -= nCard[i]["num"]
                    i += 1

        user["otherIdol"] += surplus
        # print([i["nickname"] for i in user["otherIdol"]])
        # print(ind)
        # return
        setting.writejson(userAll, 'chess/user')
        msg = "\n获得%s点招募值" % str(num)
    return msg



def oneIdol(user_id, nickname):# 查单个
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        nCard = list(filter(lambda x: x["nickname"] == nickname, userAllIdol))
        if not len(nCard):
            return "你没有【%s】" % nickname
        nCard = nCard[0]
        # 计算星级显示
        msg = "【%s】的【%s】：\n稀有度：%s\n攻击：[CQ:emoji,id=9876]️%s\n防御：[CQ:emoji,id=128737]️%s\n血量：[CQ:emoji,id=9829]%s/%s\n星级：%s\n拥有数量：%s\n状态：%s" % (
            user["nickname"][0], nCard["nickname"], nCard["level"], nCard["attack"], nCard["defense"], nCard["life"], nCard["alllife"], setting.levelN(nCard["star"]), nCard["num"], "[CQ:emoji,id=128274]上锁" if nCard["lock"] else "[CQ:emoji,id=128275]未上锁")
        if nCard["skill"] != "未知":
            msg +="\n技能：%s" % nCard["skill"]
    return msg


def lockOn(user_id, nickname, m):# 上锁
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        if user[0]["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user[0]["idol"] + user[0]["otherIdol"]
        nCard = list(filter(lambda x: x["nickname"] == nickname, userAllIdol))
        if not len(nCard):
            return "你没有【%s】" % nickname
        nCard = nCard[0]
        nCard["lock"] = True
        msg = "【%s】已上锁" % nickname
        if m:
            nCard["lock"] = False
            msg = "【%s】已解锁" % nickname
    setting.writejson(userAll, "chess/user")
    return msg


def hasLock(user_id):# 以上锁
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        nCard = list(filter(lambda x: x["lock"], userAllIdol))
        if not len(nCard):
            return "你没有上锁角色"
        msg = "锁了："
        for item in nCard:
            msg += "%s、" % item["nickname"]
    return msg


def dead(user_id):# 已阵亡
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        nCard = list(filter(lambda x: x["life"] <= 0, userAllIdol))
        if not len(nCard):
            return "你没有战败角色"
        msg = "战败："
        for item in nCard:
            msg += "%s、" % item["nickname"]
    return msg


def levelProtect(userAll):# 排名
    for item in userAll:
        allIdol = item["idol"] + item["otherIdol"]
        allIdol = sorted(
            list(filter(lambda x: x["life"] > 0, allIdol)), key=lambda x: x['attack'], reverse=True)
        if len(allIdol) < 6:
            item["power"] = 0
        else:
            item["power"] = int(sum([allIdol[i]["attack"]/0.15+allIdol[i]["defense"]/0.15+allIdol[i]["alllife"]*0.7 for i in range(6)]))
    userAll = sorted(userAll,
                     key=lambda i: i["power"],
                     reverse=True)
    for i in range(len(userAll)):
        userAll[i]['KO'] = i+1
    ini = setting.openjson('ini')
    ini['allUser'] = userAll[-1]['KO']
    setting.writejson(ini,'ini')
    return userAll

def skills():
    msg = "技能列表："
    data = setting.openjson('chess/skill')
    for item in data:
        msg += "\n%s：%s" % (item["name"],item["msg"])
    return msg

def showSkill(user_id,name):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        nCard = list(filter(lambda x: x["skill"] == name, userAllIdol))
        if not len(nCard):
            return "你没有 *%s* 的角色" % name
        msg = "*%s*：" % name
        for item in nCard:
            msg += "%s、" % item["nickname"]
    return msg

def goSkill(user_id,name):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        # 活着的角色
        userAllIdols = list(filter(lambda x: x["life"] > 0, userAllIdol))
        # 活着的角色里有技能的
        hasName = sorted(list(filter(lambda x: x["skill"] == name, userAllIdols)),
                key=lambda i: i['attack'], reverse=True)
        # 活着的角色里么有技能的
        noName = sorted(list(filter(lambda x: x["skill"] != name, userAllIdols)),
                key=lambda i: i['attack'], reverse=True)
        
        userAllIdolDead =list(filter(lambda x: x["life"] <= 0, userAllIdol))
        # 拼接全部角色
        userAllIdol = hasName + noName + userAllIdolDead
        user["idol"] = userAllIdol[:6]
        user["otherIdol"] = userAllIdol[6:]
        msg = "当前阵容(%d)：" % len(user["idol"])
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],setting.levelN(item["star"]), item["level"], item["nickname"],"*"+item["skill"]+"*" if item["skill"] != "未知" else '', item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg

def seachPack(user_id):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        if not len(user["package"]):
            return "你没有道具"
        msg = "你的道具："
        for item in user["package"]:
            msg += "%s*%d、" % (item["name"],item["num"])
    return msg

def blood(user_id):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        # 过滤出残血
        noblood = sorted(list(filter(lambda x:x["life"] < x["alllife"] and x["life"]>0,user["idol"]+user["otherIdol"])),key=lambda i:i["life"])
        if not len(noblood):
            return "你没有残血"
        msg = "你的残血："
        for item in noblood:
            msg += "%s %d/%d、" % (item["nickname"],item["life"],item["alllife"])
    return msg

def revenge(user_id):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        if user[0]["uninstall"]:
            return "你已卸载退游"
        # 开始复仇
        msg = ''
        revenges = list(filter(lambda x:x['revenge'] < x['num'] ,user[0]["revenge"]))
        if not len(revenges):
            return False
        for item in revenges:
            msg += "%s\n" % item["nickname"][0]
    return msg

def getDui(user_id):
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        if user[0]["uninstall"]:
            return "你已卸载退游"
        # 开始复仇
        duishou = random.choice(list(filter(lambda item: item['user_id'] != user_id and user_id not in [j['user_id'] for j in item['revenge']] and item['power']>0, userAll)))
        msg = duishou['nickname'][1] if len(duishou['nickname']) >1 else duishou['nickname'][0]
    return msg