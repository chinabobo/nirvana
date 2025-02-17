from futu import *
from src import constants

############################ 全局变量设置 ############################
FUTUOPEND_ADDRESS = '127.0.0.1'  # OpenD 监听地址
FUTUOPEND_PORT = 11111  # OpenD 监听端口

TRADING_ENVIRONMENT = TrdEnv.SIMULATE  # 交易环境：真实 / 模拟
TRADING_MARKET = TrdMarket.HK  # 交易市场权限，用于筛选对应交易市场权限的账户
TRADING_PWD = '123456'  # 交易密码，用于解锁交易
TRADING_PERIOD = KLType.K_DAY  # 信号 K 线周期
MOVING_AVERAGE_PERIOD = 5  # 均线周期：5日均线

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象
trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT, security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型

# 解锁交易
def unlock_trade():
    if TRADING_ENVIRONMENT == TrdEnv.REAL:
        ret, data = trade_context.unlock_trade(TRADING_PWD)
        if ret != RET_OK:
            print('unlock_trade failed：', data)
            return False
        print('unlock_trade done！')
    return True


# 获取市场状态
def is_normal_trading_time(code):
    ret, data = quote_context.get_market_state([code])
    if ret != RET_OK:
        print('get_market_state failed：', data)
        return False
    market_state = data['market_state'][0]
    if market_state in [MarketState.MORNING, MarketState.AFTERNOON, MarketState.FUTURE_DAY_OPEN,
                        MarketState.FUTURE_OPEN, MarketState.FUTURE_BREAK_OVER, MarketState.NIGHT_OPEN]:
        return True
    print('This is not a sustained trading session')
    return False


# 获取5日均线
def get_moving_average(code, period):
    ret, data = quote_context.get_cur_kline(code=code, num=period + 1)
    if ret != RET_OK:
        print('get_moving_average failed：', data)
        return None
    candlestick_list = data['close'].values.tolist()[::-1]  # 获取收盘价并反转
    if len(candlestick_list) < period:
        return None
    return sum(candlestick_list[1: period + 1]) / period

def get_moving_average_include_cur(code, period, cur):
    ret, data = quote_context.get_cur_kline(code=code, num=period)
    if ret != RET_OK:
        print('get_moving_average_include_cur failed：', data)
        return None
    candlestick_list = data['close'].values.tolist()[::-1]  # 获取收盘价并反转
    if len(candlestick_list) < period:
        return None
    return sum(candlestick_list[1: period], cur) / period

# 获取当前现价
def get_current_price(code):
    ret, data = quote_context.get_market_snapshot([code])
    if ret != RET_OK:
        print('get_current_price failed：', data)
        return None
    return data['last_price'][0]

# 获取昨天的收盘价
def get_yesterday_close_price(stock_code):
    today = datetime.today()
    yesterday = today - timedelta(1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    ret_code, data = quote_context.request_history_kline(
        stock_code, start=yesterday_str, end=yesterday_str
    )
    if ret_code != 0:
        print(f"Error: {data}")
        return None

    if len(data) > 0:
        close_price = data[-1]['close']
        return close_price
    else:
        print(f"No data for {stock_code} on {yesterday_str}")
        return None


# 获取持仓数量
def get_holding_position(code):
    holding_position = 0
    ret, data = trade_context.position_list_query(code=code, trd_env=TRADING_ENVIRONMENT)
    if ret != RET_OK:
        print('get_holding_position failed：', data)
        return None
    else:
        for qty in data['qty'].values.tolist():
            holding_position += qty
        print('【position status】 {} open position：{}'.format(constants.CODE_TENCENT, holding_position))
    return holding_position


# 下单函数
def open_position(code):
    current_price = get_current_price(code)
    if current_price is None:
        print("get_current_price failed")
        return

    # 计算下单量
    # open_quantity = calculate_quantity()
    open_quantity = 1

    # 判断购买力是否足够
    if is_valid_quantity(code, open_quantity, current_price):
        # 下单
        ret, data = trade_context.place_order(
            price=current_price, qty=open_quantity, code=code,
            trd_side=TrdSide.BUY, order_type=OrderType.NORMAL,
            trd_env=TRADING_ENVIRONMENT, remark='moving_average_strategy')
        if ret != RET_OK:
            print('place_order failed：', data)
    else:
        print('exceeds the maximum available quantity')


# 计算下单数量
def calculate_quantity():
    price_quantity = 0
    ret, data = quote_context.get_market_snapshot([constants.CODE_TENCENT])
    if ret != RET_OK:
        print('get_market_snapshot failed：', data)
        return price_quantity
    price_quantity = data['lot_size'][0]
    return price_quantity


# 判断购买力是否足够
def is_valid_quantity(code, quantity, price):
    ret, data = trade_context.acctradinginfo_query(
        order_type=OrderType.NORMAL, code=code, price=price,
        trd_env=TRADING_ENVIRONMENT)
    if ret != RET_OK:
        print('acctradinginfo_query failed：', data)
        return False
    max_can_buy = data['max_cash_buy'][0]
    max_can_sell = data['max_sell_short'][0]
    if quantity > 0:
        return quantity < max_can_buy
    elif quantity < 0:
        return abs(quantity) < max_can_sell
    else:
        return False


# 策略启动时运行一次，用于初始化策略
def on_init():
    if not unlock_trade():
        return False
    print('************ strategy start ************')
    return True


# 每根 K 线产生时运行一次（每天收盘前1分钟）
def on_bar_open(code):
    print('*************************************')

    # 只在常规交易时段交易
    if not is_normal_trading_time(code):
        return

    # 获取5日均线
    # moving_average_5 = get_moving_average(code, MOVING_AVERAGE_PERIOD)
    #
    # if moving_average_5 is None:
    #     print('无法获取5日均线数据。')
    #     return

    # 获取当前现价
    current_price = get_current_price(code)
    if current_price is None:
        print('get_current_price failed')
        return

    moving_average_5_include_cur = get_moving_average_include_cur(code, MOVING_AVERAGE_PERIOD, current_price)
    if moving_average_5_include_cur is None:
        print('moving_average_5_include_cur failed')
        return

    yesterday_close_price = get_yesterday_close_price(code)

    print(f"current_price: {current_price}, yesterday_close_price: {yesterday_close_price}, moving_average_5_include_cur: {moving_average_5_include_cur}, ")

    # 判断如果现价大于5日均线，则买入
    if yesterday_close_price < moving_average_5_include_cur < current_price:
        print('buy!')
        open_position(code)
    else:
        print('not buy!')


# 主函数
if __name__ == '__main__':
    if not on_init():
        print('init failed, script exit!')
        quote_context.close()
        trade_context.close()
    else:
        quote_context.subscribe(code_list=[constants.CODE_TENCENT], subtype_list=[TRADING_PERIOD])

        while True:
            on_bar_open(constants.CODE_TENCENT)
            time.sleep(60)
