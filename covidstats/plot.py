import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np
import datetime as dt
import random

from covidstats import data, helpers
from covidstats.locales import t


def setup_sns():
    custom_styles = {
        'xtick.bottom': True,
        'ytick.left': True,
        'axes.titlepad': 20,
        'axes.edgecolor': '.15'
    }

    color_palette = sns.color_palette('husl', 27)

    sns.set(rc={'figure.figsize': (12, 8)})
    sns.set_theme(style='whitegrid', palette=color_palette, color_codes=True, rc=custom_styles)


def set_plot_subtitle(ax, text):
    ax.annotate(text, xy=(0.5, 1.015), xytext=(0.5, 1.015), xycoords='axes fraction', annotation_clip=False,
                ha='center', fontsize='small')


def generate_week_cases_plot(
        df=data.get_week_cases_df(),
        value_vars=['infected', 'cured', 'fatal'],
        hue_order=['infected', 'cured', 'fatal'],
        palette=['orange', 'green', 'red'],
        legend=[
            t('plots.week_cases_plot.legend.infected'),
            t('plots.week_cases_plot.legend.cured'),
            t('plots.week_cases_plot.legend.fatal')]
):
    plot_df = pd.melt(df, id_vars=['date'], value_vars=value_vars).dropna()

    week_cases_plot = sns.lineplot(x='date', y='value', hue='variable', hue_order=hue_order, palette=palette,
                                   data=plot_df)
    week_cases_plot.set_title(t('plots.week_cases_plot.title'), fontweight='bold')
    set_plot_subtitle(week_cases_plot, helpers.get_generation_date_text())
    week_cases_plot.set_xlabel(t('plots.week_cases_plot.x_label'))
    week_cases_plot.set_ylabel(t('plots.week_cases_plot.y_label'))
    week_cases_plot.legend(labels=legend)
    plt.gcf().autofmt_xdate(rotation=45)

    week_cases_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m (%V)'))

    week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
    week_cases_plot.xaxis.set_minor_locator(week_locator)

    ticks = np.arange(plot_df['date'].min(), plot_df['date'].max(), np.timedelta64(28, 'D'), dtype='datetime64')
    week_cases_plot.set_xticks(ticks)

    return week_cases_plot


def generate_active_cases_plot(df=data.get_active_cases_df()):
    active_cases_plot = sns.lineplot(data=df, x=df.index, y='active', color='orange', legend=False)
    active_cases_plot.set_title(t('plots.active_cases_plot.title'), fontweight='bold')
    set_plot_subtitle(active_cases_plot, helpers.get_generation_date_text())
    active_cases_plot.set_xlabel(t('plots.active_cases_plot.x_label'))
    active_cases_plot.set_ylabel(t('plots.active_cases_plot.y_label'))
    active_cases_plot.fill_between(df.index, df['active'], alpha=0.2, color='orange')
    plt.gcf().autofmt_xdate(rotation=45)

    active_cases_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m (%V)'))

    week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
    active_cases_plot.xaxis.set_minor_locator(week_locator)

    ticks = np.arange(df.index.min(), df.index.max(), np.timedelta64(28, 'D'), dtype='datetime64')
    active_cases_plot.set_xticks(ticks)

    return active_cases_plot


def generate_week_places_cases_plot(df=data.get_week_places_cases_df()):
    draw_order = df.sort_values('date').groupby('place').tail(1).sort_values('infected_avg', ascending=True).place
    legend_order = draw_order.iloc[::-1]

    draw_colors_order = list(sns.color_palette('husl', draw_order.size))
    random.shuffle(draw_colors_order)

    legend_colors_order = draw_colors_order[::-1]

    week_places_cases_plot = sns.lineplot(data=df, x='date', y='infected_avg', hue='place', hue_order=draw_order,
                                          palette=draw_colors_order)
    week_places_cases_plot.set_title(t('plots.week_places_cases_plot.title'), fontweight='bold')
    set_plot_subtitle(week_places_cases_plot, helpers.get_generation_date_text())
    week_places_cases_plot.set_xlabel(t('plots.week_places_cases_plot.x_label'))
    week_places_cases_plot.set_ylabel(t('plots.week_places_cases_plot.y_label'))
    plt.gcf().autofmt_xdate(rotation=45)

    week_places_cases_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m (%V)'))

    week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
    week_places_cases_plot.xaxis.set_minor_locator(week_locator)

    ticks = np.arange(df['date'].min(), df['date'].max(), np.timedelta64(28, 'D'), dtype='datetime64')
    week_places_cases_plot.set_xticks(ticks)

    handles = list(map(lambda color: Line2D([0], [0], color=color), legend_colors_order))
    labels = list(legend_order)

    week_places_cases_plot.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5))

    return week_places_cases_plot


