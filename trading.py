from futu import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CODE_TENCENT = 'HK.00700'  # 交易标的
CODE_BABA = 'HK.09988'  # 交易标的
CODE_SH_000001 = 'SH.000001'
CODE_SZ_399001 = 'SZ.399001'

def trading(ctx, price, qty, code, trd_side):
    res, msg = ctx.place_order(
        price=price, qty=qty, code=code, trd_side=trd_side, trd_env=TrdEnv.SIMULATE)
    if res == RET_OK:
        print(msg)
        print(msg['order_id'][0])  # 获取下单的订单号
        print(msg['order_id'].values.tolist())  # 转为 list
    else:
        print('place_order error: ', msg)

def get_history(ctx):
    ret, data = ctx.history_order_list_query()
    if ret == RET_OK:
        print(data)
        if data.shape[0] > 0:  # 如果订单列表不为空
            print(data['order_id'][0])  # 获取持仓第一个订单号
            print(data['order_id'].values.tolist())  # 转为 list
    else:
        print('history_order_list_query error: ', data)

def order_list(ctx):
    ret, data = ctx.order_list_query()
    if ret == RET_OK:
        print(data)
        if data.shape[0] > 0:  # 如果订单列表不为空
            print(data['order_id'][0])  # 获取未完成订单的第一个订单号
            print(data['order_id'].values.tolist())  # 转为 list
    else:
        print('order_list_query error: ', data)



if __name__ == '__main__':
    with OpenSecTradeContext(
            filter_trdmarket=TrdMarket.HK, host='127.0.0.1',
            port=11111, security_firm=SecurityFirm.FUTUSECURITIES
    ) as trd_ctx:
        # trading(ctx=trd_ctx, price=500.0, qty=100, code="HK.00700", trd_side=TrdSide.SELL)
        # get_history(trd_ctx)
        order_list(trd_ctx)