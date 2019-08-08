# -*- coding: utf-8 -*-
import random
import setting

def DeathNot(user,userIdol,otherUser,otherUserIdol,oneSkill = False):
    msga = ''
    if otherUserIdol['life']<= 0: # 被攻击死亡
        otherUser['idol'] = list(filter(lambda x:x['nickname'] != otherUserIdol['nickname'],otherUser['idol']))
        if len(otherUser['otherIdol']) and otherUser['otherIdol'][0]["life"] > 0: # 如果场下存在存活的角色
            otherUser['idol'].append(otherUser['otherIdol'][0])
            otherUser['otherIdol'].remove(otherUser['otherIdol'][0])
        otherUserIdol['life'] = 0
        otherUser['otherIdol'].append(otherUserIdol)
        msga += "\n【%s】战死沙场" % otherUserIdol["nickname"]
        # 开始分配道具
        n = random.uniform(1, 100)
        list1 = [40,80,86,93,100]
        list2 = [20,40,60,80,100]
        list3 = [5,30,50,75,100]
        ini = setting.openjson('ini')
        Ko = int(user['KO']/ini['allUser']*100)
        if Ko<=25:
            Probably = list3
        elif Ko<=50:
            Probably = list2
        else:
            Probably = list1
        if oneSkill:
            Probably = [101,0,0,0]
        if n <= Probably[0]: # 小星星
            # 看看背包里有没有
            hasProp = list(filter(lambda x:x["name"] == "小星星",user["package"]))
            if len(hasProp):
                hasProp[0]["num"] += 1
            else:
                user["package"].append({
                    "name":"小星星",
                    "num": 1
                })
            msga += "\n【%s】获得战利品【小星星】" % user["nickname"][0]
        elif n <= Probably[1]: # 获得死亡角色
            # 判断自己有没有这个角色
            nickname = otherUserIdol["nickname"]
            # 判断角色是否存在
            userAllIdol = user["idol"] + user["otherIdol"]
            user["idol"] = []
            has = list(
                filter(lambda item: item['nickname'] == nickname, userAllIdol))
            if not len(has):
                # 在库中找到一级的该角色
                path = "chess/idol/%s" % otherUserIdol["level"].lower()
                idol = list(
                    filter(lambda item: item['nickname'] == nickname, setting.openjson(path)))[0]
                userAllIdol.append(idol)
                user["idol"] = userAllIdol[:6]
                user["otherIdol"] = userAllIdol[6:]
                msga += "\n【%s】获得战利品【%s】【%s】NEW！" % (user["nickname"][0],otherUserIdol["level"],nickname)
            else:
                # 升级
                hasIdol = has[0]
                hasIdol["num"] += 1
                msga += "\n【%s】获得战利品【%s】【%s】" % (user["nickname"][0],otherUserIdol["level"],nickname)
                if hasIdol["num"] >= 4:
                    hasIdol["star"] += 1
                    hasIdol["num"] -= 4
                    [attack,defense,life] = setting.dataUp(hasIdol["level"])
                    hasIdol["attack"] += attack
                    hasIdol["life"] += life
                    hasIdol["alllife"] += life
                    hasIdol["defense"] += defense
                    # if hasIdol["level"] in ["R","N"]:
                    #     hasIdol["lock"] = True
                    msga += "\n【%s】升星！\n星级：%s \n[CQ:emoji,id=9876]️%s ↑ %s\n[CQ:emoji,id=128737]️%s ↑ %s\n[CQ:emoji,id=9829]%s ↑ %s" % (
                        hasIdol["nickname"], setting.levelN(hasIdol["star"]), hasIdol["attack"], attack, hasIdol["defense"], defense, hasIdol["life"], life)
                    if hasIdol["level"] in ["N","R","SR"] and hasIdol["star"] >= 4 and hasIdol["skill"] == "未知": # 获得技能
                        skill = list(filter(lambda x:x["study"], setting.openjson("chess/skill")))
                        hasIdol["skill"] = random.choice(skill)["name"]
                        msga += '\n获得技能：%s' % hasIdol["skill"]

                user["idol"] = userAllIdol[:6]
                user["otherIdol"] = userAllIdol[6:]
        elif n <= Probably[2]: # 技能书
            # 看看背包里有没有
            hasProp = list(filter(lambda x:x["name"] == "技能书",user["package"]))
            if len(hasProp):
                hasProp[0]["num"] += 1
            else:
                user["package"].append({
                    "name":"技能书",
                    "num": 1
                })
            msga += "\n【%s】获得战利品【技能书】" % user["nickname"][0]
        elif n <= Probably[3]: # 治疗药水
            # 看看背包里有没有
            hasProp = list(filter(lambda x:x["name"] == "复活药水",user["package"]))
            if len(hasProp):
                hasProp[0]["num"] += 1
            else:
                user["package"].append({
                    "name":"复活药水",
                    "num": 1
                })
            msga += "\n【%s】获得战利品【复活药水】" % user["nickname"][0]
        elif n <= Probably[4]: # 治疗药水
            # 看看背包里有没有
            hasProp = list(filter(lambda x:x["name"] == "治疗药水",user["package"]))
            if len(hasProp):
                hasProp[0]["num"] += 1
            else:
                user["package"].append({
                    "name":"治疗药水",
                    "num": 1
                })
            msga += "\n【%s】获得战利品【治疗药水】" % user["nickname"][0]
    if userIdol['life']<= 0: # 主动攻击死亡
        user['idol'] = list(filter(lambda x:x['nickname'] != userIdol['nickname'],user['idol']))
        if len(user['otherIdol']) and  user['otherIdol'][0]["life"] > 0:
            user['idol'].append(user['otherIdol'][0])
            user['otherIdol'].remove(user['otherIdol'][0])
        userIdol['life'] = 0
        user['otherIdol'].append(userIdol)
        msga += "\n【%s】战死沙场" % userIdol["nickname"]
    return [msga,user,userIdol,otherUser,otherUserIdol]

