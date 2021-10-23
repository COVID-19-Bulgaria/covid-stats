'''
covid-stats: Main module

Copyright 2021, Veselin Stoyanov
Licensed under Attribution-NonCommercial-ShareAlike 4.0 International.
'''

from covidstats import data, plot, locales
import datetime as dt

from locales import t


def main():
    locales.setup_i18n()

    plot.setup_sns()

    date_cases_df = data.get_date_cases_df()
    week_cases_df = data.get_week_cases_df()
    date_diff_cases_df = data.get_date_diff_cases_df()
    active_cases_df = data.get_active_cases_df()
    week_places_cases_df = data.get_week_places_cases_df()
    date_positive_cases_percentage_df = data.get_date_positive_cases_percentage_df()

    generate_plots('bg', date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_cases_percentage_df)

    generate_plots('en', date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_cases_percentage_df)


def generate_plots(locale, date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_cases_percentage_df):
    locales.set_locale(locale)

    # Weekly infected and cured cases plot
    infected_cured_week_cases_plot = plot.generate_week_cases_plot(
        df=week_cases_df,
        value_vars=['infected', 'cured'],
        hue_order=['infected', 'cured'],
        palette=['orange', 'green'],
        legend=[t('plots.week_cases_plot.legend.infected'), t('plots.week_cases_plot.legend.cured')]
    )
    plot.export_plot(infected_cured_week_cases_plot, '%s/WeeklyInfectedCured' % locale)

    # Weekly hospitalized, intensive care and fatal cases plot
    hospitalized_intensive_fatal_week_cases_plot = plot.generate_week_cases_plot(
        df=week_cases_df,
        value_vars=['hospitalized', 'intensive_care', 'fatal'],
        hue_order=['hospitalized', 'intensive_care', 'fatal'],
        palette=['pink', 'purple', 'red'],
        legend=[
            t('plots.week_cases_plot.legend.hospitalized'),
            t('plots.week_cases_plot.legend.intensive_care'),
            t('plots.week_cases_plot.legend.fatal')
        ]
    )
    plot.export_plot(hospitalized_intensive_fatal_week_cases_plot, '%s/WeeklyHospitalizedIntensiveCareFatal' % locale)

    # Weekly places cases plot
    places_cases_week_plot = plot.generate_week_places_cases_plot(week_places_cases_df)
    plot.export_plot(places_cases_week_plot, '%s/WeeklyPlacesCases' % locale)

    # 14 days forecast
    start_date = dt.date.today() + dt.timedelta(days=1)
    weekly_14_days_forecast_plot = plot.generate_weekly_14_days_prediction_plot_for_date(start_date, week_cases_df,
                                                                                         date_diff_cases_df)
    plot.export_plot(weekly_14_days_forecast_plot, '%s/Weekly14DaysForecast' % locale)

    # Active cases plot
    active_cases_plot = plot.generate_active_cases_plot(active_cases_df)
    plot.export_plot(active_cases_plot, '%s/ActiveCases' % locale)

    # Daily positivity plot
    date_positive_cases_percentage_plot = plot.generate_date_positive_cases_percentage_plot(
        date_positive_cases_percentage_df)
    plot.export_plot(date_positive_cases_percentage_plot, '%s/PositiveCasesPercentage' % locale)

    # Historical cases plot
    historical_cases_plot = plot.generate_combined_date_cases_plot(date_cases_df)
    plot.export_plot(historical_cases_plot, '%s/HistoricalCases' % locale)
