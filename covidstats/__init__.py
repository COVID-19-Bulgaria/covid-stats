'''
covid-stats: Main module

Copyright 2021, Veselin Stoyanov
Licensed under Attribution-NonCommercial-ShareAlike 4.0 International.
'''

from covidstats import data, plot
import datetime as dt


def main():
    plot.setup_sns()

    week_cases_df = data.get_week_cases_df()
    date_diff_cases_df = data.get_date_diff_cases_df()
    active_cases_df = data.get_active_cases_df()
    week_places_cases_df = data.get_week_places_cases_df()

    # Weekly infected and cured cases plot
    infected_cured_week_cases_plot = plot.generate_week_cases_plot(
        df=week_cases_df,
        value_vars=['infected', 'cured'],
        hue_order=['infected', 'cured'],
        palette=['orange', 'green'],
        legend=['Заразени', 'Излекувани']
    )
    plot.export_plot(infected_cured_week_cases_plot, 'WeeklyInfectedCured')

    # Weekly hospitalized, intensive care and fatal cases plot
    hospitalized_intensive_fatal_week_cases_plot = plot.generate_week_cases_plot(
        df=week_cases_df,
        value_vars=['hospitalized', 'intensive_care', 'fatal'],
        hue_order=['hospitalized', 'intensive_care', 'fatal'],
        palette=['pink', 'purple', 'red'],
        legend=['Хоспитализирани', 'Интензивни грижи', 'Жертви']
    )
    plot.export_plot(hospitalized_intensive_fatal_week_cases_plot, 'WeeklyHospitalizedIntensiveCareFatal')

    # Weekly places cases plot
    places_cases_week_plot = plot.generate_week_places_cases_plot(week_places_cases_df)
    plot.export_plot(places_cases_week_plot, 'WeeklyPlacesCases')

    # 14 days forecast
    start_date = dt.date.today() + dt.timedelta(days=1)
    weekly_14_days_forecast_plot = plot.generate_weekly_14_days_prediction_plot_for_date(start_date, week_cases_df,
                                                                                         date_diff_cases_df)
    plot.export_plot(weekly_14_days_forecast_plot, 'Weekly14DaysForecast')

    # Active cases plot
    active_cases_plot = plot.generate_active_cases_plot(active_cases_df)
    plot.export_plot(active_cases_plot, 'ActiveCases')
