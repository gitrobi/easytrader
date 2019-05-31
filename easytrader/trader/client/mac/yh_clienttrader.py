import applescript
import time

from easytrader.trader.trader import BaseTrader

scpt = applescript.AppleScript('''
	#--------------------------------------------------------------------------------------
	on foo()
		return "你好"
	end foo
	
	#--------------------------------------------------------------------------------------
	on toPage(itemid)
		my _toPage(44) -- to 预留信息修改页面，起到刷新页面的效果
		my _toPage(itemid)
	end toPage

	#--------------------------------------------------------------------------------------
	on _toPage(itemid)
		tell application "System Events"
			tell process "银河玖乐Mac版"
				set frontmost to false
				tell window "银河玖乐Mac版 V1.0.3"
					--  构造菜单项列表
					set menulist to {}
					try
						set menulist to row of outline 1 of scroll area 1 of group 1
					on error
						set menulist to row of outline 1 of scroll area 1 of group 3
					end try

					--选中某个菜单项
					set selecteditem to get the item itemid of menulist
					set value of attribute "AXSelected" of the selecteditem to true
				end tell
			end tell
		end tell
	end _toPage

	#--------------------------------------------------------------------------------------
	on login()
		tell application "System Events"
			tell process "银河玖乐Mac版"
				--set frontmost to true
				tell window "银河玖乐Mac版 V1.0.3"
					set value of text field 2 to "981626"
					set value of text field 1 to "2614"
					click checkbox "登  录"  
					set _str to 1
					return _str
				end tell
			end tell
		end tell
	end login

	#--------------------------------------------------------------------------------------
	on buy_entrust(para, isdo)
		set v_stock_code to item 1 of para
		set v_price to item 2 of para
		set v_count to item 3 of para
	
		set v_result to {}

		tell application "System Events"
			tell process "银河玖乐Mac版"
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 买入委托
					my toPage(1)

					-- 检查标志
					set value of text field 3 to ""

					-- 证券代码
					set value of attribute "AXFocused" of text field 1 to true
					set value of text field 1 to v_stock_code
					action "AXConfirm" of text field 1

					-- 等待刷新股票名称
					repeat until the length of (get value of text field 3) > 0
					end repeat

					-- 证券价格
					set value of text field 3 to v_price

					-- 证券数量
					set value of text field 2 to v_count

					-- 对于逆回购，按钮显示为"融资委托"，其他产品，显示为"买入委托"
					if button "买入委托" exists
						click button "买入委托"
					else if button "融资委托" exists
						click button "融资委托"
					end if
				end tell

				-- 等待弹出窗口"委托确认提示"
				repeat until window "委托确认提示" exists
				end repeat
				
				set v_result to v_result & (get name of static text 1 of window "委托确认提示")
				if isdo then
					set v_result to v_result & "Y"
					tell button "买入" of window "委托确认提示" to click
				else
					set v_result to v_result & "N"
					tell button "取消" of window "委托确认提示" to click
					return v_result
				end if

				-- 等待确认结果窗口返回
				--repeat until window 1 exists
				--end repeat
				repeat until button "确认" of window 1  exists
				end repeat

				set v_result to v_result & (get name of static text of window 1)
				tell button "确认" of window 1 to click

				return v_result
			end tell
		end tell
	end buy_entrust

	#--------------------------------------------------------------------------------------
	on sell_entrust(para, isdo)
		set v_stock_code to item 1 of para
		set v_price to item 2 of para
		set v_count to item 3 of para
	
		set v_result to {}

		tell application "System Events"
			tell process "银河玖乐Mac版"
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 卖出委托
					my toPage(2)

					-- 检查标志
					set value of text field 3 to ""

					-- 证券代码
					set value of attribute "AXFocused" of text field 1 to true
					set value of text field 1 to v_stock_code 
					action "AXConfirm" of text field 1
					
					-- 等待刷新股票名称
					repeat until the length of (get value of text field 3) > 0
					end repeat

					-- 证券价格
					set value of text field 3 to v_price

					-- 证券数量
					set value of text field 2 to v_count

					-- 对于逆回购，按钮显示为"融券委托"，其他产品，显示为"卖出委托"
					if button "卖出委托" exists
						click button "卖出委托"
					else if button "融券委托" exists
						click button "融券委托"
					end if
				end tell

				-- 等待弹出窗口"委托确认提示"
				repeat until window "委托确认提示" exists
				end repeat

				set v_result to v_result & (get name of static text 1 of window "委托确认提示")
				if isdo then
					set v_result to v_result & "Y"
					tell button "卖出" of window "委托确认提示" to click
				else
					set v_result to v_result & "N"
					tell button "取消" of window "委托确认提示" to click
					return v_result
				end if


				-- 等待确认结果窗口返回
				--repeat until window 1 exists
				--end repeat
				repeat until button "确认" of window 1  exists
				end repeat

				set v_result to v_result & (get name of static text of window 1)
				tell button "确认" of window 1 to click

				return v_result
			end tell
		end tell
	end sell_entrust

	#--------------------------------------------------------------------------------------
	on cancel_entrust(para, isdo)
		set v_result to {}
		set v_count to 0

		tell application "System Events"
			tell process "银河玖乐Mac版"
				
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 委托撤单
					my toPage(3)

					-- 等待委托数据加载
					--repeat until row of table of scroll area 1 exists -- fix no row data
					--end repeat
					delay 0.1

					-- 如果有委托数据，则执行撤单
					if get the (count of row of table of scroll area 1) > 0 then
						if value of attribute "AXValue" of checkbox "全选" = 0 then
							set v_count to get the (count of row of table of scroll area 1) as integer
							click checkbox "全选"
						end if
					else
						set v_result to v_result & "NO entrust data to cancel" & "N"
						return v_result
					end if

					-- 全部撤单
					ignoring application responses --忽略应用的反馈
						click button "撤 单"
					end ignoring
				end tell
			end tell
		end tell

		-- 杀掉 System Events 应用
		delay 0.1 --自定义 UI 反馈的等待时间为0.1 秒
		do shell script "killall System\\\ Events"   -- outside in applescript editor using two \\

		tell application "System Events"
			tell process "银河玖乐Mac版"
				-- afer do
				if v_count > 1 then
					-- 等待弹出窗口"委托确认提示"
					repeat until window "委托确认提示" exists
					end repeat
					
					set v_result to v_result & (get value of static text 1 of window "委托确认提示")
					if isdo then
						set v_result to v_result & "Y"
						tell button "撤单" of window "委托确认提示" to click
					else
						set v_result to v_result & "N"
						tell button "取消" of window "委托确认提示" to click
						return v_result
					end if
				else if v_count = 1 then
					-- 等待弹出窗口"委托撤单确认"
					repeat until window "委托撤单确认" exists
					end repeat

					set v_result to v_result & (get value of static text 1 of window "委托撤单确认")
					if isdo then
						set v_result to v_result & "Y"
						tell button "撤单" of window "委托撤单确认" to click
					else
						set v_result to v_result & "N"
						tell button "取消" of window "委托撤单确认" to click
						return v_result
					end if
				end if

				-- 等待确认结果窗口返回
				--repeat until window 1 exists
				--end repeat
				repeat until button "确认" of window 1 exists
				end repeat

				set v_result to v_result & (get name of static text of window 1)
				tell button "确认" of window 1 to click

				return v_result
			end tell
		end tell
	end cancel_entrust

	#--------------------------------------------------------------------------------------
	on queryAssets()
		tell application "System Events"
			tell process "银河玖乐Mac版"
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 资产查询
					my toPage(4)

					-- to do
					delay 0.3

					-- 资金信息
					set a0 to name of buttons of group 1 of table 1 of scroll area 1
					set a1 to value of UI elements of row of table 1 of scroll area 1
					
					-- 持仓信息
					set a2 to name of buttons of group 1 of table 1 of scroll area 2
					set a3 to value of UI elements of row of table 1 of scroll area 2
			
					set result to {a0, a1, a2, a3}
					return result

				end tell
			end tell
		end tell
	end queryAssets

	#--------------------------------------------------------------------------------------
	on queryTransaction()
		tell application "System Events"
			tell process "银河玖乐Mac版"
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 成交查询
					my toPage(5)

					-- to do
					delay 0.2

					-- 成交信息
					set a0 to name of buttons of group 1 of table 1 of scroll area 1
					set a1 to value of UI elements of row of table 1 of scroll area 1
			
					set result to {a0, a1}
					return result
				end tell
			end tell
		end tell
	end queryTrasaction

	#--------------------------------------------------------------------------------------
	on queryEntrust()
		tell application "System Events"
			tell process "银河玖乐Mac版"
				tell window "银河玖乐Mac版 V1.0.3"
					-- 选中 委托查询
					my toPage(6)

					-- to do
					return 1
				end tell
			end tell
		end tell	
	end queryEntrust
''')


