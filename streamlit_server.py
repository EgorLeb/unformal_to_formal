import streamlit as st
import requests
import json

folder_id = 'b1gql3ul5bq1rbuv2fvg'
IAM_token = "t1.9euelZqYipnMyY2YzcfOmMbOjM-Smu3rnpWanoyZxo7HxpOKio-Yx8qVjpDl8_clUxhP-e87CA51_N3z92UBFk_57zsIDnX8zef1656VmpiOi5Kbi4qczI_JzcybnpSP7_zF656VmpiOi5Kbi4qczI_JzcybnpSP._GAPD9v9kQoeaKPrLCJB6-s1Ez87V5itO_RueFWd7d3oDQDjuJFyAHGWbB-TYsYL8W7RHiCz7UmboildvTQpDg"


# temporary token


def request_YandexGPT(text_list, folder_id, IAM_token):
    prompt = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",

        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Я готовлю датасет для перевода предложений из неформального языка в формальный. У меня есть набор русских твитов, можешь сделать текст более официальным и формальным. Напиши этот текст будто ты профессор русского языка. Проверь, что в ответе нет матов, и разговорных слов. Избегай неофициальных слов. Заменяй маты во всех их вариациях! Старайся сохранить эмоцию автора. Убедись, что выходные данные пронумерованы с нуля. На каждый вход ровно один выход. Для разделения используй символ '\n'. Выведи только исправленный список, не выводи лишнего."
            },
            {
                "role": "user",
                "text": str(text_list)
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IAM_token}",
        "x-folder-id": folder_id

    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    return json.loads(result)['result']['alternatives'][0]['message']['text']


st.title("Informal to formal")

text = st.text_area("Введите текст в неформальной форме", max_chars=300, height=150)

if st.button("Перевести"):
    st.text_area("Ответ", max_chars=300, height=150, value=", блять, ".join(text.upper().split()))
else:
    st.text_area("Ответ", max_chars=300, height=150)

st.text("Помогите дообучить модель, как вам перевод конкретно этого предложения?")

c1, c2, c3, c4, c5, c6 = st.columns(6)
if c1.button("Хорошо"):
    pass

if c2.button("Плохо"):
    pass

if st.button("Хочу увидеть что ответит Yandex-GPT"):
    if text.strip() != '':
        value = request_YandexGPT(text, folder_id, IAM_token)

        st.text_area("вот что выдал Yandex-GPT:", max_chars=300, height=150, value=value)
    else:
        st.text("Напишите хоть что-то...")
