# -*- coding: utf-8 -*-
from cqhttp import CQHttp
import setting
import chess

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
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.battle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:5] == "全军出击 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.allBattle(context['user_id'],context['message'][5:])
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
            bot.send(context, msg)
        elif context['message'][:3] == "出战 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.goBattle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "替换 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.changeBattle(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'] in ["攻击姿态","进攻姿态"]:
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.attack(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "防御姿态":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.defense(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "融合":
            msg = "[CQ:at,qq=%d]" % context['user_id']
            msg += chess.nchange(context['user_id'])
            msg += chess.nchange(context['user_id'],"R")
            bot.send(context, msg)
        elif context['message'][:3] == "我的 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.oneIdol(context['user_id'],context['message'][3:])
            bot.send(context, msg)
        elif context['message'][:3] == "上锁 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.lockOn(context['user_id'],context['message'][3:],False)
            bot.send(context, msg)
        elif context['message'][:3] == "解锁 ":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.lockOn(context['user_id'],context['message'][3:],True)
            bot.send(context, msg)
        elif context['message'] == "锁了":
            msg = "[CQ:at,qq=%d]\n" % context['user_id']
            msg += chess.hasLock(context['user_id'])
            bot.send(context, msg)
        elif context['message'] == "战败":
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
            elif cont.upper() in ["N","R","SR","SSR","UR"]:
                msg = "[CQ:at,qq=%d]\n" % context['user_id']
                msg += chess.idolhMy(context['user_id'],cont.upper())
                bot.send(context, msg)


# 如果修改了端口，请修改http-API插件的配置文件中对应的post_url
bot.run(host='127.0.0.1', port=8080)