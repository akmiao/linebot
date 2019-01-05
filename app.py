from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from urllib.request import urlopen
import random

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ijmaUPJJoFEOC4u7aLMNugBoAZcaGqh7c88b/OOT5khRUi6Lr8FzVcq0yb1UiOJnyaFgOUN52x/m1Ua/gcJAZM5+DYOVQmmpeK/tGwloaGkOgqi2+ZVDo7Q5bbZpLL5CjvBveV13SMpJno6Jf7enuwdB04t89/1O/w1cDnyilFU=
')
# Channel Secret
handler = WebhookHandler('297ecd403cc0b1df4511ddcf70465600')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #確定訊息種類
    msg_type = 0
    image_key = ""
    image_name = ""
    reply_text = ""
    #4 - 你寧可回答
    if event.message.text.find("?刷牙刷牙啦") != -1:
        image_key = "yellow_teeth"
        reply_text = "臭牙齒！"
        msg_type = 4
    elif event.message.text.find("?洗臉洗臉啦") != -1:
        image_key = "the_scream"
        reply_text = "「為什麼大家都說我的臉很臭？」"
        msg_type = 4
    elif event.message.text.find("?我想吃！") != -1:
        image_key = "shit_curry"
        reply_text = "來，這盤是你的。"
        msg_type = 4
    #1 - 梗圖
    compare_txt = ["隨便圖", "幹話", "廢圖", "廢到笑"]
    for x in compare_txt:
        if event.message.text.find(x) != -1:
            #雜圖
            image_key = "others"
            image_name = "隨便圖"
            msg_type = 1
    compare_txt = ["FGO", "fgo", "Fate", "fate", "Fgo", "Fate Grand Order", "非的幹不過歐的"]
    for x in compare_txt:
        if event.message.text.find(x) != -1:
            #FGO
            image_key = "FGO"
            image_name = "FGO"
            msg_type = 1
    compare_txt = ["地獄", "hell", "HELL", "Hell", "地域"]
    for x in compare_txt:
        if event.message.text.find(x) != -1:
            #地獄
            image_key = "hell"
            image_name = "地獄"
            msg_type = 1
    #2 - 機器人被罵
    if msg_type < 1:
        compare_txt = ["廢物", "垃圾", "白癡", "滾", "北七", "你媽", "智障", "我考", "吃屎", "?屎", "媽的", "沙小", "殺小", "?三小？"]
        for x in compare_txt:
            if event.message.text.find(x) != -1:
                msg_type = 2
    #3 - 使用者詢問
    if msg_type < 2:
        compare_txt = ["怎麼用", "嗨", "有什麼梗圖", "總覽", "圖庫", "目錄"]
        for x in compare_txt:
            if event.message.text.find(x) != -1:
                msg_type = 3
    #回覆訊息
    if (msg_type == 1):
        count = 1
        
        count_txt = urlopen('https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/' + image_key + '/count.txt')
        count = int(str(count_txt.read()).replace("b'",'').replace("\\r",'').replace("\\n'",''))
        
        rImage = str(random.randint(1, count))
        message = (
            ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/' + image_key + '/' + rImage + '.jpg',
                preview_image_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/' + image_key + '/' + rImage + '.jpg'
            ),
            TextSendMessage(text=image_name + '梗圖第 ' + rImage + ' 張')
        )
    elif (msg_type == 2):
        count_txt = urlopen('https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/forkBot/count.txt')
        count = int(str(count_txt.read()).replace("b'",'').replace("\\r",'').replace("\\n'",''))

        rImage = str(random.randint(1, count))
        message = (
            ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/forkBot/' + rImage + '.jpg',
                preview_image_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/forkBot/' + rImage + '.jpg'
            )
        )
    elif (msg_type == 3):
        #說明文件
        message = (
            TextSendMessage(text="輸入關鍵詞查看指令種類梗圖：\n◆ FGO\n◆ 雜圖\n◆ 地獄")
        )
    elif (msg_type == 4):
        #你寧可
        if image_key != "":
            message = (
                ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/WYR/' + image_key + '.jpg',
                    preview_image_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/WYR/' + image_key + '.jpg'
                ),
                TextSendMessage(text=reply_text)
            )
        else:
            message = (TextSendMessage(text=reply_text))
    else:
        #當機器人看不懂時
        if (random.randint(1, 100) >= 75):
            #你寧可題目
            rndQ = random.randint(1, 2)
            if rndQ == 1:
                message = TemplateSendMessage(
                    alt_text='你寧可一輩子不能...？',
                    template=ConfirmTemplate(
                        text='你寧可一輩子不能...',
                        actions=[
                            PostbackTemplateAction(
                                label='刷牙',
                                text='?一輩子不能刷牙',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='洗臉',
                                text='?一輩子不能洗臉'
                            )
                        ]
                    )
                )
            else:
                message = TemplateSendMessage(
                    alt_text='你寧可吃...？',
                    template=ConfirmTemplate(
                        text='你寧可吃屎味咖哩還是吃咖哩味屎？',
                        actions=[
                            PostbackTemplateAction(
                                label='我全都要',
                                text='?我全都要吃！',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='三小？',
                                text='?三小？'
                            )
                        ]
                    )
                )
        elif (random.randint(1, 100) > 55):
            message = (TextSendMessage(text="不知道要講什麼的話可以問我\n「這個機器人怎麼用？」"))
        elif (random.randint(1, 100) > 20):
            message = (TextSendMessage(text=event.message.text.replace("！",'').replace("!",'') + '?'))
        else:
            # 20%機率會被機器人用梗圖嗆
            count_txt = urlopen('https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/chokeUser/count.txt')
            count = int(str(count_txt.read()).replace("b'",'').replace("\\r",'').replace("\\n'",''))

            rImage = str(random.randint(1, count))
            message = (
                ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/chokeUser/' + rImage + '.jpg',
                    preview_image_url='https://raw.githubusercontent.com/RenaWevin/meme-bot1919810/master/chokeUser/' + rImage + '.jpg'
                )
            )
    
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
