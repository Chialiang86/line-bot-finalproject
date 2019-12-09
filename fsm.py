from transitions.extensions import GraphMachine
import pygraphviz
from utils import send_text_message

gender_dict = {"男": 1, "女": 0}

sign_dict = {3:"ari" ,4:"tau" ,5:"gem" ,6:"can" ,7:"leo" ,8:"vir" ,9:"lib" ,10:"sco" ,11:"sag" ,12:"cap" ,1:"aqu" ,2:"pis"}

whole_sign_dict = {3:"牡羊座" ,4:"金牛座" ,5:"雙子座" ,6:"巨蟹座" ,7:"獅子座" ,8:"處女座" ,9:"天秤座" ,10:"天蠍座" ,11:"射手座" ,12:"摩羯座" ,1:"水瓶座" ,2:"雙魚座"}

index_dict = {
    "ari" : { "ari" : 90, "tar" : 75, "gem" : 82, "can" : 47, "leo" : 94, "vir" : 65, "lib" : 85, "sco" : 70, "sag" : 99, "cap" : 58, "aqu" : 88, "pis" : 79},
    "tau" : { "ari" : 68, "tar" : 88, "gem" : 72, "can" : 75, "leo" : 45, "vir" : 97, "lib" : 57, "sco" : 78, "sag" : 61, "cap" : 93, "aqu" : 66, "pis" : 81},
    "gem" : { "ari" : 79, "tar" : 76, "gem" : 89, "can" : 71, "leo" : 81, "vir" : 57, "lib" : 93, "sco" : 69, "sag" : 86, "cap" : 64, "aqu" : 99, "pis" : 48},
    "can" : { "ari" : 52, "tar" : 82, "gem" : 78, "can" : 89, "leo" : 61, "vir" : 84, "lib" : 66, "sco" : 92, "sag" : 70, "cap" : 87, "aqu" : 74, "pis" : 97},
    "leo" : { "ari" : 97, "tar" : 56, "gem" : 79, "can" : 69, "leo" : 87, "vir" : 72, "lib" : 81, "sco" : 45, "sag" : 92, "cap" : 77, "aqu" : 84, "pis" : 62},
    "vir" : { "ari" : 61, "tar" : 91, "gem" : 76, "can" : 88, "leo" : 66, "vir" : 89, "lib" : 49, "sco" : 81, "sag" : 72, "cap" : 95, "aqu" : 55, "pis" : 84},
    "lib" : { "ari" : 85, "tar" : 74, "gem" : 98, "can" : 58, "leo" : 88, "vir" : 77, "lib" : 90, "sco" : 71, "sag" : 80, "cap" : 47, "aqu" : 95, "pis" : 64},
    "sco" : { "ari" : 60, "tar" : 80, "gem" : 68, "can" : 97, "leo" : 65, "vir" : 84, "lib" : 73, "sco" : 87, "sag" : 47, "cap" : 76, "aqu" : 57, "pis" : 92},
    "sag" : { "ari" : 92, "tar" : 70, "gem" : 81, "can" : 65, "leo" : 98, "vir" : 58, "lib" : 86, "sco" : 68, "sag" : 89, "cap" : 75, "aqu" : 78, "pis" : 44},
    "cap" : { "ari" : 43, "tar" : 97, "gem" : 70, "can" : 80, "leo" : 59, "vir" : 92, "lib" : 51, "sco" : 85, "sag" : 64, "cap" : 88, "aqu" : 74, "pis" : 77},
    "aqu" : { "ari" : 72, "tar" : 41, "gem" : 91, "can" : 58, "leo" : 78, "vir" : 64, "lib" : 96, "sco" : 51, "sag" : 82, "cap" : 69, "aqu" : 87, "pis" : 60},
    "pis" : { "ari" : 71, "tar" : 78, "gem" : 46, "can" : 93, "leo" : 61, "vir" : 65, "lib" : 74, "sco" : 99, "sag" : 54, "cap" : 82, "aqu" : 69, "pis" : 88}
}

date_dict = {
    3:21,
    4:20,
    5:21,
    6:22,
    7:23,
    8:23,
    9:23,
    10:24,
    11:23,
    12:22,
    1:20,
    2:19
}

max_dict = {
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31,
    1:31,
    2:29
}