# --------------------------------------------------------------------------------------
class Account :
	# ['资金帐号', '银行名称', '币种', '资金余额', '可用资金', '参考市值', '总资产']
	def __init__(self, lname):
		self.acctId_desc = lname[0]
		self.bankName_desc = lname[1]
		self.currency_desc = lname[2]
		self.balance_desc = lname[3]
		self.available_desc = lname[4]
		self.marketValue_desc = lname[5]
		self.totalAssets_desc = lname[6]

	def initData(self, ldata) :
		if len(ldata) > 0 :
			self.acctId = ldata[0]
			self.bankName = ldata[1]
			self.currency = ldata[2]
			self.balance = ldata[3]
			self.available = ldata[4]
			self.marketValue = ldata[5]
			self.totalAssets = ldata[6]

	def __str__(self) :
		ss = "{}:{},{}:{},{}:{}".format(self.totalAssets_desc, self.totalAssets,
										self.available_desc, self.available, self.balance_desc, self.balance)
		return ss


# --------------------------------------------------------------------------------------
class CapitalInfo :
	def __init__(self, lacc) :
		self.lacc = lacc

	def __str__(self) :
		_str = "\n资金信息\n"
		for acc in self.lacc :
			_str = _str + str(acc) + '\n'
		return _str

# --------------------------------------------------------------------------------------
class Security:
	# '证券名称', '证券代码', '当前持仓', '参考盈亏', '股份余额', '股份可用', '参考市值', '参考市价', '参考成本价', '盈亏比例(%)', '买入冻结', '卖出冻结', '股东代码', '交易市场'
	def __init__(self, lname):
		self.secName_desc = lname[0]
		self.secCode_desc = lname[1]
		self.currentCount_desc = lname[2]
		self.balanceCount_desc = lname[4]
		self.availableCount_desc = lname[5]
		self.marketValue_desc = lname[6]
		self.holderCode_desc = lname[12]
		self.market_desc = lname[13]

	def initData(self, ldata) :
		if len(ldata) > 0 :
			self.secName = ldata[0]
			self.secCode = ldata[1]
			self.currentCount = ldata[2]
			self.balanceCount = ldata[4]
			self.availableCount = ldata[5]
			self.marketValue = ldata[6]
			self.holderCode = ldata[12]
			self.market = ldata[13]

	def __str__(self) :
		ss = "{}:{},{}:{},{}:{},{}:{},{}:{}".format(self.secCode_desc, self.secCode,self.secName_desc, self.secName,
													self.currentCount_desc, self.currentCount, self.availableCount_desc,
													self.availableCount, self.marketValue_desc, self.marketValue)
		return ss

