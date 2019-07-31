# -*- coding: utf-8 -*-
import random
import setting

def lvUp(user_id,nickname): # 小星星
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 玩家在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        # 角色在不在
        has = list(
            filter(lambda item: item['nickname'] == nickname, userAllIdol))
        if not len(has):
            return "你没有%s" % nickname
        # 判断道具在不在或者够不够
        hasProp = list(
            filter(lambda item: item['name'] == "小星星", user["package"]))
        if not len(hasProp):
            return "你没有小星星"
        hasIdol = has[0]
        # 根据等级扣除小星星，最多四个
        need = {
            "N":1,
            "R":2,
            "SR":3,
            "SSR":4,
            "UR":4
        }
        needStar = need[hasIdol["level"]]
        if hasProp[0]["num"] < needStar:
            return "小星星数量不够"
        hasProp[0]["num"] -= needStar
        if hasProp[0]["num"] <= 0:
            user["package"].remove(hasProp[0])
        # 开始升级
        hasIdol["star"] += 1
        [attack,defense,life] = setting.dataUp(hasIdol["level"])
        hasIdol["attack"] += attack
        hasIdol["life"] += life
        hasIdol["alllife"] += life
        hasIdol["defense"] += defense
        if hasIdol["level"] in ["R","N"]:
            hasIdol["lock"] = True
        msg = "【%s】升星！\n星级：%s \n[CQ:emoji,id=9876]️%s ↑ %s\n[CQ:emoji,id=128737]️%s ↑ %s\n[CQ:emoji,id=9829]%s ↑ %s" % (
            hasIdol["nickname"], setting.levelN(hasIdol["star"]), hasIdol["attack"], attack, hasIdol["defense"], defense, hasIdol["life"], life)
        if hasIdol["level"] in ["N","R","SR"] and hasIdol["star"] >= 4 and hasIdol["skill"] == "未知": # 获得技能
            skill = setting.openjson("chess/skill")
            hasIdol["skill"] = random.choice(skill)["name"]
            msg += '\n获得技能：%s' % hasIdol["skill"]
        setting.writejson(userAll, 'chess/user')
    return msg
    

def tolive(user_id,nickname): # 复活
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 玩家在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        # 角色在不在
        has = list(
            filter(lambda item: item['nickname'] == nickname, userAllIdol))
        if not len(has):
            return "你没有%s" % nickname
        # 角色死没死
        hasIdol = has[0]
        if hasIdol["life"]:
            return "你的%s没有死亡" % nickname
        # 判断道具在不在或者够不够
        hasProp = list(
            filter(lambda item: item['name'] == "复活药水", user["package"]))
        if not len(hasProp):
            return "你没有复活药水"
        hasProp[0]["num"] -= 1
        if hasProp[0]["num"] <= 0:
            user["package"].remove(hasProp[0])
        # 开始复活
        hasIdol["life"] = hasIdol["alllife"]
        msg = "你的【%s】已复活" % nickname 
        setting.writejson(userAll, 'chess/user')
    return msg

def treatment(user_id,nickname): # 治疗
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 玩家在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        # 角色在不在
        has = list(
            filter(lambda item: item['nickname'] == nickname, userAllIdol))
        if not len(has):
            return "你没有%s" % nickname
        # 角色是不是残血
        hasIdol = has[0]
        if hasIdol["life"] >= hasIdol["alllife"] or hasIdol["life"]<=0:
            return "你的%s已死亡或不需要治疗" % nickname
        # 判断道具在不在或者够不够
        hasProp = list(
            filter(lambda item: item['name'] == "治疗药水", user["package"]))
        if not len(hasProp):
            return "你没有治疗药水"
        hasProp[0]["num"] -= 1
        if hasProp[0]["num"] <= 0:
            user["package"].remove(hasProp[0])
        # 开始复活
        hasIdol["life"] = hasIdol["alllife"]
        msg = "你的【%s】已恢复生命值" % nickname 
        setting.writejson(userAll, 'chess/user')
    return msg

def studySkill(user_id,cont): # 学技能
    msg = "请先招募"
    userAll = setting.openjson('chess/user')  # 打开本地user缓存到 userAll
    # 玩家在不在
    user = list(filter(lambda item: item['user_id'] == user_id, userAll))
    if len(user):
        [skill,nickname] = cont.split(" ")
        user = user[0]
        if user["uninstall"]:
            return "你已卸载退游"
        userAllIdol = user["idol"] + user["otherIdol"]
        # 角色在不在
        has = list(
            filter(lambda item: item['nickname'] == nickname, userAllIdol))
        if not len(has):
            return "你没有%s" % nickname
        # 判断道具在不在或者够不够
        hasProp = list(
            filter(lambda item: item['name'] == "技能书", user["package"]))
        if not len(hasProp):
            return "你没有技能书"
        # 技能在不在
        hasSkill = list(
            filter(lambda item: item['name'] == skill, setting.openjson('chess/skill')))
        if not len(hasSkill):
            return "【%s】不存在" % skill
        elif not hasSkill[0]["study"]:
            return "【%s】不可学习" % skill

        hasIdol = has[0]
        hasProp[0]["num"] -= 1
        if hasProp[0]["num"] <= 0:
            user["package"].remove(hasProp[0])
        # 开始复活
        hasIdol["skill"] = skill
        msg = "你的【%s】已学会【%s】" % (nickname,skill) 
        setting.writejson(userAll, 'chess/user')
    return msg

def backpack():
    data = setting.openjson("chess/pack")
    msg = "全部道具："
    for item in data:
        msg += "\n%s：%s" % (item["name"],item["msg"])
    return msg