class TocMachine(GraphMachine):

    is_enter = False
    is_next = False
    enter_arg = -1
    mode = []
    pair_arg = []
    err_dict = {}

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.mode = ["對方生日","匹配機率"]
        self.pair_arg = ["none" , "none"]
        self.err_dict = {"your_birth_err" : False, "his_birth_err" : False}

    def is_int(self,str_):
        try:
            val = int(str_)
            return True
        except ValueError:
            return False

    def is_going_to_gender(self, event):
        text = event.message.text
        return text.lower() == "男" or text.lower() == "女"

    def on_enter_gender(self, event):
        print("I'm entering gender")
        msg = str(event.message.text.lower())
        self.enter_arg = gender_dict[msg]
        self.is_enter = True
        call_dict = {"男":"小王子","女":"小公主"}
        reply_token = event.reply_token
        send_text_message(reply_token, call_dict[msg] + " 您好，請輸入您的生日～")

    def is_going_to_Aries(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 3 and (day >= date_dict[3] and day <= max_dict[3])) or (mon == 4 and (day < date_dict[4] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
            return False
        return False
            

    def on_enter_Aries(self, event):
        print("I'm entering state1")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[3]
        return_msg = "您是 牡羊座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Taurus(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 4 and (day >= date_dict[4] and day <= max_dict[4])) or (mon == 5 and (day < date_dict[5] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
            return False
        return False

    def on_enter_Taurus(self, event):
        print("I'm entering state2")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[4]
        return_msg = "您是 金牛座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Gemini(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 5 and (day >= date_dict[5] and day <= max_dict[5])) or (mon == 6 and (day < date_dict[6] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Gemini(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[5]
        return_msg = "您是 雙子座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Cancer(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 6 and (day >= date_dict[6] and day <= max_dict[6])) or (mon == 7 and (day < date_dict[7] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Cancer(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[6]
        return_msg = "您是 巨蟹座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Leo(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 7 and (day >= date_dict[7] and day <= max_dict[7])) or (mon == 8 and (day < date_dict[8] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Leo(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[7]
        return_msg = "您是 獅子座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Virgo(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 8 and (day >= date_dict[8] and day <= max_dict[8])) or (mon == 9 and (day < date_dict[9] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Virgo(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[8]
        return_msg = "您是 處女座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)
    
    def is_going_to_Libra(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 9 and (day >= date_dict[9] and day <= max_dict[9])) or (mon == 10 and (day < date_dict[10] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Libra(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[9]
        return_msg = "您是 天秤座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Scorpio(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 10 and (day >= date_dict[10] and day <= max_dict[10])) or (mon == 11 and (day < date_dict[11] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Scorpio(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[10]
        return_msg = "您是 天蠍座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Sagittarius(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 11 and (day >= date_dict[11] and day <= max_dict[11])) or (mon == 12 and (day < date_dict[12] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Sagittarius(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[11]
        return_msg = "您是 射手座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)
    
    def is_going_to_Capricorn(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 12 and (day >= date_dict[12] and day <= max_dict[12])) or (mon == 1 and (day < date_dict[1] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Capricorn(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[12]
        return_msg = "您是 摩羯座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Aquarius(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 1 and (day >= date_dict[1] and day <= max_dict[1])) or (mon == 2 and (day < date_dict[2] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Aquarius(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[1]
        return_msg = "您是 水瓶座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_Pisces(self, event):
        if self.is_enter == True and self.is_next == False :
            msg = str(event.message.text.lower())
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if (mon == 2 and (day >= date_dict[2] and day <= max_dict[2])) or (mon == 3 and (day < date_dict[3] and day >= 1)) :
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_Pisces(self, event):
        print("I'm entering state3")
        self.is_next = True
        if self.enter_arg != -1:
            self.pair_arg[self.enter_arg] = sign_dict[2]
        return_msg = "您是 雙魚座 喔～\n請輸入對方的生日!!!"
        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

    def is_going_to_result(self, event):
        text = event.message.text
        msg = str(event.message.text.lower())
        if (self.is_enter == True) and (self.is_next == True) :
            if msg.count("/") >= 1 and self.is_int(msg.split("/")[0]) and self.is_int(msg.split("/")[1]):
                mon = int(msg.split("/")[0])
                day = int(msg.split("/")[1])
                if mon >= 1 and mon <= 12 and day >= 1 and day <= max_dict[mon]:
                    return True
            self.err_dict["your_birth_err"] = True
        return False

    def on_enter_result(self, event):
        print("I'm entering state3")
        msg = str(event.message.text.lower())
        mon = int(msg.split("/")[0])
        day = int(msg.split("/")[1])
        return_msg = "對方為 ： "
        for m in range(1,13):
            if m == mon :
                if day >= date_dict[m] and day <= max_dict[m]:
                    if self.pair_arg[0] == "none":
                        self.pair_arg[0] = sign_dict[m]
                    else :
                        self.pair_arg[1] = sign_dict[m]
                    return_msg = return_msg + whole_sign_dict[m]
                elif day < date_dict[m] and day >= 0:
                    m_ = 12 if m - 1 == 0 else m - 1
                    if self.pair_arg[0] == "none":
                        self.pair_arg[0] = sign_dict[m_]
                    else :
                        self.pair_arg[1] = sign_dict[m_]
                    return_msg = return_msg + whole_sign_dict[m_]
                break
        print(self.pair_arg[0] + " " + self.pair_arg[1])

        score = index_dict[self.pair_arg[0]][self.pair_arg[1]]
        bless_msg = ""

        if score == 99:
            bless_msg = "你們最好不要在一起，不然赤道的太陽都沒你們閃＾＿＾"
        elif score >= 90:
            bless_msg = "不追就是憑實力單身了喔＾＿＾"
        elif score >= 80:
            bless_msg = "你們很配，錯失機會就準備當好朋友吧~"
        elif score >= 70:
            bless_msg = "相處起來還挺不錯，真的啦～"
        elif score >= 60:
            bless_msg = "時有火花、偶有摩擦\n"\
                "幫他撥蝦、還算不差"
        elif score >= 50:
            bless_msg = "其實最能長久的戀情，往往都不是最速配的愛情"
        elif score >= 40:
            bless_msg = "冤家"

        return_msg = \
        return_msg + "\n" +\
        "你們的速配指數為：" + str(score) + "\n\n" + \
        bless_msg 

        reply_token = event.reply_token
        send_text_message(reply_token, return_msg)

        self.enter_arg = -1
        self.is_enter = False
        self.is_next = False
        self.pair_arg = ["none", "none"]
        self.err_dict = {"your_birth_err" : False, "his_birth_err" : False}
        self.go_back()

    def on_exit_result(self):
        print("Leaving state3")
