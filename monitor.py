from futu import *
import constants

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# TRADING_PERIOD = KLType.K_1M  # 信号 K 线周期
# FAST_MOVING_AVERAGE = 1  # 均线快线的周期
# SLOW_MOVING_AVERAGE = 3  # 均线慢线的周期

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_pb):
        """
        处理接收到的股票报价回调数据
        """
        ret_code, data = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logging.error(f"StockQuoteTest: error, msg: {data}")
            return RET_ERROR, data

        # 输出接收到的数据
        logging.info(f"StockQuoteTest received data: {data}")
        return RET_OK, data

def subscribe_quotes(ctx, code_list):
    """
    订阅股票报价
    """
    try:
        ctx.subscribe(code_list, constants.SUBSCRIBE_TYPES)
        logging.info("Successfully subscribed to stock quotes.")
    except Exception as e:
        logging.error(f"Error during subscription: {e}")
        return False
    return True

def handle_subscription(ctx, code_list):
    """
    处理订阅的股票报价，并在指定时间内接收数据
    """
    handler = StockQuoteTest()
    ctx.set_handler(handler)

    # 订阅股票报价
    if subscribe_quotes(ctx, code_list):
        # 等待15秒来接收数据
        time.sleep(15)

    # 关闭连接
    ctx.close()
    logging.info("Connection closed.")

def manage_subscription_periodically(ctx):
    """
    根据港股交易时间周期性管理订阅，启动和停止订阅
    """
    is_subscribing = False

    while True:
        # 获取当前时间
        time_obj = time.localtime()
        hour = time_obj.tm_hour
        mins = time_obj.tm_min
        wday = time_obj.tm_wday

        # 判断是否是港股交易时间段
        if wday < 5:  # 只考虑工作日（周一至周五）
            # 开市前竞价时段：09:30 - 10:00
            if (hour == 9 and mins >= 30) or (hour == 10 and mins <= 0):
                if not is_subscribing:
                    ctx.start()  # 开始订阅
                    is_subscribing = True
                    logging.info("Started subscribing during pre-market.")

            # 早市：09:30 - 12:00
            elif (hour == 9 and mins > 30) or (hour >= 10 and hour < 12):
                if not is_subscribing:
                    ctx.start()  # 开始订阅
                    is_subscribing = True
                    logging.info("Started subscribing during morning session.")

            # 午市：13:00 - 16:00
            elif (hour == 13 and mins >= 0) or (hour > 13 and hour < 16):
                if not is_subscribing:
                    ctx.start()  # 开始订阅
                    is_subscribing = True
                    logging.info("Started subscribing during afternoon session.")

            # 收市时段：16:00 - 16:10
            elif hour == 16 and mins <= 10:
                if not is_subscribing:
                    ctx.start()  # 开始订阅
                    is_subscribing = True
                    logging.info("Started subscribing during closing auction.")

            # 如果不在任何交易时段内，停止订阅
            else:
                if is_subscribing:
                    ctx.stop()  # 停止订阅
                    is_subscribing = False
                    logging.info("Stopped subscribing outside trading hours.")

        # 打印当前状态
        logging.info(f"Running state: {'Subscribed' if is_subscribing else 'Not subscribed'} - {time.ctime()}")
        time.sleep(600)  # 每隔10分钟检查一次

if __name__ == '__main__':
    try:
        # 创建连接上下文
        with OpenQuoteContext(host='127.0.0.1', port=11111) as quote_ctx:
            # 测试订阅15秒内的数据
            handle_subscription(
                quote_ctx,
                [constants.CODE_TENCENT,
                 constants.CODE_SH_000001,
                 constants.CODE_SZ_399001]
            )

            # 周期性管理订阅
            manage_subscription_periodically(quote_ctx)
    except Exception as e:
        logging.error(f"Error: {e}")
