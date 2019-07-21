# -*- coding: utf-8 -*-
import random
import setting

star = "[CQ:emoji,id=127775]"
moon = "[CQ:emoji,id=127769]"
sun = "[CQ:emoji,id=9728]"
crown = "[CQ:emoji,id=128081]"
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
        data = setting.openjson('chess/sr')  # 打开本地user缓存到 userAll
        idol = list(filter(lambda item: item['nickname'] == "方琪", data))
        user = {
            "user_id": user_id,
            "nickname": [nickname],
            "gold": 5,
            "idol": idol,
            "otherIdol": [],
            "uninstall": False,
            "power": 0,
            "package":[]
        }
        userAll.append(user)
        msg = "恭喜你招募到了【SR】的新角色【方琪】！\n初次招募必得大帝，后续招募全看缘分。"
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
    elif n <= 5:
        # ssr
        idols = setting.openjson("chess/ssr")
        idol = random.choice(idols)
    elif n <= 20:
        # sr
        idols = setting.openjson("chess/sr")
        idol = random.choice(idols)
    elif n <= 45:
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
            attack = random.randint(5, 15)
            life = random.randint(10, 100)
            defense = random.randint(5, 15)
            hasIdol["attack"] += attack
            hasIdol["life"] += life
            hasIdol["alllife"] += life
            hasIdol["defense"] += defense
            msg += "\n【%s】升星！\n星级：%s \n[CQ:emoji,id=9876]️%s ↑ %s\n[CQ:emoji,id=128737]️%s ↑ %s\n[CQ:emoji,id=9829]%s ↑ %s" % (
                hasIdol["nickname"], levelN(hasIdol["star"]), hasIdol["attack"], attack, hasIdol["defense"], defense, hasIdol["life"], life)
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
        msg = "%s一共招募了%s个角色，当前阵容(前六位)：" % (nickname[0], str(len(userAllIdol)))
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],levelN(item["star"]), item["level"], item["nickname"],  item["attack"], item["defense"], item["life"], item["alllife"])
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


def battle(user_id, nickname):# 进攻
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        if "nickname" not in user:
            return "没有昵称不可进攻"
        # 过滤出对手
        otherUser = list(filter(
            lambda item: 'nickname' in item and nickname in item['nickname'], userAll))
        if not len(otherUser):
            return "对手不存在"
        # 判断对手是否弱小
        # 1.获取进攻列表 2.看看对手在不在列表
        otherUsers = battlelist(user_id,True)
        hasOtherUser = list(filter(
            lambda item: nickname in item['nickname'], otherUsers))
        if not len(hasOtherUser):
            return "禁止欺负弱小！"
        otherUser = hasOtherUser[0]

        # 过滤出一个可进攻角色
        atc = list(filter(
            lambda item: item['battle'], user['idol']))
        if not len(atc):
            return "没有可攻击的角色"
        userIdol = random.choice(atc)
        otherUserIdol = random.choice(otherUser['idol'])
        msg = "【%s】对战【%s】：\n" % (
            user["nickname"][0], nickname)

        if userIdol['attack'] <= otherUserIdol['defense']:  # 攻小于防
            msg += "\n【%s】VS【%s】无功而返" % (
                userIdol["nickname"], otherUserIdol["nickname"])
        elif userIdol['attack'] == otherUserIdol['attack']:  # 攻等于攻
            msg += "\n【%s】VS【%s】势均力敌" % (
                userIdol["nickname"], otherUserIdol["nickname"])
        elif userIdol['attack'] > otherUserIdol['defense']:  # 攻大于攻
            life = userIdol['attack'] - otherUserIdol['defense']
            otherUserIdol['life'] -= life  # 剩余生命值
            msg += "\n【%s】VS【%s】势如破竹，造成%s点伤害" % (
                userIdol["nickname"], otherUserIdol["nickname"], life)
            if otherUserIdol['life'] <= 0:
                otherUserIdol['life'] = 0
                otherUser['idol'].remove(otherUserIdol)
                otherUser['idol'].append(otherUser['otherIdol'][0])
                otherUser['otherIdol'].remove(otherUser['otherIdol'][0])
                otherUser['otherIdol'].append(otherUserIdol)
                msg += "\n【%s】战死沙场，替换成【%s】" % (
                    otherUserIdol["nickname"], otherUser['idol'][-1]["nickname"])
        userIdol['battle'] -= 1  # 可攻击次数减一
        userAll = levelProtect(userAll)  # 计算战斗力
        setting.writejson(userAll, "chess/user")
    return msg


