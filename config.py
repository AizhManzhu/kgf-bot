from os.path import exists

if not exists('localconfig.py'):
    DOMAIN = 'https://kgf.cic.kz/api'
    TOKEN = '5168514956:AAHKstmZ4JGifLKHP3nG_gewg_rzl6-SUmA'
else:
    import localconfig

    DOMAIN = localconfig.DOMAIN
    TOKEN = localconfig.TOKEN
