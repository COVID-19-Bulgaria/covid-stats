'''
covid-stats: Main module

Copyright 2021, Veselin Stoyanov
Licensed under Attribution-NonCommercial-ShareAlike 4.0 International.
'''

from covidstats import data, plot, locales
import datetime as dt

from covidstats.locales import t


def main():
    locales.setup_i18n()

    plot.setup_sns()

    date_cases_df = data.get_date_cases_df()
    week_cases_df = data.get_week_cases_df()
    date_diff_cases_df = data.get_date_diff_cases_df()
    active_cases_df = data.get_active_cases_df()
    week_places_cases_df = data.get_week_places_cases_df()
    date_positive_tests_df = data.get_date_positive_tests_df()
    weekly_positive_tests_df = data.build_weekly_positive_tests_df(date_positive_tests_df)
    rolling_biweekly_places_cases_df = data.get_rolling_biweekly_places_cases_df()
    date_cases_age_df = data.get_date_cases_age_df()
    date_diff_cases_age_df = data.build_date_diff_cases_age_df(date_cases_age_df)

    generate_plots('bg', date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_tests_df, weekly_positive_tests_df, rolling_biweekly_places_cases_df,
                   date_cases_age_df, date_diff_cases_age_df)

    generate_plots('en', date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_tests_df, weekly_positive_tests_df, rolling_biweekly_places_cases_df,
                   date_cases_age_df, date_diff_cases_age_df)


def generate_plots(locale, date_cases_df, week_cases_df, date_diff_cases_df, active_cases_df, week_places_cases_df,
                   date_positive_cases_percentage_df, weekly_positive_tests_df, rolling_biweekly_places_cases_df,
                   date_cases_age_df, date_diff_cases_age_df):
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

    # Historical cases plot
    historical_cases_plot = plot.generate_combined_date_cases_plot(date_cases_df)
    plot.export_plot(historical_cases_plot, '%s/HistoricalCases' % locale)

    # Daily positivity plot
    date_tests_positivity_plot = plot.generate_date_positive_cases_percentage_plot(
        date_positive_cases_percentage_df)
    plot.export_plot(date_tests_positivity_plot, '%s/DateTestsPositivity' % locale)

    # Weekly positivity plot
    weekly_tests_positivity_plot = plot.generate_tests_positivity_plot(
        df=weekly_positive_tests_df,
        value_vars=['total_tests', 'total_positive_tests'],
        hue_order=['total_tests', 'total_positive_tests'],
        main_palette=['orange', 'red'],
        main_legend=[
            t('plots.tests_positivity_plot.legend.tests'),
            t('plots.tests_positivity_plot.legend.positive_tests')
        ],
        secondary_var='positive_percentage',
        secondary_legend=t('plots.tests_positivity_plot.legend.positive_tests_percentage'),
        title=t('plots.tests_positivity_plot.title.pcr_antigen')
    )
    plot.export_plot(weekly_tests_positivity_plot, '%s/WeeklyTestsPositivity' % locale)

    # Weekly PCR positivity plot
    weekly_pcr_tests_positivity_plot = plot.generate_tests_positivity_plot(
        df=weekly_positive_tests_df,
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
    )
    plot.export_plot(weekly_pcr_tests_positivity_plot, '%s/WeeklyPCRTestsPositivity' % locale)

    # Weekly antigen positivity plot
    weekly_antigen_tests_positivity_plot = plot.generate_tests_positivity_plot(
        df=weekly_positive_tests_df[weekly_positive_tests_df.antigen_positive_percentage.notnull()],
        value_vars=['antigen_tests', 'positive_antigen_tests'],
        hue_order=['antigen_tests', 'positive_antigen_tests'],
        main_palette=['orange', 'red'],
        main_legend=[
            t('plots.tests_positivity_plot.legend.antigen_tests'),
            t('plots.tests_positivity_plot.legend.positive_antigen_tests')
        ],
        secondary_var='antigen_positive_percentage',
        secondary_legend=t('plots.tests_positivity_plot.legend.positive_tests_percentage'),
        title=t('plots.tests_positivity_plot.title.antigen')
    )
    plot.export_plot(weekly_antigen_tests_positivity_plot, '%s/WeeklyAntigenTestsPositivity' % locale)

    # Rolling biweekly places cases plot
    rolling_biweekly_places_cases_plot = plot.generate_rolling_biweekly_places_cases_facet_plot(
        rolling_biweekly_places_cases_df
    )
    plot.export_plot(rolling_biweekly_places_cases_plot, '%s/RollingBiWeeklyPlacesCases' % locale)

    # Date cases age plot
    date_cases_age_plot = plot.generate_cases_age_plot(date_cases_age_df)
    plot.export_plot(date_cases_age_plot, '%s/DateCasesAge' % locale)

    # Week cases age plot
    date_week_cases_age_plot = plot.generate_week_cases_age_plot(date_diff_cases_age_df)
    plot.export_plot(date_week_cases_age_plot, '%s/WeekCasesAge' % locale)