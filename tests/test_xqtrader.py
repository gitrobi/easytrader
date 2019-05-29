# coding: utf-8
import unittest

from easytrader.exceptions import TradeError
from easytrader.xqtrader import XueQiuTrader


class TestXueQiuTrader(unittest.TestCase):
    def test_prepare_account(self):
        user = XueQiuTrader()
        params_without_cookies = dict(
            portfolio_code="ZH123456", portfolio_market="cn"
        )
        with self.assertRaises(TypeError):
            user._prepare_account(**params_without_cookies)

        params_without_cookies.update(cookies="123")
        user._prepare_account(**params_without_cookies)
        self.assertEqual(params_without_cookies, user.account_config)

    def test_get_balance(self):
        user = XueQiuTrader()
        user.prepare('../xq.json')
        balance = user.get_balance()
        self.assertIsNotNone(balance)

    def test_buy(self):
        user = XueQiuTrader()
        user.prepare('../xq.json')

        security = 'SZ159901'
        price = 4.282
        shares = 100
        result = user.buy(security, price, shares)
        self.assertEqual(result['amount'], 428.2)
        self.assertIsNotNone(result['gid'], user._gid)

    def test_sell(self):
        user = XueQiuTrader()
        user.prepare('../xq.json')

        security = 'SZ159901'
        price = 4.282
        shares = 200
        try:
            result = user.sell(security, price, shares)
            self.assertEqual(result['amount'], 428.2)
            self.assertIsNotNone(result['gid'], user._gid)
        except TradeError as te:
            self.assertEqual(str(te), "操作数量大于实际可卖出数量")

        shares = 100
        result = user.sell(security, price, shares)
        self.assertEqual(result['amount'], 428.2)
        self.assertIsNotNone(result['gid'], user._gid)

        try:
            result = user.sell(security, price, shares)
            self.assertEqual(result['amount'], 428.2)
            self.assertIsNotNone(result['gid'], user._gid)
        except TradeError as te:
            self.assertEqual(str(te), "操作数量大于实际可卖出数量")




