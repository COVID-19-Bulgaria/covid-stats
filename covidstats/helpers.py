import epyestim.covid19 as covid19
import pydlm
import numpy as np
import datetime as dt

from locales import t


def estimate_rt(df):
    rt_df = covid19.r_covid(df, smoothing_window=21, r_window_size=7, quantiles=(0.05, 0.5, 0.95), auto_cutoff=False)

    return rt_df.dropna()


def predict_rt(df, start_point, number_of_predictions):
    linear_trend = pydlm.trend(degree=1, discount=0.9, name='linear_trend')
    simple_dlm = pydlm.dlm(df['Q0.5']) + linear_trend
    simple_dlm.fit()

    return simple_dlm.predictN(date=start_point, N=number_of_predictions)[0]


def draw_from_si(days_ago, si=covid19.generate_standard_si_distribution()):
    days_ago = np.array(days_ago)
    var_length = len(si)

    if max(days_ago) > var_length:
        si = np.append(si, np.repeat(0, max(days_ago) - var_length + 1))

    draws = si[days_ago - 1]

    return draws


def predict_cases(reported_cases, predicted_rts):
    predicted_cases = np.array([])
    rng = np.random.default_rng()

    for i in range(len(predicted_rts)):
        previous_cases = np.append(reported_cases, predicted_cases)[::-1]
        distribution = draw_from_si([*range(len(previous_cases))])

        predicted_cases = np.append(predicted_cases,
                                    rng.poisson(predicted_rts[i] * np.sum(np.multiply(previous_cases, distribution)),
                                                1)[0])

    return predicted_cases


def get_generation_date_text():
    date = dt.date.today()

    return date.strftime(t('plots.common.generation_date_subtitle'))