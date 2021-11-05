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
                   'positive_pcr_tests', 'antigen_tests', 'positive_antigen_tests', 'vaccinated']:
        date_cases_dataset[column] = date_cases_dataset[column].apply(pd.Series)

    date_cases_dataset['date'] = date_cases_dataset.index

    return date_cases_dataset


def get_date_cases_age_df():
    date_cases_age_df = pd.read_csv('https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/'
                                    'Bulgaria/CasesAgeDataset.csv', parse_dates=['date'])

    return date_cases_age_df


def build_date_diff_cases_age_df(df=get_date_cases_age_df()):
    date_diff_cases_age_df = pd.DataFrame({'date': df['date']})
    for column in ['group_0_19', 'group_20_29', 'group_30_39', 'group_40_49', 'group_50_59', 'group_60_69',
                   'group_70_79', 'group_80_89', 'group_90']:
        date_diff_cases_age_df[column] = df[column].diff()

    return date_diff_cases_age_df.dropna()


def get_date_diff_cases_df():
    date_diff_cases_dataset = pd.read_json(
        'https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/Bulgaria/DateDiffCasesDataset.json')

    for column in ['infected', 'cured', 'fatal', 'hospitalized', 'intensive_care', 'medical_staff', 'pcr_tests',
                   'positive_pcr_tests', 'antigen_tests', 'positive_antigen_tests', 'vaccinated']:
        date_diff_cases_dataset[column] = date_diff_cases_dataset[column].apply(pd.Series)

    date_diff_cases_dataset['date'] = date_diff_cases_dataset.index

    return date_diff_cases_dataset


def get_date_positive_tests_df():
    date_positive_tests_df = pd.read_csv('https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/master/'
                                         'Bulgaria/DatePositiveTestsDataset.csv', parse_dates=['date'])

    return date_positive_tests_df


def get_rolling_biweekly_places_cases_df():
    rolling_biweekly_places_cases_df = pd.read_csv('https://raw.githubusercontent.com/COVID-19-Bulgaria/covid-database/'
                                                   'master/Bulgaria/RollingBiWeeklyPlacesCasesDataset.csv',
                                                   parse_dates=['date'])

    return rolling_biweekly_places_cases_df


def get_data_egov_bg_df(resource):
    df = pd.read_csv(resource,
                     storage_options={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.'
                                       '36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'},
                     parse_dates=['Дата'], cache_dates=True, encoding='utf-8')

    return df


def get_infected_by_age_group_df():
    infected_by_age_group_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                                   '8f62cfcf-a979-46d4-8317-4e1ab9cbd6a8/csv')
    infected_by_age_group_df.rename(columns={'Дата': 'date'}, inplace=True)

    return infected_by_age_group_df


def get_fatal_by_age_group_df():
    fatal_by_age_group_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                                '18851aca-4c9d-410d-8211-0b725a70bcfd/csv')
    rename_age_df_columns(fatal_by_age_group_df, 'Брой починали', 'fatal')

    return fatal_by_age_group_df


def rename_age_df_columns(df, column_bg, column_en):
    df.rename(columns={
        'Дата': 'date',
        'Пол': 'sex',
        'Възрастова група': 'age',
        column_bg: column_en
    }, inplace=True)


def build_total_infected_by_age_group_df(df):
    total_infected_by_age_group_df = df[df['date'] == df['date'].max()].drop(['date', '0 - 19'], axis=1)
    total_infected_by_age_group_df = total_infected_by_age_group_df.melt(var_name='age', value_name='infected')
    total_infected_by_age_group_df['infected'] = pd.to_numeric(total_infected_by_age_group_df['infected'])

    return total_infected_by_age_group_df


def aggregate_0_19_age_group(df):
    age_group_0_19 = df.iloc[lambda row: row.index < df[df['age'] == '20 - 29'].index[0]].sum()[1]
    rest_age_groups = df.iloc[lambda row: row.index >= df[df['age'] == '20 - 29'].index[0]].reset_index(drop=True)

    rest_age_groups.loc[len(rest_age_groups.index)] = ['0 - 19', age_group_0_19]
    rest_age_groups.sort_values(by='age', inplace=True, ignore_index=True)

    return rest_age_groups


