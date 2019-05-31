import applescript
import time

from easytrader.trader.trader import BaseTrader
from easytrader import exceptions


class Assets :
    def __init__(self, asset_list):
        self.total_assets_desc = asset_list[0][0]
        self.total_assets = asset_list[0][1]
        self.total_market_value_desc = asset_list[1][0]
        self.total_market_value = asset_list[1][1]
        self.total_earning_desc = asset_list[2][0]
        self.total_earning = asset_list[2][1]
        self.today_earning_desc = asset_list[3][0]
        self.today_earning = asset_list[3][1]
        self.asset_balance_desc = asset_list[4][0]
        self.asset_balance = asset_list[4][1]
        self.fetch_balance_desc = asset_list[5][0]
        self.fetch_balance = asset_list[5][1]
        self.enable_balance_desc = asset_list[6][0]
        self.enable_balance = asset_list[6][1]

    def __str__(self):
        ss = "{}:{},{}:{},{}:{},{}:{},{}:{},{}:{},{}:{}".format(
            self.total_assets_desc, self.total_assets,
            self.total_market_value_desc,self.total_market_value,
            self.total_earning_desc, self.total_earning,
            self.today_earning_desc, self.today_earning,
            self.asset_balance_desc, self.asset_balance,
            self.fetch_balance_desc, self.fetch_balance,
            self.enable_balance_desc, self.enable_balance)
        return ss


class Positon :
    '''
    ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户']
    ['131990', '标准券', '100.000', '0.000', '0.000', '0', '0', '0', '0', '0.000', '0.000', '深圳Ａ股', '0200802943']
    '''
    def __init__(self, position_list):
        self.desc_list = position_list[0]
        self.security_list = position_list[1:]

    def __str__(self):
        ss = str(self.desc_list) + '\n'
        for one in self.security_list :
            ss = ss + str(one) + '\n'
        return ss


