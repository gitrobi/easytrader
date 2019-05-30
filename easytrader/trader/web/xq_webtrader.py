# -*- coding: utf-8 -*-
import numbers
import os
import time
import datetime

import requests

from easytrader import exceptions, helpers
from easytrader.trader.web import webtrader
from easytrader.log import log


class XueQiuWebTrader(webtrader.WebTrader):
    config_path = os.path.dirname(__file__) + "/xq.json"

    @staticmethod
    def _time_strftime(time_stamp):
        try:
            local_time = time.localtime(time_stamp / 1000)
            return time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        # pylint: disable=broad-except
        except Exception:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    _HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/64.0.3282.167 Safari/537.36",
        #"Host": "xueqiu.com",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Referer": "https://xueqiu.com/performance",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, **kwargs):
        super(XueQiuWebTrader, self).__init__()

        # 资金换算倍数
        self.multiple = (
            kwargs["initial_assets"] if "initial_assets" in kwargs else 1000000
        )
        if not isinstance(self.multiple, numbers.Number):
            raise TypeError("initial assets must be number(int, float)")
        if self.multiple < 1e3:
            raise ValueError("雪球初始资产不能小于1000元，当前预设值 {}".format(self.multiple))

        self.s = requests.Session()
        self.s.verify = False
        self.s.headers.update(self._HEADERS)
        self.account_config = None

    def autologin(self, **kwargs):
        """
        使用 cookies 之后不需要自动登陆
        :return:
        """
        self._set_cookies(self.account_config["cookies"])
        portfolio_code = self.account_config.get("portfolio_code", "ch")
        self._gid = self._get_portfolio_gid(portfolio_code)

    def _set_cookies(self, cookies):
        """设置雪球 cookies，代码来自于
        https://github.com/shidenggui/easytrader/issues/269
        :param cookies: 雪球 cookies
        :type cookies: str
        """
        cookie_dict = helpers.parse_cookies_str(cookies)
        self.s.cookies.update(cookie_dict)

    def _prepare_account(self, user="", password="", **kwargs):
        """
        转换参数到登录所需的字典格式
        :param cookies: 雪球登陆需要设置 cookies， 具体见
            https://smalltool.github.io/2016/08/02/cookie/
        :param portfolio_code: 组合代码
        :param portfolio_market: 交易市场， 可选['cn', 'us', 'hk'] 默认 'cn'
        :return:
        """
        if "portfolio_code" not in kwargs:
            raise TypeError("雪球登录需要设置 portfolio_code(组合代码) 参数")
        if "portfolio_market" not in kwargs:
            kwargs["portfolio_market"] = "cn"
        if "cookies" not in kwargs:
            raise TypeError(
                "雪球登陆需要设置 cookies， 具体见"
                "https://smalltool.github.io/2016/08/02/cookie/"
            )
        self.account_config = {
            "cookies": kwargs["cookies"],
            "portfolio_code": kwargs["portfolio_code"],
            "portfolio_market": kwargs["portfolio_market"],
        }

    def _virtual_to_balance(self, virtual):
        """
        虚拟净值转化为资金
        :param virtual: 雪球组合净值
        :return: 换算的资金
        """
        return virtual * self.multiple

    def _search_stock_info(self, code):
        """
        通过雪球的接口获取股票详细信息
        :param code: 股票代码 000001
        :return:
        """
        url = self.config["search_url"] % (code)
        r = self.s.get(url)
        resjson = r.json()
        stocks = resjson.get('stocks', None)
        stock = None
        if len(stocks) > 0:
            stock = stocks[0]
        return stock

    def _get_portfolio_gid(self, portfolio_code):
        """获取组合信息的gid"""
        r = self.s.get(self.config["portfolio_gids"])
        resjson = r.json()
        result_code = resjson['result_code']
        result_data = resjson['result_data']
        if result_code == '60000':
            trans_groups = result_data.get('trans_groups', None)

        gid = None
        if trans_groups is not None and len(trans_groups) >0:
            for one in trans_groups:
                if one['name'] == portfolio_code:
                    gid = one['gid']
                    break

        if gid is None:
            raise Exception("cannot get trans_groups gid for '%s'"(portfolio_code))
        return gid

    def _get_performances(self):
        url = self.config["performances_url"] % (self._gid)
        r = self.s.get(url)
        resjson = r.json()
        result_code = resjson['result_code']
        result_data = resjson['result_data']
        if result_code == '60000':
            performances = result_data.get('performances', None)
        if performances is None:
            raise Exception("cannot get performances for '%s'"(self._gid))
        return performances

    def get_balance(self):
        """
        获取账户资金状况
        :return:
        """
        performances = self._get_performances()
        performance = performances[1]
        # xq_positions = performance['list']
        asset_balance = performance['assets']
        cash = performance['cash']
        market = performance['market_value']
        return [
            {
                "asset_balance": asset_balance,
                "current_balance": cash,
                "enable_balance": cash,
                "market_value": market,
                "money_type": u"人民币",
                "pre_interest": 0.25,
            }
        ]

    def get_position(self):
        """
        获取持仓
        :return:
        """
        performances = self._get_performances()
        performance = performances[1]
        xq_positions = performance['list']
        return xq_positions

    @property
    def history(self):
        log.warning("雪球新版不支持委托")
        return None

    def get_entrust(self):
        """
        获取委托单(目前返回20次调仓的结果)
        操作数量都按1手模拟换算的
        :return:
        """
        log.warning("雪球新版不支持委托")
        return None

    def cancel_entrusts(self):
        """
        对未成交的调仓进行伪撤单
        :return:
        """
        log.warning("雪球新版不支持委托")
        return True

    def cancel_entrust(self, entrust_no):
        """
        对未成交的调仓进行伪撤单
        :param entrust_no:
        :return:
        """
        log.warning("雪球新版不支持委托")
        return True

    def adjust_weight(self, stock_code, weight):
        """
        雪球组合调仓, weight 为调整后的仓位比例
        :param stock_code: str 股票代码
        :param weight: float 调整之后的持仓百分比， 0 - 100 之间的浮点数
        """
        log.warning("雪球新版不支持调仓")
        return None

    def _trade(self, security, price=0, shares=0, amount=0, entrust_bs="buy"):
        """
        调仓
        :param security:
        :param price:
        :param shares:
        :param amount:
        :param entrust_bs:
        :return:
        """
        stock = self._search_stock_info(security)
        balance = self.get_balance()[0]

        if stock is None:
            raise exceptions.TradeError(u"没有查询要操作的股票信息")
        if not amount:
            amount = price * shares
        if balance["current_balance"] < amount and entrust_bs == "buy":
            raise exceptions.TradeError(u"没有足够的现金进行操作")
        if amount == 0:
            raise exceptions.TradeError(u"操作金额不能为零")

        # 获取原有仓位信息
        position_list = self.get_position()

        # 调整后的持仓
        is_have = False
        for position in position_list:
            if position["symbol"] == stock["code"]:
                is_have = True
                old_shares = position["shares"]
                if entrust_bs == "sell":
                    if shares > old_shares:
                        raise exceptions.TradeError(u"操作数量大于实际可卖出数量")

        if not is_have:
            if entrust_bs == "sell":
                raise exceptions.TradeError(u"没有持有要卖出的股票")

        if entrust_bs == "buy":
            type = 1
        else: # "sell"
            type = 2

        today = datetime.date.today().strftime("%Y-%m-%d")
        tax = 0
        commission = 0

        data = {
            "type": type,
            "date": today,
            "comment": None,
            "gid": self._gid,
            "symbol": security,
            "price": price,
            "shares": shares,
            "tax": tax,
            "commission": commission
        }

        try:
            res = self.s.post(self.config["trade_url"], data=data)
        except Exception as e:
            log.warning("交易失败: %s ", e)
            return None
        else:
            resjson = res.json()
            result_code = resjson['result_code']
            result_data = resjson['result_data']
            return result_data

    def buy(self, security, price=0, shares=0, amount=0, entrust_prop=0):
        """买入卖出股票
        :param security: 股票代码
        :param price: 买入价格
        :param shares: 买入股数
        :param amount: 买入总金额
        :param entrust_prop:
        """
        return self._trade(security, price, shares, amount, "buy")

    def sell(self, security, price=0, shares=0, amount=0, entrust_prop=0):
        """卖出股票
        :param security: 股票代码
        :param price: 卖出价格
        :param shares: 卖出股数
        :param amount: 卖出总金额
        :param entrust_prop:
        """
        return self._trade(security, price, shares, amount, "sell")
