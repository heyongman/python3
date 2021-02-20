from pyecharts import options as opts
from pyecharts.charts import Line
week_name_list = (["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
                  ["Mon", 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
price = [11.57, 14.34, 15.37, 12.29, 12.29, 15.60, 13.49]
sales = [114, 55, 27, 101, 101, 26, 105]

line= (
    Line()
    .add_xaxis(week_name_list[0])
    # 在顶部添加x轴
    # .extend_axis(xaxis_data=week_name_list[1],
    #             xaxis=opts.AxisOpts(type_="category", position='top',
    #             # axistick_opts=opts.AxisTickOpts(is_align_with_label=True),  # 设置标签位置
    #             axisline_opts=opts.AxisLineOpts(is_on_zero=False, linestyle_opts=opts.LineStyleOpts(color="#6e9ef1"))
    #                 ))
    # 在右侧添加y轴
    .extend_axis(yaxis=opts.AxisOpts(type_="value", position="right",))
    .add_yaxis("价格", price)
    # 设置右侧y轴
    .add_yaxis("销量", sales, yaxis_index=1)
    .add_yaxis("收益", [int(price[i]*sales[i]) for i in range(len(price))], yaxis_index=1)
    # .set_global_opts(title_opts=opts.TitleOpts(title="销量统计"),
    #                  设置图例， 多个y轴要分开设置
                     # legend_opts=[opts.LegendOpts(pos_left="right", pos_top='20%', orient='vertical', legend_icon='rent'),
                     #              opts.LegendOpts(pos_left="right", pos_top='50%', orient='vertical', legend_icon='circle')],
                    # 交叉指向工具
                    # tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    # 设置范围控制滑块
                     # datazoom_opts=opts.DataZoomOpts(orient='vertical', pos_top="5%", pos_left="93%", pos_bottom="60%",
                     #                                 range_start=0, range_end=200)
                     # )
)
line.render("professional_kline_chart.html")