class ClientTrader(BaseTrader):

    scpt = applescript.AppleScript('''
        #--------------------------------------------------------------------------------------
        on query_assets()
            tell application "System Events"
                tell process "同花顺至尊版"
                    tell window 1
                        -- to do
                        delay 0.1
                        set v_result to get name of UI elements of row of table 1 of scroll area 1
                        return v_result
                    end tell
                end tell
            end tell
        end query_assets

        #--------------------------------------------------------------------------------------
        on query_position()
            tell application "System Events"
                tell process "同花顺至尊版"
                    tell window 1
                    delay 0.1
                    set v_result to {}
    				set v_result to v_result & {(get name of button of group 1 of table 1 of scroll area 4)}
    				set v_result to v_result & (get value of UI elements of row of table 1 of scroll area 4)
    				return v_result
                    end tell
                end tell
            end tell
        end query_position

        #--------------------------------------------------------------------------------------
        on buy_entrust(para, isdo)
            tell application "System Events"
                tell process "同花顺至尊版"
                    tell window 1
                        set v_stock_code to item 1 of para
                        set v_price to item 2 of para
                        set v_count to item 3 of para
                        --delay 0.1
                        set buy_or_sell to get value of attribute "AXTitle" of button 27
                        if buy_or_sell = "确定卖出" then
                            click button 16
                        end if

                        -- 证券代码
                        set value of attribute "AXFocused" of text field 2 to true
                        set value of text field 2 to v_stock_code
                        action "AXConfirm" of text field 2

                        -- 等待刷新股票名称
                        repeat until the length of (get value of text field 1) > 0
                        end repeat

                        -- 证券价格
                        set value of text field 1 to v_price

                        -- 证券数量
                        set value of text field 3 to v_count

                        if button "确定买入" exists then
                            click button "确定买入"
                        end if

                        repeat until sheet 1 exists
                        end repeat

                        set v_result to {}
                        if isdo then
                            set v_result to v_result & "Y"
                            click button 1 of sheet 1

                            if sheet 1 exists then
                                set v_result to v_result & (get value of static text 2 of sheet 1)  
                                click button 1 of sheet 1
                            end if
                        else 
                            set v_result to v_result & "N"
                            click button 2 of sheet 1
                        end if

                        return v_result

    		        end tell
    		    end tell
            end tell
    	end buy_entrust

        #--------------------------------------------------------------------------------------
        on sell_entrust(para, isdo)
            tell application "System Events"
                tell process "同花顺至尊版"
                    tell window 1
                        set v_stock_code to item 1 of para
                        set v_price to item 2 of para
                        set v_count to item 3 of para
                        --delay 0.1
                        set buy_or_sell to get value of attribute "AXTitle" of button 27
                        if buy_or_sell = "确定买入" then
                            click button 16
                        end if

                        -- 证券代码
                        set value of attribute "AXFocused" of text field 2 to true
                        set value of text field 2 to v_stock_code
                        action "AXConfirm" of text field 2

                        -- 等待刷新股票名称
                        repeat until the length of (get value of text field 1) > 0
                        end repeat

                        -- 证券价格
                        set value of text field 1 to v_price

                        -- 证券数量
                        set value of text field 3 to v_count

                        if button "确定卖出" exists then
                            click button "确定卖出"
                        end if

                        repeat until sheet 1 exists
                        end repeat

                        set v_result to {}
                        if isdo then
                            set v_result to v_result & "Y"
                            click button 1 of sheet 1

                            if sheet 1 exists then
                                set v_result to v_result & (get value of static text 2 of sheet 1)  
                                click button 1 of sheet 1
                            end if
                        else 
                            set v_result to v_result & "N"
                            click button 2 of sheet 1
                        end if

                        return v_result

    		        end tell
    		    end tell
            end tell
    	end sell_entrust

    	#--------------------------------------------------------------------------------------
        on cancel_entrust(para, isdo)
            tell application "System Events"
                tell process "同花顺至尊版"
                    tell window 1
                        set v_cancel_flag to item 1 of para
                        set thebutton to button 34
                        --get value of attribute "AXTitle" of thebutton
                        --display dialog value of thebutton
                        if v_cancel_flag = 0 then
                            -- 全撤 button 34
                            set thebutton to button 34
                        else if v_cancel_flag = 1 then
                            -- 撤买 button 35
                            set thebutton to button 35
                        else if v_cancel_flag = 2 then
                            -- 撤卖 button 36
                            set thebutton to button 36
                        else
                            -- 不合法
                        end if

                        click thebutton

                        set v_result to {}
                        if isdo then
                            set v_result to v_result & "Y"
                            if sheet 1 exists then
                                -- button 1 确认
                                click button 1 of sheet 1
                            end if
                        else
                            set v_result to v_result & "N"
                            if sheet 1 exists then
                                -- button 2 取消
                                click button 2 of sheet 1
                            end if
                        end if
                        return v_result
                    end tell
                end tell
            end tell
        end cancel_entrust

    ''')

    def __init__(self):
        import threading
        self.mutex = threading.Lock()

    def prepare(self,
        config_path=None,
        user=None,
        password=None,
        exe_path=None,
        comm_password=None,
        **kwargs):
        pass

    def exit(self):
        pass

    def buy(self, security, price, shares, isdo=True):
        '''
        参数格式: '002018', 1.34, 100
        '''
        if shares < 1 or shares > 1000:
            raise exceptions.TradeError('操作数量不在1~1000之间')

        start = time.time()
        print("###BUY### start -- buy_entrust: %s||%s||%s" % (security, price, shares))
        result = self.scpt.call('buy_entrust', [security, str(price), str(shares)], isdo)
        print("###BUY### %s" % (result))
        print("###BUY### end -- ", round(time.time() - start, 2), "seconds")
        return result

    def sell(self, security, price, shares, isdo=True):
        '''
        参数格式: '002018', 1.34, 100
        '''
        if shares < 1 or shares > 1000:
            raise exceptions.TradeError('操作数量不在1~1000之间')

        start = time.time()
        print("###SEL### start -- sell_entrust: %s||%s||%s" % (security, price, shares))
        result = self.scpt.call('sell_entrust', [security, str(price), str(shares)], isdo)
        print("###SEL### %s" % (result))
        print("###SEL### end -- ", round(time.time() - start, 2), "seconds")
        return result

    def cancel_entrusts(self):
        return self.cancel_entrust(para=[0])

    def cancel_entrust(self, para=[0], isdo=True):
        '''
        [0]: 全撤; [1]: 撤买; [2]: 撤卖
        '''
        cancel_flag = para[0]
        start = time.time()
        print("###CAN### start -- cancel_entrust: %s" % (cancel_flag))
        result = self.scpt.call('cancel_entrust', para, isdo)
        print("###CAN### %s" % (result))
        print("###CAN### end -- ", round(time.time() - start, 2), "seconds")
        return result

    @property
    def balance(self):
        with self.mutex:
            return self.query_assets()

    @property
    def position(self):
        with self.mutex:
            return self.query_position()

    def query_assets(self):
        """
        总资产:12472.58,总市值:0.00,总盈亏:0.00,当日盈亏:0.00,资金余额:12472.58,可取金额:12472.58,可用金额:12472.58
        [{
                "asset_balance": asset_balance,
                "current_balance": cash,
                "enable_balance": cash,
                "market_value": market,
                "money_type": u"人民币",
                "pre_interest": 0.25,}]
        :return:
        """
        start = time.time()
        print("###ASS### start -- query assets")
        result = self.scpt.call('query_assets')
        assets = Assets(result)
        x_balance = [
            {
                "asset_balance": assets.total_assets,
                "current_balance": assets.fetch_balance,
                "enable_balance": assets.enable_balance,
                "market_value": assets.total_market_value,
                "money_type": u"人民币",
                "pre_interest": 0.25,
            }
        ]
        print(x_balance)
        print("###ASS### end -- ", round(time.time() - start, 2), "seconds")
        return x_balance

    def query_position(self):
        """
        ['证券代码', '证券名称', '市价', '盈亏', '浮动盈亏比(%)', '实际数量', '股票余额', '可用余额', '冻结数量', '成本价', '市值', '交易市场', '股东账户']
        ['131990', '标准券', '100.000', '0.000', '0.000', '0', '0', '0', '0', '0.000', '0.000', '深圳Ａ股', '0200802943']
        ['159005', '添富快钱', '100.001', '0.000', '0.000', '100', '100', '100', '0', '100.001', '10000.100', '深圳Ａ股', '0200802943']]
        [{'cost_price': item['diluted_cost'],
                 'current_amount': item['shares'],
                 'enable_amount': item['shares'],
                 'income_balance': item['accum_amount'],
                 'keep_cost_price': item['hold_cost'],
                 'last_price': item['current'],
                 'market_value': item['market_value'],
                 'position_str': '',
                 'stock_code': item['symbol'].lower(),
                 'stock_name': item['name']}]
        :return:
        """
        start = time.time()
        print("###POS### start -- query position")
        result = self.scpt.call('query_position')
        position = Positon(result)
        x_position = []
        for item in position.security_list:
            x_position.append({
                'cost_price': float(item[9]),
                'current_amount': float(item[6]),
                'enable_amount': float(item[7]),
                'income_balance': float(item[3]),
                'keep_cost_price': float(item[9]),
                'last_price': float(item[2]),
                'market_value': float(item[10]),
                'position_str': '',
                'stock_code': str(item[0]),
                'stock_name': str(item[1])
            })
        print(x_position)
        print("###POS### end -- ", round(time.time() - start, 2), "seconds")
        return x_position

def test():
    ths_trader = ClientTrader()
    #ths_trader.buy('159001', 99.990, 100, isdo=True)
    # ths_trader.buy('511850', 99.999, 100, isdo=True)
    # ths_trader.buy('002505', 2.01, 100, isdo=True)
    # ths_trader.buy('000982', 1.63, 100, isdo=True)
    #ths_trader.sell('131810', 5.500, 100, isdo=True)
    # ths_trader.sell('511850', 99.999, 100, isdo=True)
    # ths_trader.sell('159001', 99.999, 100, isdo=True)
    #time.sleep(1)
    #ths_trader.cancel_entrust([0], isdo=True)
    ths_trader.query_assets()
    ths_trader.query_assets()
    ths_trader.query_position()
    ths_trader.query_position()



if __name__ == '__main__' :
    test()