def generate_14_days_prediction_plot(
        cases_df,
        predicted_cases_df,
        rt_df,
        predicted_rt_df):
    cases_plot = sns.lineplot(data=cases_df,
                              x=cases_df.date.append(predicted_cases_df.index.to_series(), ignore_index=True),
                              y='infected', color='orange', label=t('plots.14_days_forecast_plot.legend.cases'))
    predicted_cases_r_increase_plot = sns.lineplot(data=predicted_cases_df, x=predicted_cases_df.index,
                                                   y='increase_cases', color='red',
                                                   label=t('plots.14_days_forecast_plot.legend.cases_r_increase'))
    predicted_cases_r_retention_plot = sns.lineplot(data=predicted_cases_df, x=predicted_cases_df.index,
                                                    y='predicted_cases', color='purple',
                                                    label=t('plots.14_days_forecast_plot.legend.cases_r_retention'))
    predicted_cases_r_decline_plot = sns.lineplot(data=predicted_cases_df, x=predicted_cases_df.index,
                                                  y='decline_cases', color='olive',
                                                  label=t('plots.14_days_forecast_plot.legend.cases_r_decline'))

    cases_plot.fill_between(predicted_cases_df.index,
                            predicted_cases_df['increase_cases'],
                            predicted_cases_df['predicted_cases'],
                            color='red', alpha=0.2)

    cases_plot.fill_between(predicted_cases_df.index,
                            predicted_cases_df['predicted_cases'],
                            predicted_cases_df['decline_cases'],
                            color='olive', alpha=0.2)

    cases_plot.set_title(t('plots.14_days_forecast_plot.title'), fontweight='bold')
    set_plot_subtitle(cases_plot, helpers.get_generation_date_text())
    cases_plot.set_xlabel(t('plots.14_days_forecast_plot.x_label'))
    cases_plot.set_ylabel(t('plots.14_days_forecast_plot.y_label'))
    plt.gcf().autofmt_xdate(rotation=45)

    cases_plot.yaxis.set_major_locator(ticker.MaxNLocator(4))

    lines, labels = cases_plot.get_legend_handles_labels()
    cases_plot.get_legend().remove()

    with sns.axes_style({'axes.grid': False}):
        common_ax = cases_plot.twinx()
        rt_plot = sns.lineplot(data=rt_df, x=rt_df.index, y='Q0.5', ax=common_ax, color='lightblue',
                               label=t('plots.14_days_forecast_plot.legend.rt'))
        rt_plot.set_ylabel(t('plots.14_days_forecast_plot.y_right_label'), rotation=-90, labelpad=20)
        rt_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m (%V)'))

        rt_plot.fill_between(rt_df.index,
                             rt_df['Q0.05'],
                             rt_df['Q0.95'],
                             color='lightblue', alpha=0.2)

        rt_plot.set_yticks(range(4))

        rt_plot.axhline(1, ls='--', color='green')
        rt_plot.set_ylim(0, 3)

        rt_prediction_retention_plot = sns.lineplot(data=predicted_rt_df, x=predicted_rt_df.index, y='predicted_rt',
                                                    ax=common_ax, color='darkblue',
                                                    label=t('plots.14_days_forecast_plot.legend.rt_forecast'))
        rt_prediction_retention_plot.fill_between(predicted_rt_df.index,
                                                  predicted_rt_df['decline_rt'],
                                                  predicted_rt_df['increase_rt'],
                                                  color='darkblue', alpha=0.2)

        lines2, labels2 = common_ax.get_legend_handles_labels()
        plt.legend(lines + lines2, labels + labels2, loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2,
                   frameon=False)

    return cases_plot


