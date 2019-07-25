# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import chess
import pack

import re

bot = CQHttp(api_root='http://127.0.0.1:5700/')
# 也可以添加access_token和secret，更加安全
# bot = CQHttp(api_root='http://127.0.0.1:5700/',
#              access_token='your-token',
#              secret='your-secret')
# 如果设置了access_token和secret，请修改http-API插件的配置文件中对应的部分

# 群消息操作
@bot.on_message('group')
def handle_msg(context):
    # 开始进行关键字触发
    if context['group_id'] in setting.groupid():
        # 关键词回复
        if context['message'] == "招募":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            nickname = context['sender']['card'] if context['sender']['card'] else context['sender']['nickname']
            msg += chess.DrawCard(context['user_id'],nickname)
            bot.send(context, msg)
        elif context['message'][:3] == "进攻 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.battle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:5] == "全军出击 ":
            if not len(context['message'][5:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.battle(context['user_id'],context['message'][5:],True)
            bot.send(context, msg)
        elif context['message'] == "梭哈":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.suoha(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "重置" and context['user_id'] == 476297692:
            msg = chess.reset()
            bot.send(context, msg)
        elif context['message'] == "进攻list":
            msg = chess.battlelist()
            if msg:
                bot.send(context, msg)
        elif context['message'][:3] == "出战 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.goBattle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "替换 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.changeBattle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'] in ["攻击姿态","进攻姿态"]:
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.attack(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "防御姿态":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.attack(context['user_id'],True)
            bot.send(context, msg)
        elif context['message'] == "融合":
            msg = "[CQ:at,qq=%d]" % context['user_id']
            msga = chess.nchange(context['user_id'])
            msg += msga
            if msga != "请先招募":
                msg += chess.nchange(context['user_id'],"R")
            bot.send(context, msg)
        elif context['message'][:3] == "我的 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.oneIdol(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "上锁 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.lockOn(context['user_id'],context['message'][3:],False)
            bot.send(context, msg)
        elif context['message'][:3] == "解锁 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.lockOn(context['user_id'],context['message'][3:],True)
            bot.send(context, msg)
        elif context['message'] == "锁了":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.hasLock(context['user_id'])
            bot.send(context, msg)
        elif context['message'] in ["战败","阵亡"]:
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.dead(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "我的对手":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.battlelist(context['user_id'])
            bot.send(context, msg)
        elif context['message'][:2] == '我的':
            cont = context['message'][2:]
            if cont  == "信息":
                msg = "[CQ:at,qq=%d]\n" % context['user_id']
                msg += chess.seachMy(context['user_id'])
                bot.send(context, msg)
            elif cont  == "道具":
                msg = "[CQ:at,qq=%d]\n" % context['user_id']
                msg += chess.seachPack(context['user_id'])
                bot.send(context, msg)
            elif cont.upper() in ["N","R","SR","SSR","UR"]:
                msg = "[CQ:at,qq=%d]\n" % context['user_id']
                msg += chess.idolhMy(context['user_id'],cont.upper())
                bot.send(context, msg)
            elif cont in [i["name"] for i in setting.openjson("chess/skill")]:
                msg = "[CQ:at,qq=%d]\n" % context['user_id']
                msg += chess.showSkill(context['user_id'],cont)
                bot.send(context, msg)
        elif context['message'] == "技能":
            msg = chess.skills()
            bot.send(context, msg)
        elif context['message'][:3] == "出击 " and context['message'][3:] in [i["name"] for i in setting.openjson("chess/skill")]:
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.goSkill(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'] == "道具":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += pack.backpack()
            bot.send(context, msg)
        elif context['message'][:3] == "升级 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += pack.lvUp(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "复活 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += pack.tolive(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "治疗 ":
            if not len(context['message'][3:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += pack.treatment(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:2] == "学习":
            if not len(context['message'][2:]):
                return
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += pack.studySkill(context['user_id'],context['message'][2:])
            bot.send(context, msg)
        elif context['message'] == "残血":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.blood(context['user_id'])
            bot.send(context, msg)



# 如果修改了端口，请修改http-API插件的配置文件中对应的post_url
bot.run(host='127.0.0.1', port=8080)