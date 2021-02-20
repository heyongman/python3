# 克隆自聚宽文章：https://www.joinquant.com/post/29225
# 标题：北上詹姆斯
# 作者：猪头港

# from .API import *
# 导入函数库
from jqdata import *
import random
import pandas as pd
import numpy as np
import datetime as dt


var = {
    'Context': {
        'subportfolios': [SubPortfolio],
        'portfolio': {
            'available_cash': '可用资金, 可用来购买证券的资金',
            'positions': {
                '000300.XSHG': {
                    'security': '标的代码',
                    'total_amount': '总仓位, 但不包括挂单冻结仓位( 如果要获取当前持仓的仓位,需要将locked_amount和total_amount相加)',
                    'locked_amount': '挂单冻结仓位',
                    'closeable_amount': '可卖出的仓位 / 场外基金持有份额'
                }
            },  # '等同于 long_positions',
            'positions_value': '持仓价值',
            'transferable_cash': '可取资金, 即可以提现的资金, 不包括今日卖出证券所得资金',
            'inout_cash': '累计出入金, 比如初始资金 1000, 后来转移出去 100, 则这个值是 1000 - 100',
            'locked_cash': '挂单锁住资金',
            'margin': '保证金，股票、基金保证金都为100%',
            'long_positions': '多单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象',
            'short_positions': '空单的仓位, 一个 dict, key 是证券代码, value 是 [Position]对象',
            'total_value': '总的权益, 包括现金, 保证金(期货)或者仓位(股票)的总价值, 可用来计算收益',
            'returns': '总权益的累计收益；（当前总资产 + 今日出入金 - 昨日总资产） / 昨日总资产；',
        },
        'current_dt': datetime.datetime,
        'previous_date': datetime.date-1,
        'universe': ['000001.XSHE', '600000.XSHG']
    }
}
# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # 输出内容到日志 log.info()
    log.info('初始函数开始运行且全局只运行一次')
    # 过滤掉order系列API产生的比error级别低的log
    log.set_level('order', 'error')

    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
                   type='stock')
    g.max_stock_count = 15
    g.back_trade_days = 40
    g.top_money_in = []
    g.window = 150
    g.stdev_n = 2
    g.mf, g.upper, g.lower = None, None, None
    run_daily(before_market_open, time='07:00')
    run_daily(reblance, '9:30')


def before_market_open(context):
    pre_date = (context.current_dt - datetime.timedelta(1)).strftime('%Y-%m-%d')
    g.mf, g.upper, g.lower = get_boll(pre_date)
    log.info('北上资金均值：%.2f  北上资金上界：%.2f 北上资金下界：%.2f' % (g.mf, g.upper, g.lower))


def get_boll(end_date):
    """
    获取北向资金布林带
    """
    table = finance.STK_ML_QUOTA
    q = query(
        table.day, table.quota_daily, table.quota_daily_balance
    ).filter(
        table.link_id.in_(['310001', '310002']), table.day <= end_date
    ).order_by(table.day)
    money_df = finance.run_query(q)
    money_df['net_amount'] = money_df['quota_daily'] - money_df['quota_daily_balance']
    # 分组求和
    money_df = money_df.groupby('day')[['net_amount']].sum().iloc[-g.window:]
    mid = money_df['net_amount'].mean()
    stdev = money_df['net_amount'].std()
    upper = mid + g.stdev_n * stdev
    lower = mid - g.stdev_n * stdev
    mf = money_df['net_amount'].iloc[-1]
    return mf, upper, lower


def calc_change(context):
    table = finance.STK_HK_HOLD_INFO
    q = query(table.day, table.name, table.code, table.share_ratio) \
        .filter(table.link_id.in_(['310001', '310002']),
                table.day.in_([context.previous_date]))
    df = finance.run_query(q)
    return df.sort_values(by='share_ratio', ascending=False)[:g.max_stock_count]['code'].values


def reblance(context):
    if g.mf >= g.upper:
        s_change_rank = calc_change(context)
        final = list(s_change_rank)
        current_hold_funds_set = set(context.portfolio.positions.keys())
        if set(final) != current_hold_funds_set:
            need_buy = set(final).difference(current_hold_funds_set)
            need_sell = current_hold_funds_set.difference(final)
            cash_per_fund = context.portfolio.total_value / g.max_stock_count * 0.99
            for fund in need_sell:
                order_target(fund, 0)
            for fund in need_buy:
                order_value(fund, cash_per_fund)

    elif g.mf <= g.lower:
        current_hold_funds_set = set(context.portfolio.positions.keys())
        if len(current_hold_funds_set) != 0:
            for fund in current_hold_funds_set:
                order_target(fund, 0)