# --------------------------------------------------------------------------------------
class PositionInfo :
	def __init__(self, lsec) :
		self.lsec = lsec

	def __str__(self) :
		_str = "\n持仓信息\n"
		for sec in self.lsec :
			_str = _str + str(sec) + '\n'
		return _str

# --------------------------------------------------------------------------------------
#['证券名称', '证券代码', '成交日期', '成交时间', '成交价格', '成交数量', '成交金额', '买卖标志', '委托序号', '股东代码', '交易市场']
class Transaction :
	def __init__(self, lname):
		self.secName_desc = lname[0]
		self.secCode_desc = lname[1]
		self.tradeDate_desc = lname[2]
		self.tradeTime_desc = lname[3]
		self.tradePrice_desc = lname[4]
		self.tradeCount_desc = lname[5]
		self.tradeAmount_desc = lname[6]
		self.tradeOp_desc = lname[7]
		self.holderCode_desc = lname[9]
		self.market_desc = lname[10]

	def initData(self, ldata) :
		if len(ldata) > 0 :
			self.secName = ldata[0]
			self.secCode = ldata[1]
			self.tradeDate = ldata[2]
			self.tradeTime = ldata[3]
			self.tradePrice = ldata[4]
			self.tradeCount = ldata[5]
			self.tradeAmount = str(ldata[6])
			self.tradeOp = ldata[7]
			self.holderCode = ldata[9]
			self.market = ldata[10]

	def __str__(self) :
		ss = "{}:{},{}:{},{}:{},{}:{},{}:{},{}:{},{}:{}".format(self.secCode_desc, self.secCode,self.secName_desc, self.secName,
																self.tradePrice_desc, self.tradePrice, self.tradeCount_desc, self.tradeCount,
																self.tradeAmount_desc, self.tradeAmount, self.tradeAmount_desc, self.tradeAmount,
																self.tradeOp_desc, self.tradeOp)
		return ss

