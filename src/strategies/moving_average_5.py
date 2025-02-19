import concurrent.futures

from futu import *

from src import constants

FUTUOPEND_ADDRESS = '127.0.0.1'  # OpenD 监听地址
FUTUOPEND_PORT = 11111  # OpenD 监听端口

TRADING_ENVIRONMENT = TrdEnv.SIMULATE  # 交易环境：真实 / 模拟
TRADING_MARKET = TrdMarket.HK  # 交易市场权限，用于筛选对应交易市场权限的账户
TRADING_PWD = '123456'  # 交易密码，用于解锁交易
TRADING_PERIOD = KLType.K_DAY  # 信号 K 线周期
MOVING_AVERAGE_PERIOD = 5  # 均线周期：5日均线

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象
trade_context = OpenSecTradeContext(filter_trdmarket=TRADING_MARKET, host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT, security_firm=SecurityFirm.FUTUSECURITIES)  # 交易对象，根据交易品种修改交易对象类型

log_file_path = 'strategy_log.log'  # 日志文件路径
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler(log_file_path, mode='a')  # 输出到日志文件，追加模式
    ]
)



# 解锁交易
def unlock_trade():
    if TRADING_ENVIRONMENT == TrdEnv.REAL:
        ret, data = trade_context.unlock_trade(TRADING_PWD)
        if ret != RET_OK:
            logging.info(f'unlock_trade failed: {data}')
            return False
        logging.info('unlock_trade done！')
    return True

# 获取市场状态
def is_normal_trading_time(code):
    ret, data = quote_context.get_market_state([code])
    if ret != RET_OK:
        logging.info(f'get_market_state failed: {data}')
        return False
    market_state = data['market_state'][0]
    valid_states = [
        MarketState.MORNING, MarketState.AFTERNOON, MarketState.FUTURE_DAY_OPEN,
        MarketState.FUTURE_OPEN, MarketState.FUTURE_BREAK_OVER, MarketState.NIGHT_OPEN
    ]
    if market_state in valid_states:
        return True
    logging.info(f'This is not a sustained trading session for {code}')
    return False

# 获取5日均线
def get_moving_average(code, period, include_current_price=False):
    ret, data = quote_context.get_cur_kline(code=code, num=period + 1 if not include_current_price else period)
    if ret != RET_OK:
        logging.info(f'get_moving_average failed: {data}')
        return None
    candlestick_list = data['close'].values.tolist()[::-1]  # 获取收盘价并反转
    if len(candlestick_list) < period:
        return None
    if include_current_price:
        # 包含当前价格
        candlestick_list.insert(0, get_current_price(code))  # 插入当前价格
    return sum(candlestick_list[:period]) / period

# 获取当前现价
def get_current_price(code):
    ret, data = quote_context.get_market_snapshot([code])
    if ret != RET_OK:
        print(f'get_current_price failed: {data}')
        return None
    return data['last_price'][0]

# 获取昨天的收盘价
def get_yesterday_close_price(stock_code):
    yesterday = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
    ret_code, data = quote_context.request_history_kline(stock_code, start=yesterday, end=yesterday)
    if ret_code != 0:
        print(f"Error: {data}")
        return None
    if data:
        return data[-1]['close']
    print(f"No data for {stock_code} on {yesterday}")
    return None

# 获取持仓数量
def get_holding_position(code):
    ret, data = trade_context.position_list_query(code=code, trd_env=TRADING_ENVIRONMENT)
    if ret != RET_OK:
        print(f'get_holding_position failed: {data}')
        return None
    return sum(data['qty'].values.tolist())

# 卖出所有持仓
def sell_all_positions(code):
    holding_position = get_holding_position(code)
    if holding_position > 0:
        ret, data = trade_context.place_order(
            price=get_current_price(code), qty=holding_position, code=code,
            trd_side=TrdSide.SELL, order_type=OrderType.NORMAL,
            trd_env=TRADING_ENVIRONMENT, remark='moving_average_strategy_sell_all')
        if ret != RET_OK:
            print(f'sell_all_positions failed: {data}')
        else:
            print(f'Successfully sold {holding_position} positions of {code}')
    else:
        print(f'No holding positions to sell for {code}')

