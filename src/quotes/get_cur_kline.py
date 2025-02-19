from src import constants
from futu import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FUTUOPEND_ADDRESS = '127.0.0.1'  # OpenD 监听地址
FUTUOPEND_PORT = 11111  # OpenD 监听端口

quote_ctx = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象

# def get_current_price(code):
#     ret, data = quote_context.get_market_snapshot([code])
#     if ret != RET_OK:
#         print(f'get_current_price failed: {data}')
#         return None
#     return data['last_price'][0]
#
# def get_moving_average(code, period, include_current_price=False):
#     ret, data = quote_context.get_cur_kline(code=code, num=period + 1 if not include_current_price else period)
#     if ret != RET_OK:
#         logging.info(f'get_moving_average failed: {data}')
#         return None
#     candlestick_list = data['close'].values.tolist()[::-1]  # 获取收盘价并反转
#     if len(candlestick_list) < period:
#         return None
#     if include_current_price:
#         # 包含当前价格
#         candlestick_list.insert(0, get_current_price(code))  # 插入当前价格
#     return sum(candlestick_list[:period]) / period

if __name__ == '__main__':
    ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_DAY], subscribe_push=False)
    # 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_cur_kline('HK.00700', 2, KLType.K_DAY, AuType.QFQ)  # 获取港股00700最近2个 K 线数据
        if ret == RET_OK:
            print(data)
            print(data['turnover_rate'][0])  # 取第一条的换手率
            print(data['turnover_rate'].values.tolist())  # 转为 list
        else:
            print('error:', data)
    else:
        print('subscription failed', err_message)
    quote_ctx.close()  # 关闭当条连接，OpenD 会在1分钟后自动取消相应股票相应类型的订阅