def allBattle(user_id, nickname):# 全军出击
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        if "nickname" not in user:
            return "没有昵称不可进攻"
        # 过滤出对手
        otherUser = list(filter(
            lambda item: 'nickname' in item and nickname in item['nickname'], userAll))
        if not len(otherUser):
            return "对手不存在"
        # 判断对手是否弱小
        # 1.获取进攻列表 2.看看对手在不在列表
        otherUsers = battlelist(user_id,True)
        hasOtherUser = list(filter(
            lambda item: nickname in item['nickname'], otherUsers))
        if not len(hasOtherUser):
            return "禁止欺负弱小！"
        otherUser = hasOtherUser[0]

        # 过滤出一个可进攻角色
        atc = list(filter(
            lambda item: item['battle'], user['idol']))
        if not len(atc):
            return "没有可攻击的角色"
        num = len(atc)
        msg = "【%s】对战【%s】：\n" % (user["nickname"][0], nickname)
        while num:
            userIdol = random.choice(atc)
            otherUserIdol = random.choice(otherUser['idol'])
            if userIdol['attack'] <= otherUserIdol['defense']:  # 攻小于防
                msg += "\n【%s】VS【%s】无功而返" % (
                    userIdol["nickname"], otherUserIdol["nickname"])
            elif userIdol['attack'] == otherUserIdol['attack']:  # 攻等于攻
                msg += "\n【%s】VS【%s】势均力敌" % (
                    userIdol["nickname"], otherUserIdol["nickname"])
            elif userIdol['attack'] > otherUserIdol['defense']:  # 攻大于攻
                life = userIdol['attack'] - otherUserIdol['defense']
                otherUserIdol['life'] -= life  # 剩余生命值
                msg += "\n【%s】VS【%s】势如破竹，造成%s点伤害" % (
                    userIdol["nickname"], otherUserIdol["nickname"], life)
                if otherUserIdol['life'] <= 0:
                    otherUserIdol['life'] = 0
                    otherUser['idol'].remove(otherUserIdol)
                    otherUser['idol'].append(otherUser['otherIdol'][0])
                    otherUser['otherIdol'].remove(otherUser['otherIdol'][0])
                    otherUser['otherIdol'].append(otherUserIdol)
                    msg += "\n【%s】战死沙场，替换成【%s】" % (
                        otherUserIdol["nickname"], otherUser['idol'][-1]["nickname"])
            userIdol['battle'] -= 1  # 可攻击次数减一
            atc.remove(userIdol)
            num -= 1
        userAll = levelProtect(userAll)  # 计算战斗力
        setting.writejson(userAll, "chess/user")
    return msg


def reset():# 重置
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    for item in userAll:
        item["gold"] = 6
        for idol in item['idol']:
            idol['battle'] = 1
    setting.writejson(userAll, 'chess/user')
    return "已经重置"


def battlelist(user_id=False,reDict = False):# 攻击列表
    msg = ""
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    if user_id:
        # 判断用户在不在
        user = list(filter(lambda item: item['user_id'] == user_id, userAll))
        if not len(user):
            return "请先招募"
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
    for item in userAll:
        if "nickname" in item:
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
            msg += "\n%s %s %s 攻：%s 防：%s 血：%s/%s 进攻：%s" % (
                levelN(item["star"]), item["level"], item["nickname"],  item["attack"], item["defense"], item["life"], item["alllife"], item["battle"])
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
        msg = "%s的当前阵容(前六位)：" % user["nickname"][0]
        for item in user["idol"]:
            msg += "\n%s %s %s 攻：%s 防：%s 血：%s/%s 进攻：%s" % (
                levelN(item["star"]), item["level"], item["nickname"],  item["attack"], item["defense"], item["life"], item["alllife"], item["battle"])
        setting.writejson(userAll, 'chess/user')
        return msg


def attack(user_id):# 攻击阵容
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        userAllIdol = sorted(
            list(filter(lambda x: x["life"] > 0, userAllIdol)),
            key=lambda x: x['attack'], reverse=True) + list(filter(lambda x: x["life"] <= 0, userAllIdol))
        user["idol"] = userAllIdol[:6]
        user["otherIdol"] = userAllIdol[6:]
        msg = "%s的当前阵容(前六位)：" % user["nickname"][0]
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],levelN(item["star"]), item["level"], item["nickname"],  item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg


def defense(user_id):# 防御阵容
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        userAllIdol = sorted(
            list(filter(lambda x: x["life"] > 0, userAllIdol)),
            key=lambda x: x['defense'], reverse=True) + list(filter(lambda x: x["life"] <= 0, userAllIdol))
        user["idol"] = userAllIdol[:6]
        user["otherIdol"] = userAllIdol[6:]
        msg = "%s的当前阵容：" % user["nickname"][0]
        for item in user["idol"]:
            msg += "\n【%s】%s %s %s [CQ:emoji,id=9876]️%s [CQ:emoji,id=128737]️%s [CQ:emoji,id=9829]%s/%s" % ( item["battle"],levelN(item["star"]), item["level"], item["nickname"],  item["attack"], item["defense"], item["life"], item["alllife"])
        setting.writejson(userAll, 'chess/user')
    return msg


def nchange(user_id, m="N"):# 融化
    if m == "N":
        n = 10
    elif m == "R":
        n = 5
    else:
        return ''
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 判断用户在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
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


def levelN(num):# 计算星
    starN = num % 4
    moonN = int(num/4)
    sunN = int(moonN/4)
    crownN = int(sunN/4)
    return crownN * crown + sunN % 4 * sun + moonN % 4 * moon + starN * star


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
            user["nickname"][0], nCard["nickname"], nCard["level"], nCard["attack"], nCard["defense"], nCard["life"], nCard["alllife"], levelN(nCard["star"]), nCard["num"], "[CQ:emoji,id=128274]上锁" if nCard["lock"] else "[CQ:emoji,id=128275]未上锁")
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
        if len(nCard):
            return "你没有战败角色"
        msg = "战败："
        for item in nCard:
            msg += "%s、" % item["nickname"]
    return msg


def levelProtect(userAll):# 弱小保护
    for item in userAll:
        allIdol = item["idol"] + item["otherIdol"]
        allIdol = sorted(
            list(filter(lambda x: x["life"] > 0, item["idol"])), key=lambda x: x['attack'], reverse=True)
        if len(allIdol) < 6:
            item["power"] = 0
        else:
            item["power"] = int(sum([allIdol[i]["attack"]/0.15+allIdol[i]
                                     ["defense"]/0.15+allIdol[i]["alllife"] for i in range(6)]))
    userAll = sorted(userAll,
                     key=lambda i: i["power"],
                     reverse=True)
    return userAll