def open_position(code, quantity=1):
    current_price = get_current_price(code)
    if current_price is None:
        print("get_current_price failed")
        return
    if is_valid_quantity(code, quantity, current_price):
        ret, data = trade_context.place_order(
            price=current_price, qty=quantity, code=code,
            trd_side=TrdSide.BUY, order_type=OrderType.NORMAL,
            trd_env=TRADING_ENVIRONMENT, remark='moving_average_strategy')
        if ret != RET_OK:
            print(f'place_order failed: {data}')
    else:
        print('Insufficient purchasing power')

# 判断购买力是否足够
def is_valid_quantity(code, quantity, price):
    ret, data = trade_context.acctradinginfo_query(
        order_type=OrderType.NORMAL, code=code, price=price,
        trd_env=TRADING_ENVIRONMENT)
    if ret != RET_OK:
        print(f'acctradinginfo_query failed: {data}')
        return False
    max_can_buy = data['max_cash_buy'][0]
    max_can_sell = data['max_sell_short'][0]
    return (quantity > 0 and quantity <= max_can_buy) or (quantity < 0 and abs(quantity) <= max_can_sell)

# 判断当前是否为收盘前1分钟
def is_near_market_close():
    now = datetime.now()
    market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)  # 假设是收盘时间16:00
    return (market_close_time - now).seconds <= 60

# 策略启动时运行一次，用于初始化策略
def on_init():
    if not unlock_trade():
        return False
    print('************ strategy start ************')
    return True

# 策略执行：每根 K 线产生时运行一次（每天收盘前1分钟）
def on_bar_open(code):
    print(f'************************************* {code}')

    # 获取5日均线
    current_price = get_current_price(code)
    if current_price is None:
        print(f'get_current_price failed for {code}')
        return

    moving_average_5_include_cur = get_moving_average(code, MOVING_AVERAGE_PERIOD, include_current_price=True)
    if moving_average_5_include_cur is None:
        print(f'moving_average_5_include_cur failed for {code}')
        return

    yesterday_close_price = get_yesterday_close_price(code)

    print(f"current_price: {current_price}, yesterday_close_price: {yesterday_close_price}, moving_average_5_include_cur: {moving_average_5_include_cur}")

    # 判断如果现价大于5日均线，则买入
    if yesterday_close_price < moving_average_5_include_cur < current_price:
        print(f'buy! {code}')
        open_position(code)
    # 判断如果现价小于5日均线，则卖出所有持仓
    elif yesterday_close_price > moving_average_5_include_cur > current_price:
        print(f'sell all! {code}')
        sell_all_positions(code)
    else:
        print(f'not buy or sell! {code}')

if __name__ == '__main__':
    if not on_init():
        print('init failed, script exit!')
        quote_context.close()
        trade_context.close()
    else:
        # 设置多个股票进行监控
        stocks_to_monitor = [
            constants.CODE_ALIBABA,
            constants.CODE_TENCENT,
            constants.CODE_YS,
            constants.CODE_HDL,
            constants.CODE_SZINT,
            constants.CODE_CNRAIL,
            constants.CODE_MT,
        ]

        quote_context.subscribe(code_list=stocks_to_monitor, subtype_list=[TRADING_PERIOD])

        last_run_time = None  # 用于记录上次执行时间

        # 使用线程池并行处理多个股票
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(stocks_to_monitor)) as executor:
            while True:
                now = datetime.now()

                if not is_near_market_close() or any(
                        not is_normal_trading_time(stock) for stock in stocks_to_monitor):
                    logging.info(f'Skipping strategy execution for all stocks')
                    time.sleep(60)
                    continue

                # 确保每天只运行一次
                if last_run_time is None or now.date() > last_run_time.date():
                    # 使用线程池并行执行每个股票的策略
                    futures = [executor.submit(on_bar_open, stock) for stock in stocks_to_monitor]
                    for future in concurrent.futures.as_completed(futures):
                        future.result()  # 获取每个线程的执行结果
                    last_run_time = now  # 更新上次执行