def generate_weekly_14_days_prediction_plot_for_date(start_date, week_cases_df=data.get_week_cases_df(),
                                                     date_diff_cases_df=data.get_date_diff_cases_df()):
    rt_df = helpers.estimate_rt(date_diff_cases_df['infected'])

    previous_day = pd.to_datetime(start_date - dt.timedelta(days=1))
    start_datetime = pd.to_datetime(start_date)

    predicted_rts = helpers.predict_rt(rt_df, rt_df.index.get_loc(previous_day), 14)
    predicted_rts_df = data.build_rts_df(predicted_rts, start_datetime)
    predicted_cases_df = data.build_predicted_cases_df(rt_df[rt_df.index < start_datetime]['cases'], predicted_rts_df,
                                                       start_datetime)
    weekly_predicted_cases_df = data.build_weekly_predicted_cases_df(week_cases_df, predicted_cases_df, start_datetime)

    return generate_14_days_prediction_plot(week_cases_df, weekly_predicted_cases_df, rt_df, predicted_rts_df)


def generate_date_positive_cases_percentage_plot(df=data.get_date_positive_tests_df()):
    df['formatted_date'] = list(map(lambda date: date.strftime('%d.%m (%V)'), df['date']))
    date_positive_cases_percentage_plot = sns.barplot(data=df, x='formatted_date', y='positive_percentage', lw=0.,
                                                      color='#4e73df', ci=None)
    date_positive_cases_percentage_plot.set_title(t('plots.positive_cases_percentage_plot.title'), fontweight='bold')
    set_plot_subtitle(date_positive_cases_percentage_plot, helpers.get_generation_date_text())
    date_positive_cases_percentage_plot.set_xlabel(t('plots.positive_cases_percentage_plot.x_label'))
    date_positive_cases_percentage_plot.set_ylabel(t('plots.positive_cases_percentage_plot.y_label'))
    plt.gcf().autofmt_xdate(rotation=45)

    minor_week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
    date_positive_cases_percentage_plot.xaxis.set_minor_locator(minor_week_locator)

    major_week_locator = mdates.WeekdayLocator(byweekday=mdates.SU, interval=4)
    date_positive_cases_percentage_plot.xaxis.set_major_locator(major_week_locator)

    return date_positive_cases_percentage_plot


def generate_tests_positivity_plot(
        df=data.get_date_positive_tests_df(),
        value_vars=['pcr_tests', 'positive_pcr_tests'],
        hue_order=['pcr_tests', 'positive_pcr_tests'],
        main_palette=['orange', 'red'],
        main_legend=[
            t('plots.tests_positivity_plot.legend.pcr_tests'),
            t('plots.tests_positivity_plot.legend.positive_pcr_tests')
        ],
        secondary_var='pcr_positive_percentage',
        secondary_legend=t('plots.tests_positivity_plot.legend.positive_tests_percentage'),
        title=t('plots.tests_positivity_plot.title.pcr')
):
    plot_df = pd.melt(df, id_vars=['date'], value_vars=value_vars).dropna()

    date_tests_plot = sns.lineplot(x='date', y='value', hue='variable', hue_order=hue_order, palette=main_palette,
                                   data=plot_df)
    date_tests_plot.set_title(title, fontweight='bold')
    date_tests_plot.set_xlabel(t('plots.tests_positivity_plot.x_label'))
    date_tests_plot.set_ylabel(t('plots.tests_positivity_plot.y_label'))
    date_tests_plot.legend(labels=main_legend)
    plt.gcf().autofmt_xdate(rotation=45)

    set_plot_subtitle(date_tests_plot, helpers.get_generation_date_text())

    lines, labels = date_tests_plot.get_legend_handles_labels()
    date_tests_plot.get_legend().remove()

    with sns.axes_style({'axes.grid': False}):
        common_ax = date_tests_plot.twinx()

        positivity_plot = sns.lineplot(data=df, x=df.index, y=secondary_var, ax=common_ax, color='blue',
                                       linestyle='dotted',
                                       label=secondary_legend)
        positivity_plot.set_ylabel(t('plots.tests_positivity_plot.y_right_label'), rotation=-90, labelpad=20)

        positivity_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))

        week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
        positivity_plot.xaxis.set_minor_locator(week_locator)

        ticks = np.arange(df['date'].min(), df['date'].max(), np.timedelta64(28, 'D'), dtype='datetime64')
        positivity_plot.set_xticks(ticks)

        lines2, labels2 = common_ax.get_legend_handles_labels()
        positivity_plot.legend(lines + lines2, main_legend + [secondary_legend])

    return date_tests_plot


