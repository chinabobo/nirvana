from futu import *
from src import constants


def get_snapshot(ctx, code_list):
    try:
        # ctx = ft.OpenQuoteContext(host='127.0.0.1', port=11111)
        ret, data = ctx.get_market_snapshot(code_list)
        if ret == RET_OK:
            selected_columns = ['code', 'name', 'last_price', 'open_price']
            print(data[selected_columns])
        else:
            print(f"查询行情失败: {data}")
    except Exception as e:
        print(f"出现异常: {e}")
    finally:
        ctx.close()

if __name__ == '__main__':
    with (OpenQuoteContext(host='127.0.0.1', port=11111) as quote_ctx):
         get_snapshot(
             quote_ctx,[
                 constants.CODE_ALIBABA,
                 constants.CODE_TENCENT,
                 constants.CODE_YS,
                 constants.CODE_HDL,
                 constants.CODE_SZINT,
                 constants.CODE_CNRAIL,
                 constants.CODE_MT,
             ]
         )