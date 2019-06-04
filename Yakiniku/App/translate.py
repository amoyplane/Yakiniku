import requests
import json


def ask_translation(language_type, content):
    url = "https://translation.googleapis.com/language/translate/v2"
    data = {
        'key': 'AIzaSyAeQO_0q-juL_-2TCA3nrUkMTCbh9kg3p0',
        'source': language_type,
        'target': 'zh-CN',
        'q': content,
        'format': 'text'
    }
    headers = {'X-HTTP-Method-Override': 'GET'}
    response = requests.post(url, data=data, headers=headers)
    res = response.json()
    text = res["data"]["translations"][0]["translatedText"]
    # print(content)
    # print(text)
    return text


if __name__ == '__main__':
    language_type = "ja"
    content = "あのとき。春にここで田中のことを好きになりはじめたのはたしかに。田中が誰のことも好きにならないって言ったからだった。"
    trans_ans = ask_translation(language_type, content)
    print(content)
    print(trans_ans)