def BlastABall(user,userIdol,otherUser,otherUserIdol): # 一击致命
    msgs = "\n【%s *一击致命*】VS【%s】" % (
        userIdol["nickname"], otherUserIdol["nickname"])
    otherUserIdol['life'] = 0
    [msga,user,userIdol,otherUser,otherUserIdol] = DeathNot(user,userIdol,otherUser,otherUserIdol,True)
    msgs += msga
    return [msgs,user,userIdol,otherUser,otherUserIdol]

def Backstab(user,userIdol,otherUser,otherUserIdol): # 背刺
    life = int(userIdol['attack']*2)
    if otherUserIdol["skill"] == "尖刺防御" and random.uniform(1, 100)<=25: # 尖刺防御
        msgs = "\n【%s *背刺*】VS【%s *尖刺防御*】造成%s点伤害，受到%s点反伤" % (
            userIdol["nickname"], otherUserIdol["nickname"],life,life)
        userIdol['life'] -= life  # 剩余生命值
    else:
        msgs = "\n【%s *背刺*】VS【%s】造成%s点伤害" % (
            userIdol["nickname"], otherUserIdol["nickname"],life)
    
    otherUserIdol['life'] -= life # 剩余生命值
    [msga,user,userIdol,otherUser,otherUserIdol] = DeathNot(user,userIdol,otherUser,otherUserIdol)
    msgs += msga
    return [msgs,user,userIdol,otherUser,otherUserIdol]

def awaken(user,userIdol,otherUser,otherUserIdol): # 觉醒
    life = (userIdol['attack'] - otherUserIdol['defense'])*5
    if otherUserIdol["skill"] == "尖刺防御" and random.uniform(1, 100)<=25: # 尖刺防御
        msgs = "\n【%s *觉醒*】VS【%s *尖刺防御*】造成%s点伤害，受到%s点反伤" % (
            userIdol["nickname"], otherUserIdol["nickname"],life,life)
        userIdol['life'] -= life # 剩余生命值
    else:
        msgs = "\n【%s *觉醒*】VS【%s】造成%s点伤害" % (
            userIdol["nickname"], otherUserIdol["nickname"],life)
    
    otherUserIdol['life'] -= life  # 剩余生命值
    [msga,user,userIdol,otherUser,otherUserIdol] = DeathNot(user,userIdol,otherUser,otherUserIdol)
    msgs += msga
    return [msgs,user,userIdol,otherUser,otherUserIdol]