# --------------------------------------------------------------------------------------
class TransactionInfo :
	def __init__(self, ltra) :
		self.ltra = ltra

	def __str__(self) :
		_str = "\n成交信息\n"
		for tra in self.ltra :
			_str = _str + str(tra) + '\n'
		return _str



# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
class YHClientTrader(BaseTrader):
	#
	# YHClientTrader - main class to transaction in a real-time way by YH client
	#
	# ----------------------------------------------------------------------------------
	def __init__(self):
		pass

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

	# ----------------------------------------------------------------------------------
	def login(self):
		result = scpt.call('login')
		return result

	# ----------------------------------------------------------------------------------
	def buy(self, security, price, shares, isdo=False):
		start = time.time()
		print("###BUY### start -- %s:%s:%s" % (security, price, shares))
		result = scpt.call('buy_entrust', [security, str(price), str(shares)], isdo)
		print("###BUY### %s" % (self.formatResult(result)))
		print("###BUY### end -- ", round(time.time() - start, 2), "seconds")
		return result

	# ----------------------------------------------------------------------------------
	def sell(self, security, price, shares, isdo=False):
		start = time.time()
		print("###SEL### start -- %s:%s:%s" % (security, price, shares))
		result = scpt.call('sell_entrust', [security, str(price), str(shares)], isdo)
		print("###SEL### %s" % (self.formatResult(result)))
		print("###SEL### end -- ", round(time.time() - start, 2), "seconds")
		return result

	def cancel_entrusts(self):
		return self.cancel_entrust(para=None)

	# ----------------------------------------------------------------------------------
	def cancel_entrust(self, para=None, isdo=False):
		start = time.time()
		print("###CAN### start -- cancel all entrust")
		result = scpt.call('cancel_entrust', para, isdo)
		print("###CAN### %s" % (self.formatResult(result)))
		print("###CAN### end -- ", round(time.time() - start, 2), "seconds")
		return result

	# ----------------------------------------------------------------------------------
	@property
	def balance(self):
		start = time.time()
		print("###ASS### start -- query assets")
		result = scpt.call('queryAssets')

		lcap = []
		capName = result[0]
		for x, capData in enumerate(result[1]):
			capData = result[1][x]
			acc = Account(capName)
			acc.initData(capData)
			lcap.append(acc)
		capInfo = CapitalInfo(lcap)

		lpos = []
		posName = result[2]
		for x, posData in enumerate(result[3]):
			posData = result[3][x]
			sec = Security(posName)
			sec.initData(posData)
			lpos.append(sec)
		posInfo = PositionInfo(lpos)

		print("###ASS### %s%s" % (capInfo, posInfo))
		print("###ASS### end -- ", round(time.time() - start, 2), "seconds")
		return result

	@property
	def position(self):
		return self.balance()

	# ----------------------------------------------------------------------------------
	def transaction(self):
		start = time.time()
		print("###TRA### start -- query transcation")
		result = scpt.call('queryTransaction')

		ltra = []
		traName = result[0]
		for x, traData in enumerate(result[1]):
			traData = result[1][x]
			tra = Transaction(traName)
			tra.initData(traData)
			if tra.tradeAmount != '.00' :
				ltra.append(tra)
		traInfo = TransactionInfo(ltra)

		print("###TRA### %s" % traInfo)
		print("###TRA### end -- ", round(time.time() - start, 2), "seconds")
		return result

	# ----------------------------------------------------------------------------------
	def entrust(self):
		start = time.time()
		print("###ENT### start -- query entrust")
		result = scpt.call('queryEntrust')
		print("###ENT### %s" % result)
		print("###ENT### end -- ", round(time.time() - start, 2), "seconds")
		return result

	# ----------------------------------------------------------------------------------
	def formatResult(self, result):
		# ['买入委托\n0560507210\n159901\n深100ETF\n限价委托\n3.005\n100', 'Y', '错误', '-150906130[-150906130]资金可用数不足,尚需300.60', AEType(b'msng')]
		# ['买入委托\n0560507210\n159901\n深100ETF\n限价委托\n3.005\n100', 'N']
		# ['\n确定要撤销选中的所有委托？', 'Y', '温馨提示', '批量撤单\n成功数量:0\n失败数量:3', AEType(b'msng')]
		if len(result) == 2:
			con = result[0].replace('\n', '|')
			re = "{}".format(result[1])
		elif len(result) == 5:
			con = result[0].replace('\n', '|')
			re = "{} {}:{}".format(result[1], result[2], result[3].replace('\n', '|'))
		else:
			return result
		return "[条件]{} [结果]{}".format(con, re)



# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# BELOW CODE FOR TEST PURPOSE

# demo data
# - test buy list
buylist = [['204001','5.500','100'],
			['131810','5.500','100'],
			['511850','95.000','100'],
			['159901','3.005','100'],
			['600993','11.88','100'],
			['300005','2.99','100']]

# - test sell list
selllist = [['204001','5.500','100'],
			['131810','5.500','100'],
			['159901','3.500','100'],
			['511660','100.02','1'],
			['511850','100.03','100']]

# Test with buy and sell lit
def testbuyNsellist() :
	# 构造YHClientTrader的实例
	trader = YHClientTrader()

	for item in buylist :
		trader.buy(item, isdo=True)

	for item in selllist :
		trader.sell(item, isdo=True)


# General TEST
def test():
	# 构造YHClientTrader的实例
	trader = YHClientTrader()
	# GC-001:204001 R-001:131810 财富宝E:511850 深100ETF:159901
	#trader.buy(['159901', '3.005', '100'], isdo=True) # 深100ETF
	trader.buy(['131810', '5.500', '100'], isdo=False) # R-001
	#trader.buy(['511810', '95', '100'], isdo=True)
	#trader.sell(['159901', '3.340', '300'], isdo=True)
	#trader.sell(['131810', '5.500', '50'], isdo=True)
	#trader.sell(['511990', '105', '100'], isdo=True)
	#trader.cancel(isdo=True)
	#trader.queryAssets()
	# trader.queryTransaction()
	#trader.queryEntrust()
	#trader.formatResult("")


# Regression TEST
def testall() :
	n = 0
	while n < 1:
		test()
		#testbuyNsellist()
		n += 1


# --------------------------------------------------------------------------------------

if __name__ == '__main__' :
	#testall()
	test()







