'''
covid-stats: Main module

Copyright 2021, Veselin Stoyanov
Licensed under Attribution-NonCommercial-ShareAlike 4.0 International.
'''

from covidstats import data, plot, locales
import datetime as dt
import argparse

from covidstats.locales import t


def main():
    startup_arguments = get_startup_arguments()

    locales.setup_i18n()
    plot.setup_sns()

    if startup_arguments.external:
        build_external()
        return

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


def get_startup_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--external', action='store_true', default=False, dest='external',
                        help='Generate plots with external data.')

    return parser.parse_args()


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

    # Historical hospitalized and intensive care
    historical_hospitalized_intensive_care_cases_plot = plot.generate_date_cases_plot(
        df=date_cases_df, value_vars=['hospitalized', 'intensive_care'], hue_order=['hospitalized', 'intensive_care'],
        palette=['pink', 'purple'],
        legend=[
            t('plots.date_cases_plot.legend.hospitalized'),
            t('plots.date_cases_plot.legend.intensive_care'),
        ]
    )
    plot.export_plot(historical_hospitalized_intensive_care_cases_plot,
                     '%s/HistoricalHospitalizedIntensiveCareCases' % locale)

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
    plot.export_plot(rolling_biweekly_places_cases_plot, ('%s/RollingBiWeeklyPlacesCases' % locale), False)

    # Date cases age plot
    date_cases_age_plot = plot.generate_cases_age_plot(date_cases_age_df)
    plot.export_plot(date_cases_age_plot, '%s/DateCasesAge' % locale)

    # Week cases age plot
    date_week_cases_age_plot = plot.generate_week_cases_age_plot(date_diff_cases_age_df)
    plot.export_plot(date_week_cases_age_plot, '%s/WeekCasesAge' % locale)

    # Vaccination timeline by day
    date_vaccination_timeline_plot = plot.generate_vaccination_timeline_plot(df=date_cases_df,
                                                                             diff_df=date_diff_cases_df,
                                                                             plot_type='daily')
    plot.export_plot(date_vaccination_timeline_plot, '%s/DateVaccinationTimeline' % locale)

    # Vaccination timeline by week
    weekly_vaccination_timeline_plot = plot.generate_vaccination_timeline_plot(df=date_cases_df,
                                                                               diff_df=week_cases_df,
                                                                               plot_type='weekly')
    plot.export_plot(weekly_vaccination_timeline_plot, '%s/WeeklyVaccinationTimeline' % locale)


def build_external():
    infected_by_age_group_df = data.get_infected_by_age_group_df()
    fatal_by_age_group_df = data.get_fatal_by_age_group_df()
    infected_vaccinated_df = data.get_infected_vaccinated_df()
    hospitalized_vaccinated_df = data.get_hospitalized_vaccinated_df()
    intensive_care_vaccinated_df = data.get_intensive_care_vaccinated_df()
    fatal_vaccinated_df = data.get_fatal_vaccinated_df()

    total_infected_by_age_group_df = data.build_total_infected_by_age_group_df(infected_by_age_group_df)
    total_fatal_by_age_group_df = data.build_grouped_by_age_df(fatal_by_age_group_df, filter_column='age')
    grouped_by_age_fatal_percentage_df = data.build_grouped_by_age_fatal_percentage_df(
        data.aggregate_0_19_age_group(infected_by_age_group_df),
        data.aggregate_0_19_age_group(fatal_by_age_group_df)
    )
    infected_vaccinated_by_age_df = data.build_grouped_by_age_df(infected_vaccinated_df, filter_column='vaccine')
    hospitalized_vaccinated_by_age_df = data.build_grouped_by_age_df(hospitalized_vaccinated_df,
                                                                     filter_column='vaccine')
    intensive_care_vaccinated_by_age_df = data.build_grouped_by_age_df(intensive_care_vaccinated_df,
                                                                       filter_column='vaccine')
    fatal_vaccinated_by_age_df = data.build_grouped_by_age_df(fatal_vaccinated_df, filter_column='vaccine')
    vaccinated_by_age_fatal_percentage_df = data.build_grouped_by_age_fatal_percentage_df(
        infected_vaccinated_by_age_df, fatal_vaccinated_by_age_df)

    date_diff_cases_df = data.get_date_diff_cases_df()
    date_vaccinated_fatal_df = data.build_date_vaccinated_fatal_df(fatal_vaccinated_df)
    vaccinated_fatal_percentage_df = data.build_vaccinated_fatal_percentage_df(date_vaccinated_fatal_df,
                                                                               date_diff_cases_df)

    generate_external_plots('bg', total_infected_by_age_group_df, total_fatal_by_age_group_df,
                            grouped_by_age_fatal_percentage_df, infected_vaccinated_by_age_df,
                            hospitalized_vaccinated_by_age_df, intensive_care_vaccinated_by_age_df,
                            fatal_vaccinated_by_age_df, vaccinated_by_age_fatal_percentage_df,
                            vaccinated_fatal_percentage_df)

    generate_external_plots('en', total_infected_by_age_group_df, total_fatal_by_age_group_df,
                            grouped_by_age_fatal_percentage_df, infected_vaccinated_by_age_df,
                            hospitalized_vaccinated_by_age_df, intensive_care_vaccinated_by_age_df,
                            fatal_vaccinated_by_age_df, vaccinated_by_age_fatal_percentage_df,
                            vaccinated_fatal_percentage_df)


