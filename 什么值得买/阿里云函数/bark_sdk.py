import requests
# from app_log import logger  # 导入 app_log 中的 logger


def send_message(url, text, title='', sound='', icon='', group='', to_url='', copy=''):
    # url
    # text:内容，不可为空
    # title：标题
    # sound声音
    #
    params = {}
    if title == '':
        url = '{}{}'.format(url, text)
    else:
        url = '{}{}/{}'.format(url, title, text)

    if sound == '':
        pass
    else:
        params['sound'] = sound

    if icon == '':
        pass
    else:
        params['icon'] = icon

    if group == '':
        pass
    else:
        params['group'] = group

    if to_url == '':
        pass
    else:
        params['url'] = to_url

    if copy == '':
        pass
    else:
        params['copy'] = copy
    response = requests.request("GET", url, params=params)
    print(response)


if __name__ == '__main__':
    url = ''
    text = 'test'
    title = 'title'
    sound = 'bell'
    send_message(url, text, title, sound='',
                 icon='', group='', to_url='', copy='')
