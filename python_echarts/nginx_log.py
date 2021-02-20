import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
import pandas as pd


def line():
    from pyecharts import options as opts
    from pyecharts.charts import Line, Bar
    from pyecharts.faker import Faker

    x = Faker.choose()
    scatter1 = (
        Line()
            .add_xaxis(x)
            .extend_axis(yaxis=opts.AxisOpts(type_="value", name="商家B", position="right",))
            .add_yaxis("商家A", Faker.values(), yaxis_index=0)
            .add_yaxis("商家AA", Faker.values(), yaxis_index=0)
            .add_yaxis("商家B", [v / 1000 for v in Faker.values()], yaxis_index=1)
            .add_yaxis("商家BB", [v / 100 for v in Faker.values()], yaxis_index=1)
            .set_global_opts(yaxis_opts=opts.AxisOpts(type_="value", name="商家A", position="left"))
    )
    scatter2 = (
        Line()
            .add_xaxis(x)
            .add_yaxis("商家B", [v / 1000 for v in Faker.values()], yaxis_index=1)
            # .extend_axis(yaxis=opts.AxisOpts(type_="value", name="商家B", position="left"))
            # .set_global_opts(yaxis_opts=opts.AxisOpts(type_="value", name="商家B", position="left"))
    )
    scatter1.render('line_smooth.html')
    # scatter1.overlap(scatter2).render('line_smooth.html')


def multi_xaxis():
    data = pd.Series([1, 2, 3, 4, 5])
    c1 = (
        Line()
        .add_xaxis(data.tolist())
        .extend_axis(yaxis_opts=opts.AxisOpts())
        .add_yaxis("A", data.tolist(), yaxis_index=0)
        # .add_yaxis("B", (data*100).tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-smooth"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            tooltip_opts=opts.TooltipOpts(trigger='axis'),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
        )
        # .render("line_smooth.html")
    )

    c2 = (
        Line()
        .add_xaxis(data.tolist())
        # .add_yaxis("A", data.tolist())
        .extend_axis(yaxis_opts=opts.AxisOpts())
        .add_yaxis("B", (data * 100).tolist(), yaxis_index=1)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Line-smooth"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            tooltip_opts=opts.TooltipOpts(trigger='axis'),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
        )
            # .render("line_smooth.html")
    )

    c2.overlap(c1).render('line_smooth.html')


if __name__ == '__main__':
    line()
