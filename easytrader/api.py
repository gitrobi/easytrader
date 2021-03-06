# -*- coding: utf-8 -*-
import logging
import sys

from .log import log

from easytrader.follower.joinquant_follower import JoinQuantFollower
from easytrader.follower.ricequant_follower import RiceQuantFollower
from easytrader.follower.xq_follower import XueQiuFollower
from easytrader.trader.web.xq_webtrader import XueQiuWebTrader

if not sys.platform.startswith("darwin"):
    from easytrader.trader.client.win.clienttrader import ClientTrader
    from easytrader.trader.client.win.gj_clienttrader import GJClientTrader
    from easytrader.trader.client.win.yh_clienttrader import YHClientTrader
    from easytrader.trader.client.win.ht_clienttrader import HTClientTrader
else:
    from easytrader.trader.client.mac.clienttrader import ClientTrader
    from easytrader.trader.client.mac.yh_clienttrader import YHClientTrader



def use(broker, debug=True, **kwargs):
    """用于生成特定的券商对象
    :param broker:券商名支持 ['yh_client', '银河客户端'] ['ht_client', '华泰客户端']
    :param debug: 控制 debug 日志的显示, 默认为 True
    :param initial_assets: [雪球参数] 控制雪球初始资金，默认为一百万
    :return the class of trader

    Usage::

        >>> import easytrader
        >>> user = easytrader.use('xq')
        >>> user.prepare('xq.json')
    """
    if not debug:
        log.setLevel(logging.INFO)
    if broker.lower() in ["xq", "雪球"]:
        return XueQiuWebTrader(**kwargs)
    if broker.lower() in ["yh_client", "银河客户端"]:
        return YHClientTrader()
    if broker.lower() in ["ht_client", "华泰客户端"]:
        return HTClientTrader()
    if broker.lower() in ["gj_client", "国金客户端"]:
        return GJClientTrader()
    if broker.lower() in ["ths", "同花顺客户端"]:
        return ClientTrader()

    raise NotImplementedError


def follower(platform, **kwargs):
    """用于生成特定的券商对象
    :param platform:平台支持 ['jq', 'joinquant', '聚宽’]
    :param initial_assets: [雪球参数] 控制雪球初始资金，默认为一万,
        总资金由 initial_assets * 组合当前净值 得出
    :param total_assets: [雪球参数] 控制雪球总资金，无默认值,
        若设置则覆盖 initial_assets
    :return the class of follower

    Usage::

        >>> import easytrader
        >>> user = easytrader.use('xq')
        >>> user.prepare('xq.json')
        >>> jq = easytrader.follower('jq')
        >>> jq.login(user='username', password='password')
        >>> jq.follow(users=user, strategies=['strategies_link'])
    """
    if platform.lower() in ["rq", "ricequant", "米筐"]:
        return RiceQuantFollower()
    if platform.lower() in ["jq", "joinquant", "聚宽"]:
        return JoinQuantFollower()
    if platform.lower() in ["xq", "xueqiu", "雪球"]:
        return XueQiuFollower(**kwargs)
    raise NotImplementedError