def generate_date_cases_plot(
        df=data.get_date_cases_df(),
        value_vars=['infected', 'cured', 'fatal'],
        hue_order=['infected', 'cured', 'fatal'],
        palette=['orange', 'green', 'red'],
        legend=[
            t('plots.date_cases_plot.legend.infected'),
            t('plots.date_cases_plot.legend.cured'),
            t('plots.date_cases_plot.legend.fatal')
        ]
):
    df['date'] = df.index
    plot_df = pd.melt(df, id_vars=['date'], value_vars=value_vars).dropna()

    date_cases_plot = sns.lineplot(x='date', y='value', hue='variable', hue_order=hue_order, palette=palette,
                                   data=plot_df)
    date_cases_plot.set_title(t('plots.date_cases_plot.title'), fontweight='bold')
    set_plot_subtitle(date_cases_plot, helpers.get_generation_date_text())
    date_cases_plot.set_xlabel(t('plots.date_cases_plot.x_label'))
    date_cases_plot.set_ylabel(t('plots.date_cases_plot.y_label'))
    date_cases_plot.legend(labels=legend)
    plt.gcf().autofmt_xdate(rotation=45)

    date_cases_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))

    week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
    date_cases_plot.xaxis.set_minor_locator(week_locator)

    ticks = np.arange(plot_df['date'].min(), plot_df['date'].max(), np.timedelta64(28, 'D'), dtype='datetime64')
    date_cases_plot.set_xticks(ticks)

    return date_cases_plot


def generate_combined_date_cases_plot(df=data.get_date_cases_df()):
    date_cases_plot = generate_date_cases_plot(df=df, value_vars=['infected', 'cured'], hue_order=['infected', 'cured'],
                                               palette=['orange', 'green'],
                                               legend=[
                                                 t('plots.date_cases_plot.legend.infected'),
                                                 t('plots.date_cases_plot.legend.cured'),
                                               ])

    lines, labels = date_cases_plot.get_legend_handles_labels()
    date_cases_plot.get_legend().remove()

    with sns.axes_style({'axes.grid': False}):
        common_ax = date_cases_plot.twinx()

        fatal_plot = sns.lineplot(data=df, x=df.index, y='fatal', ax=common_ax, color='red',
                                  label=t('plots.date_cases_plot.legend.fatal'))
        fatal_plot.set_ylabel(t('plots.date_cases_plot.y_fatal_label'), rotation=-90, labelpad=20)

        fatal_plot.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))

        week_locator = mdates.WeekdayLocator(byweekday=mdates.SU)
        fatal_plot.xaxis.set_minor_locator(week_locator)

        ticks = np.arange(df['date'].min(), df['date'].max(), np.timedelta64(28, 'D'), dtype='datetime64')
        fatal_plot.set_xticks(ticks)

        lines2, labels2 = common_ax.get_legend_handles_labels()
        fatal_plot.legend(lines + lines2, [
            t('plots.date_cases_plot.legend.infected'),
            t('plots.date_cases_plot.legend.cured'),
            t('plots.date_cases_plot.legend.fatal')
        ])

    return date_cases_plot


def export_plot(ax, file_name):
    ax.figure.tight_layout()
    ax.figure.savefig(file_name + '.svg', dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)
    ax.figure.clf()
