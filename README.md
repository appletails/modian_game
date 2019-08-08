# modian_game

[TOC]

## 简介
自娱自乐的机器人<br>
有问题加Q群：691963133<br>
或者微博私信[-青春的小尾巴-](https://weibo.com/amber0401)

## 说明
* 使用前先在`jsons/chess`下新建一个`user.json`，内容为`[]`

## 更新记录
* 2019/08/06
  * 恢复`复活`药水
  * 提升了`觉醒`、`嗜血`和`一击致命`的触发概率
  * `一击致命`必得小星星
  * 修复了抢角色升级任会自动上锁的bug
  * 修复了进攻/复仇时角色死亡无法正确执行的bug
  * 新增全部解锁
  * 新增攻击过所有玩家后`来个对手`的反馈
  * 宵禁后战队不足6人自动补齐
  * 调整了json文件的目录结构

* 2019/07/30
  * 删除`复活`药水
  * 调整了道具的掉落几率
  * 新增了根据角色排名掉率道具
  * 背刺伤害调整为2倍攻击力
  * 下调了N,R的成长值，上调了SSR,UR的成长值
  * 【来个对手】不再推送战斗力为0的玩家
  * 【复仇】bug已修复
  * `SR`也可被融合
  * 下调n，r，sr生命值

* 2019/07/25
  * 删除【我的对手】和【进攻list】指令
  * 开放攻击，不再保护
  * 对同一玩家一天只能攻击6次（等于全军出击一次）
  * 复仇对手不消耗攻击次数值，复仇攻击最多可以攻击6次（等于全军出击一次）
  * 添加【仇人】指令，查看可复仇的仇人
  * 晚上1点至早上七点宵禁
  * 周六周日早上6点复活和恢复所有角色 ---- 待完成
  * 部分指令错误不再反馈消息

* 2019/07/24
  * 修复了`user.json`为空时使用【进攻list】控制台报错的问题
  * 修复了`user.json`为空时【融合】指令出现两次提示的问题
  * 修复了`user.json`为空时【我的对手】控制台报错的问题
  * 修复了存活角色不足6个时【攻击姿态】等会派出死亡角色的问题
  * 修复了【出战 】等指令在没有目标是任会执行的问题
  * 修复了【道具】指令无效的问题
  * 修复了【全军出击】弱小判断有误的问题
  * 修复了【残血】指令时候死亡角色会出现的问题
  * 修复了【出击 背刺】后死亡角色会消失的问题
  * 修复了【学习 a b】无效的问题
  * 调整了【学习 背刺 王晓佳】为【学习背刺 王晓佳】
  * 调整全角色稀有度和属性和技能
  * 【一击致命】为小鞠专属技能，不可学习获得
  * 初次招募必得方琪修改为初次招募必得SSR任意角色
  * 调整【嗜血】触发时若生命值已满会突破生命上限
  * 其他更新

* 2019/07/23
  * 修复了【攻击姿态】后死亡角色消失的bug
  * 修复了【背刺】会反伤自己的bug
  * 修复了角色没有技能时会显示`**`的问题
  * 修改了【替换】【出击】后信息显示格式
  * 修改了角色没有技能时查看角色不再显示`技能：未知`
  * 新增【我的一击致命】等指令，查看拥有该技能的角色
  * 新增【出击 一击致命】等指令，优先出战拥有该技能的角色
  * 新增击杀角色掉落道具、被击杀角色
  * 新增【小星星 王晓佳】等使用道具指令
  * 新增【残血】查看自己的残血角色
  * 新增【道具】查看道具和描述
  * 新增【我的道具】查看自己的道具
  * 修复了战斗力计算异常
  * 添加两星N、R自动上锁提示

* 2019/07/22
  * 合并进攻和全军出击函数`battle`，剥离对战内容函数`sBattle`
  * 剥离角色死亡的判断函数，新增`skill.py`技能战斗判断函数
  * 添加角色技能，SSR和UR初始有技能，其他等级升级到月亮时随机获得技能，技能概率触发
  * 区别SSR、UR和其他等级角色的成长属性
  * 新增【技能】指令查看技能描述

* 2019/07/21
  * 调整了【进攻】和【全军出击】的显示方式
  * 玩家昵称字段类型改为`list`
  * 【我的UR】等指令不再区分大小写
  * 调整的【我的信息】等指令的显示
  * 【我的对手】至少保留自己以外的三个低级对手
  * `N`和`R`升级自动上锁
  * 提升SSR和UR的基础属性

* 2019/07/20
  * 将【融合R/r】指令合并到【融合】中
  * 删除【我的角色】指令，新增【我的UR】等指令
  * 调整【招募】和【梭哈】的显示方式

* 2019/07/19
  * 调整战斗力计算，新增`power`字段
  * 添加【禁止欺负弱小】反馈
  * 回复时艾特操作者
  * 调整等级的显示，进率4，增加太阳月亮皇冠
  * 修复了角色战死战力不重新计算的bug

* 2019/07/18
  * 死亡角色会正确的退场，自动替换场下攻击力最高的角色上场
  * 删除反杀操作，防御力起到正常抵抗作用
  * 删除【我的阵容】指令
  * 【替换】和【出战】不能派出战死角色
  * 调整角色稀有度
  * 提升各稀有度角色的招募概率
  * 调整全角色防御力
  * 添加`uninstall`卸载退游字段
  * 调整【我的 王晓佳】的显示

* 2019/07/18
  * 第一次提交

## 指令
指令 | 描述
:-:|:-:
招募 | 消耗一个招募值招募一个角色
梭哈 | 消耗所有招募值招募对应数量的角色
我的信息 | 查看当前出战角色的信息
进攻 师兄 | 随机使用一个有攻击次数的角色攻击师兄的随机角色
全军出击 师兄 | 有攻击次数的所有角色攻击师兄的随机角色
出战 A B C D E F | 没什么好说的
替换 A B | A下场B上场
攻击姿态/进攻姿态 | 按存活角色的攻击力自动上阵
防御姿态 | 按存活角色的防御力自动上阵
出击 一击致命 | 优先上场一击致命，剩下的按攻击力来
我的一击致命 | 查看拥有觉醒的角色
融合 | 融合未上锁的N和R卡，N10换1，R5换1
上锁 王晓佳 | 上锁，不会被融合
解锁 王晓佳 | 没什么好说的
全部解锁 | 没什么好说的
锁了 | 查看全部上锁的角色
我的 王晓佳 | 查看王晓佳的信息
战败 | 查看全部战败的角色
残血 | 查看受伤的角色
技能 | 查看技能描述
道具 | 查看道具描述，击杀角色掉落道具
升级 王晓佳 | 升星，需要一些`小星星`
治疗 王晓佳 | 治疗，需要`治疗药水`
复活 王晓佳 | 复活，需要`复活药水`
学习觉醒 王晓佳 | 让王晓佳学习觉醒，需要`技能书`

## 备注
- 招募值每整10分钟恢复一点，最多保存6点
- 进攻次数每整小时恢复所有角色攻击次数
- 宵禁时间为凌晨1点至早上7点