def generate_external_plots(locale, total_infected_by_age_group_df, total_fatal_by_age_group_df,
                            grouped_by_age_fatal_percentage_df, infected_vaccinated_by_age_df,
                            hospitalized_vaccinated_by_age_df, intensive_care_vaccinated_by_age_df,
                            fatal_vaccinated_by_age_df, vaccinated_by_age_fatal_percentage_df,
                            vaccinated_fatal_percentage_df):
    locales.set_locale(locale)

    # Infected by age group
    total_infected_by_age_group_plot = plot.generate_grouped_by_age_bar_plot(
        total_infected_by_age_group_df,
        y='infected',
        color='orange',
        plot_type='total.infected'
    )
    plot.export_plot(total_infected_by_age_group_plot, '%s/InfectedByAgeGroup' % locale)

    # Fatal by age group
    total_fatal_by_age_group_plot = plot.generate_grouped_by_age_bar_plot(
        total_fatal_by_age_group_df,
        y='fatal',
        color='red',
        plot_type='total.fatal'
    )
    plot.export_plot(total_fatal_by_age_group_plot, '%s/FatalByAgeGroup' % locale)

    # Fatal percentage by age group
    grouped_by_age_group_fatal_percentage_plot = plot.generate_grouped_by_age_bar_plot(
        grouped_by_age_fatal_percentage_df,
        y='fatal_percentage',
        color='red',
        plot_type='total.fatal_percentage'
    )
    plot.export_plot(grouped_by_age_group_fatal_percentage_plot, '%s/FatalPercentageByAgeGroup' % locale)

    # Vaccinated Infected By Age
    infected_vaccinated_by_age_plot = plot.generate_grouped_by_age_bar_plot(
        infected_vaccinated_by_age_df,
        y='infected',
        color='orange',
        plot_type='vaccinated.infected')
    plot.export_plot(infected_vaccinated_by_age_plot, '%s/VaccinatedByAgeInfected' % locale)

    # Vaccinated Hospitalized By Age
    hospitalized_vaccinated_by_age_plot = plot.generate_grouped_by_age_bar_plot(
        hospitalized_vaccinated_by_age_df,
        y='hospitalized',
        color='pink',
        plot_type='vaccinated.hospitalized')
    plot.export_plot(hospitalized_vaccinated_by_age_plot, '%s/VaccinatedByAgeHospitalized' % locale)

    # Vaccinated Intensive Care By Age
    intensive_care_vaccinated_by_age_plot = plot.generate_grouped_by_age_bar_plot(
        intensive_care_vaccinated_by_age_df,
        y='intensive_care',
        color='purple',
        plot_type='vaccinated.intensive_care')
    plot.export_plot(intensive_care_vaccinated_by_age_plot, '%s/VaccinatedByAgeIntensiveCare' % locale)

    # Vaccinated Fatal By Age
    fatal_vaccinated_by_age_plot = plot.generate_grouped_by_age_bar_plot(
        fatal_vaccinated_by_age_df,
        y='fatal',
        color='red',
        plot_type='vaccinated.fatal')
    plot.export_plot(fatal_vaccinated_by_age_plot, '%s/VaccinatedByAgeFatal' % locale)

    # Vaccinated Fatal Percentage By Age
    vaccinated_by_age_fatal_percentage_plot = plot.generate_grouped_by_age_bar_plot(
        vaccinated_by_age_fatal_percentage_df,
        y='fatal_percentage',
        color='red',
        plot_type='vaccinated.fatal_percentage')
    plot.export_plot(vaccinated_by_age_fatal_percentage_plot, '%s/VaccinatedByAgeFatalPercentage' % locale)

    # Monthly Vaccinated Fatal Percentage Plot
    vaccinated_fatal_percentage_plot = plot.generate_vaccinated_fatal_percentage_plot(vaccinated_fatal_percentage_df)
    plot.export_plot(vaccinated_fatal_percentage_plot, '%s/VaccinatedFatalPercentage' % locale)
