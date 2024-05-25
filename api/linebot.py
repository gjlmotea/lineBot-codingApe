from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
                            CarouselTemplate, MessageAction, URIAction, ImageCarouselColumn, ImageCarouselTemplate,
                            ImageSendMessage, ButtonsTemplate, ConfirmTemplate)
import os
import requests
from bs4 import BeautifulSoup
import random

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == 'confirm':
        confirm_template = TemplateSendMessage(
            alt_text = 'confirm template',
            template = ConfirmTemplate(
                text = '喝一口咖啡嗎?',
                actions = [
                    MessageAction(
                        label = 'yes',
                        text = '是的，我想喝一口！'),
                    MessageAction(
                        label = 'no',
                        text = '不，我不喝咖啡。')]
                )
            )
        line_bot_api.reply_message(event.reply_token, confirm_template)


    #按鈕樣板
    if event.message.text == 'button':
        buttons_template = TemplateSendMessage(
            alt_text = 'buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url='https://treeman.tw/wp-content/uploads/2023/09/%E6%8B%BF%E9%90%B5%E5%9C%96.jpg',
                title = 'Brown Cafe',
                text = 'Enjoy your coffee',
                actions = [
                    MessageAction(
                        label='1111111？',
                        text='11111！'),
                    MessageAction(
                        label='2222？',
                        text='22222！'),
                    MessageAction(
                        label='3333？',
                        text='3333！'),
                    MessageAction(
                        label='4444？',
                        text='4444！'),
                    MessageAction(
                        label='5555？',
                        text='555！'),
                    MessageAction(
                        label='今天要來一點咖啡嗎？',
                        text='我今天想喝咖啡！'),
                    MessageAction(
                        label = '咖啡有什麼好處',
                        text = '讓人有精神'),
                    URIAction(
                        label = '伯朗咖啡',
                        uri = 'https://www.youtube.com/watch?v=-kvY2AmbLOE&list=RDQMWaU5e3UbmI0&start_radio=1')]
                )
            )

        line_bot_api.reply_message(event.reply_token, buttons_template)


    #carousel樣板
    if event.message.text == 'carousel':
        carousel_template = TemplateSendMessage(
            alt_text = 'carousel template',
            template = CarouselTemplate(
                columns = [
                    #第一個
                    CarouselColumn(
                        thumbnail_image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title = 'this is menu1',
                        text = 'menu1',
                        actions = [
                            MessageAction(
                                label = '咖啡有什麼好處',
                                text = '讓人有精神'),
                            URIAction(
                                label = '伯朗咖啡',
                                uri = 'https://www.mrbrown.com.tw/')]),
                    #第二個
                    CarouselColumn(
                        thumbnail_image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        title = 'this is menu2',
                        text = 'menu2',
                        actions = [
                            MessageAction(
                                label = '咖啡有什麼好處',
                                text = '讓人有精神'),
                            URIAction(
                                label = '伯朗咖啡',
                                uri = 'https://www.mrbrown.com.tw/')]),
                    # 第三個
                    CarouselColumn(
                        thumbnail_image_url='https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcTZCSmCzmIPm0up8wmW566cK5w3sSTUChT5UnaU3VnFxrHwoRNSnks0xUBmj2r2oeJk',
                        title='這是可愛的貓咪',
                        text='咪咪咪咪咪咪咪',
                        actions=[
                            MessageAction(
                                label='吸貓有什麼好處',
                                text='讓人有精神！'),
                            URIAction(
                                label='貓咪可愛嗎？',
                                uri='https://puppy.hccg.gov.tw/ch/home.jsp?id=20033&parentpath=0,6')])
                ])
            )

        line_bot_api.reply_message(event.reply_token, carousel_template)


    #image carousel樣板
    if event.message.text == 'image carousel':
        image_carousel_template = TemplateSendMessage(
            alt_text = 'image carousel template',
            template = ImageCarouselTemplate(
                columns = [
                    #第一張圖
                    ImageCarouselColumn(
                        image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action = URIAction(
                            label = '伯朗咖啡',
                            uri = 'https://www.mrbrown.com.tw/')),
                    #第二張圖
                    ImageCarouselColumn(
                        image_url = 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
                        action = URIAction(
                            label = '伯朗咖啡',
                            uri = 'https://www.mrbrown.com.tw/'))
                ])
            )

        line_bot_api.reply_message(event.reply_token, image_carousel_template)

if __name__ == "__main__":
    app.run()