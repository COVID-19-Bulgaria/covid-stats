import pandas as pd
import datetime as dt

from covidstats import helpers


def get_week_cases_df():
    week_cases_df = pd.read_csv(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/WeekCasesDataset.csv')
    week_cases_df['date'] = week_cases_df.apply(
        lambda row: pd.to_datetime(dt.date.fromisocalendar(row.year, row.week, 7)), axis=1)

    return week_cases_df


def get_week_places_cases_df():
    week_places_cases_df = pd.read_csv(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/WeekPlacesCasesDataset.csv')
    week_places_cases_df['date'] = week_places_cases_df.apply(
        lambda row: dt.date.fromisocalendar(row.year, row.week, 7), axis=1)

    return week_places_cases_df


def get_active_cases_df():
    active_cases_dataset = pd.read_json(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/DateActiveCasesDataset.json'
    )
    active_cases_dataset['active'] = active_cases_dataset['active'].apply(pd.Series)

    return active_cases_dataset


def get_date_cases_df():
    date_cases_dataset = pd.read_json(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/DateCasesDataset.json')

    for column in ['infected', 'cured', 'fatal', 'hospitalized', 'intensive_care', 'medical_staff', 'pcr_tests',
                   'antigen_tests', 'vaccinated']:
        date_cases_dataset[column] = date_cases_dataset[column].apply(pd.Series)

    return date_cases_dataset


def get_date_diff_cases_df():
    date_diff_cases_dataset = pd.read_json(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/DateDiffCasesDataset.json')

    for column in ['infected', 'cured', 'fatal', 'hospitalized', 'intensive_care', 'medical_staff', 'pcr_tests',
                   'antigen_tests', 'vaccinated']:
        date_diff_cases_dataset[column] = date_diff_cases_dataset[column].apply(pd.Series)

    return date_diff_cases_dataset


def get_date_positive_tests_df():
    date_positive_tests_df = pd.read_csv('https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/'
                                         'Bulgaria/DatePositiveTestsDataset.csv', parse_dates=['date'])

    return date_positive_tests_df


def build_rts_df(predicted_rts, start_date):
    df_index = pd.date_range(start_date, periods=len(predicted_rts), freq='D')

    increase_rts = [row + row * 0.05 for row in predicted_rts]
    decline_rts = [row - row * 0.05 for row in predicted_rts]

    df = pd.DataFrame({
        'predicted_rt': predicted_rts,
        'increase_rt': increase_rts,
        'decline_rt': decline_rts
    }, index=df_index)

    return df


def build_predicted_cases_df(reported_cases, rts_df, start_date):
    df_index = pd.date_range(start_date, periods=len(rts_df), freq='D')

    df = pd.DataFrame({
        'predicted_cases': helpers.predict_cases(reported_cases, rts_df['predicted_rt']),
        'increase_cases': helpers.predict_cases(reported_cases, rts_df['increase_rt']),
        'decline_cases': helpers.predict_cases(reported_cases, rts_df['decline_rt'])
    }, index=df_index)

    return df


def build_weekly_predicted_cases_df(week_cases_df, predicted_cases_df, start_date):
    df = predicted_cases_df.groupby(pd.Grouper(freq='W')).mean()
    df['predicted_cases'] = df['predicted_cases'].multiply(7)
    df['increase_cases'] = df['increase_cases'].multiply(7)
    df['decline_cases'] = df['decline_cases'].multiply(7)

    start_date_weekday = start_date.weekday()
    start_of_week_date = start_date - dt.timedelta(days=start_date_weekday)
    end_of_week_date = start_of_week_date + dt.timedelta(days=6)

    if end_of_week_date >= start_date:
        if week_cases_df.loc[week_cases_df['date'] == end_of_week_date].empty:
            current_cases = week_cases_df[week_cases_df['date'] <= end_of_week_date].iloc[-1]['infected']
            previous_week_date = end_of_week_date - dt.timedelta(weeks=1)
            df.loc[previous_week_date] = [current_cases, current_cases, current_cases]
            df.sort_index(inplace=True)
        else:
            current_cases = week_cases_df[week_cases_df['date'] == end_of_week_date].iloc[-1]['infected']
            average_week_cases = (current_cases / (start_date_weekday + 1)) * 7

            week_cases_df.loc[week_cases_df['date'] == end_of_week_date, ['infected']] = average_week_cases

            df.loc[df.index == end_of_week_date, ['predicted_cases']] = average_week_cases
            df.loc[df.index == end_of_week_date, ['increase_cases']] = average_week_cases
            df.loc[df.index == end_of_week_date, ['decline_cases']] = average_week_cases

    return df


def build_weekly_positive_tests_df(date_positive_tests_df=get_date_positive_tests_df()):
    weekly_positive_tests_df = date_positive_tests_df.groupby(pd.Grouper(key='date', freq='W')).agg({
        'pcr_tests': 'sum',
        'antigen_tests': 'sum',
        'positive_percentage': 'mean',
        'positive_pcr_tests': 'sum',
        'pcr_positive_percentage': 'mean',
        'positive_antigen_tests': 'sum',
        'antigen_positive_percentage': 'mean'
    })

    weekly_positive_tests_df['date'] = weekly_positive_tests_df.index
    weekly_positive_tests_df['total_tests'] = weekly_positive_tests_df['pcr_tests'] \
                                              + weekly_positive_tests_df['antigen_tests']
    weekly_positive_tests_df['total_positive_tests'] = weekly_positive_tests_df['positive_pcr_tests'] \
                                                       + weekly_positive_tests_df['positive_antigen_tests']

    return weekly_positive_tests_df