def rename_vaccinated_df_columns(df, column_bg, column_en):
    df.rename(columns={
        'Дата': 'date',
        'Ваксина': 'vaccine',
        'Пол': 'sex',
        'Възрастова група': 'age',
        column_bg: column_en
    }, inplace=True)


def get_infected_vaccinated_df():
    infected_vaccinated_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                                 'e9f795a8-0146-4cf0-9bd1-c0ba3d9aa124/csv')
    rename_vaccinated_df_columns(infected_vaccinated_df, 'Брой заразени', 'infected')

    return infected_vaccinated_df


def get_hospitalized_vaccinated_df():
    hospitalized_vaccinated_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                                     '6fb4bfb1-f586-45af-8dd2-3385499c3664/csv')
    rename_vaccinated_df_columns(hospitalized_vaccinated_df, 'Брой хоспитализирани', 'hospitalized')

    return hospitalized_vaccinated_df


def get_intensive_care_vaccinated_df():
    intensive_care_vaccinated_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                                       '218d49de-88a8-472a-9bb2-b2a373bd7ab4/csv')
    rename_vaccinated_df_columns(intensive_care_vaccinated_df, 'Брой в интензивно отделение', 'intensive_care')

    return intensive_care_vaccinated_df


def get_fatal_vaccinated_df():
    fatal_vaccinated_df = get_data_egov_bg_df('https://data.egov.bg/resource/download/'
                                              'e6a72183-28e0-486a-b4e4-b5db8b60a900/csv')
    rename_vaccinated_df_columns(fatal_vaccinated_df, 'Брой починали', 'fatal')

    return fatal_vaccinated_df


def build_grouped_by_age_df(df, filter_column):
    grouped_by_age_df = df[df[filter_column] != '-'].groupby('age').sum()
    grouped_by_age_df.reset_index(inplace=True)

    return grouped_by_age_df


def build_grouped_by_age_fatal_percentage_df(infected_by_age_df, fatal_by_age_df):
    grouped_by_age_fatal_percentage_df = pd.merge(infected_by_age_df, fatal_by_age_df, on='age', how='outer')
    grouped_by_age_fatal_percentage_df['fatal'] = grouped_by_age_fatal_percentage_df['fatal'].fillna(0)
    grouped_by_age_fatal_percentage_df['fatal_percentage'] = (
            grouped_by_age_fatal_percentage_df['fatal'] * 100 / grouped_by_age_fatal_percentage_df['infected'])\
        .round(decimals=2)

    return grouped_by_age_fatal_percentage_df


def build_date_vaccinated_fatal_df(fatal_vaccinated_df):
    date_vaccinated_fatal_df = fatal_vaccinated_df[fatal_vaccinated_df.vaccine != '-'].groupby(
        pd.Grouper(key='date', freq='D')).sum()
    date_vaccinated_fatal_df.reset_index(inplace=True)

    date_vaccinated_fatal_df.rename(columns={'fatal': 'fatal_vaccinated'}, inplace=True)

    return date_vaccinated_fatal_df


def build_vaccinated_fatal_percentage_df(date_vaccinated_fatal_df, date_diff_cases_df):
    vaccinated_fatal_percentage_df = pd.merge(date_vaccinated_fatal_df, date_diff_cases_df[['fatal', 'date']],
                                              on='date',
                                              how='outer')
    vaccinated_fatal_percentage_df = vaccinated_fatal_percentage_df[
        vaccinated_fatal_percentage_df['date'] >= pd.to_datetime('2021-01-01')]
    vaccinated_fatal_percentage_df['fatal_vaccinated'] = vaccinated_fatal_percentage_df['fatal_vaccinated'].fillna(0)
    vaccinated_fatal_percentage_df.sort_values(by='date', inplace=True)
    vaccinated_fatal_percentage_df = vaccinated_fatal_percentage_df.groupby(pd.Grouper(key='date', freq='M')).sum()
    vaccinated_fatal_percentage_df['fatal_vaccinated_percentage'] = vaccinated_fatal_percentage_df[
                                                                        'fatal_vaccinated'] * 100 / \
                                                                    vaccinated_fatal_percentage_df['fatal']

    return vaccinated_fatal_percentage_df


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
