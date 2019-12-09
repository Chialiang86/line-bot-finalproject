import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=[
     "user"       , "gender"    ,
    "Aries"       , "Taurus"    , "Gemini"   , "Cancer"  ,
    "Leo"         , "Virgo"     , "Libra"    , "Scorpio" ,
    "Sagittarius" , "Capricorn" , "Aquarius" , "Pisces"  ,
    "result"
    ],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "gender",
            "conditions": "is_going_to_gender",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Aries",
            "conditions": "is_going_to_Aries",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Taurus",
            "conditions": "is_going_to_Taurus",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Gemini",
            "conditions": "is_going_to_Gemini",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Cancer",
            "conditions": "is_going_to_Cancer",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Leo",
            "conditions": "is_going_to_Leo",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Virgo",
            "conditions": "is_going_to_Virgo",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Libra",
            "conditions": "is_going_to_Libra",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Scorpio",
            "conditions": "is_going_to_Scorpio",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Sagittarius",
            "conditions": "is_going_to_Sagittarius",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Capricorn",
            "conditions": "is_going_to_Capricorn",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Aquarius",
            "conditions": "is_going_to_Aquarius",
        },
        {
            "trigger": "advance",
            "source": "gender",
            "dest": "Pisces",
            "conditions": "is_going_to_Pisces",
        },
        {
            "trigger": "advance",
            "source": [
                "Aries"       , "Taurus"    , "Gemini"   , "Cancer"  ,
                "Leo"         , "Virgo"     , "Libra"    , "Scorpio" ,
                "Sagittarius" , "Capricorn" , "Aquarius" , "Pisces"  ],
            "dest": "result",
            "conditions": "is_going_to_result",
        },
        {
            "trigger": "go_back",
            "source": "result",
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text + "yee")
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    msg = "<資工神良 的 星座小教室>\n\n"\
            "想知道您跟他/她的速配指數？\n"\
            "首先我們先拿出幸運草\n"\
            "把它放到手心吹一口氣\n\n\n"\
            "呼~~~~~~~\n\n\n"\
            "剛剛你弄丟了一株幸運草\n"\
            "你這個亂丟垃圾的壞小孩\n"\
            "好啦沒關係，反正首先\n"\
            "1.請先輸入您的性別\n"\
            "ex:男\n"\
            "2.再輸入您的生日\n"\
            "ex:2/29\n"\
            "3.愛的水晶球就浮現你們神聖的速配指數喔!!!"

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        #print(f"REQUEST BODY: \n{body}")
            
        response = machine.advance(event)
        if response == False:
            if machine.err_dict["your_birth_err"] == True :
                machine.err_dict["your_birth_err"] = False
                send_text_message(event.reply_token, "小叮嚀：您的生日輸入有誤喔！")
            elif machine.err_dict["his_birth_err"] == True :
                machine.err_dict["his_birth_err"] = False
                send_text_message(event.reply_token, "小叮嚀：他／她的生日輸入有誤喔！")
            else :
                send_text_message(event.reply_token, msg)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    #port = os.environ['PORT']
    app.run(host="0.0.0.0", port=port, debug=True)
