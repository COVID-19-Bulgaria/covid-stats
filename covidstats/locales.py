import i18n


def setup_i18n():
    i18n.load_path.append('../config/locales')
    i18n.set('filename_format', '{locale}.{format}')
    i18n.set('enable_memoization', True)
    i18n.set('fallback', 'en')


def set_locale(locale):
    i18n.set('locale', locale)


def t(key, **kwargs):
    return i18n.t(key, kwargs)

