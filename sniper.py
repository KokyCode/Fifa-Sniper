import requests
import json
import time
from playsound import playsound
from bs4 import BeautifulSoup as bs

class colors:
    LOADING = '\033[95m'
    MESSAGE = '\033[94m'
    SUCCESS = '\033[96m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def CheckCaptcha():
    global key
    url = "https://utas.external.s2.fut.ea.com/ut/game/fifa21/captcha/fun/data"
    headers = {'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'X-UT-SID': sid,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Accept-Language': 'en-ie',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'}

    r = requests.get(url, headers = headers)
    data = r.json()
    key = data["pk"]
    print(key)
    return r.text

def GetCheapestPrice(itemid):
    cheapest = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'X-UT-SID': sid,
    'Accept-Language': 'en-ie',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br'}

    url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa21/transfermarket?num=21&start=0&type=player&maskedDefId=' + str(itemid)
    r = requests.get(url, headers = headers)
    data = r.json()
    players = data["auctionInfo"]
    if "expired session" in r.text:
       print(colors.WARNING + "Access token has expired. Please renew your token. Possible Repatcha, check the app.")

    if r.status_code == 458:
        print(colors.WARNING + "Captcha required.")

    if "buyNowPrice" in r.text:
        for p in players:
            price = p["buyNowPrice"]
            #print(colors.SUCCESS + "Found cheaper than Max Buy Now!" + " $" + str(p["buyNowPrice"]) + " TradeID: " + str(p["tradeId"]))
            #bnprice = p["buyNowPrice"]
            #tradeid = p["tradeId"]
            cheapest.append(price)
            #itemid = p["itemData"]["id"] #Used to if we wanna sell the item.
            #BuyPlayer(tradeid, bnprice)
    else:
        print("No items found")
    return min(cheapest)

def GetPlayerCoins():
    url = "https://utas.external.s2.fut.ea.com/ut/game/fifa21/watchlist"
    
    headers = {
    'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'X-UT-SID': sid,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Accept-Language': 'en-ie',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br'}

    r = requests.get(url, headers = headers)
    if r.status_code == 458:
        print(colors.WARNING + "Captcha required.")

    data = r.json()
    coins = data["credits"]
    return coins

def SellPlayer(item, price, bid):
    url = "https://utas.external.s2.fut.ea.com/ut/game/fifa2/item"

    headers = {'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'Origin': 'file://',
    'Connection': 'keep-alive',
    'X-UT-SID': sid,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Length': '49',
    'Accept-Language': 'en-ie',
    'Accept-Encoding': 'gzip, deflate, br'}

    postdata = '{"itemData":[{"id":' + str(item) + ',"pile":"trade"}]}'
    r = requests.put(url, data = postdata, headers = headers)

    if r.status_code == 458:
        print(colors.WARNING + "Captcha required.")

    if '"success":true' in r.text:
        url = "https://utas.external.s2.fut.ea.com/ut/game/fifa21/auctionhouse"
        headers = {'Host': 'utas.external.s2.fut.ea.com',
        'Content-Type': 'application/json',
        'Origin': 'file://',
        'Connection': 'keep-alive',
        'X-UT-SID': sid,
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Content-Length': '86',
        'Accept-Language': 'en-ie',
        'Accept-Encoding': 'gzip, deflate, br'}
        post = '{"itemData":{"id":' + str(item) +  '},"startingBid":' + str(bid) + ',"duration":3600,"buyNowPrice":' + str(price) + '}'
        #print(post)
        r = requests.post(url, data = post, headers = headers)
        if r.status_code == 458:
            print(colors.WARNING + "Captcha required.")
        if "needsGroupsRefresh" in r.text:
            print(colors.WARNING + "You have put " + player +  " up for sale!")
            SnipePlayer(pid, maxbuynow, 0)
        else:
            print(colors.FAIL + "Failed to sell player. Printing debug.")
            SnipePlayer(pid, maxbuynow, 0)
            print(r.text)    
    else:
        print(colors.FAIL + "The player failed to sell. I'm not sure why, please check your assigned items.")
        SnipePlayer(pid, maxbuynow, 0)
def BuyPlayer(tradeid, price):
    headers = {'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'Origin': 'file://',
    'Connection': 'keep-alive',
    'X-UT-SID': sid,
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Length': '11',
    'Accept-Language': 'en-ie',
    'Accept-Encoding': 'gzip, deflate, br'}

    url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa21/trade/' + str(tradeid) + '/bid'
    postdata = '{"bid":' + str(price) + '}'
    r = requests.put(url, data = postdata, headers = headers)
    if "Permission Denied" in r.text:
        print(colors.FAIL + "Failed to buy the player. Trying again...")
        SnipePlayer(pid, maxbuynow, 0) # SEEMS TO BE PROBLEM HERE. FIX ASAP.
    else:   
        print(colors.SUCCESS + "You have purchased " + colors.WARNING +  player +  colors.SUCCESS + " at " + colors.OK + "$" + str(price) + colors.SUCCESS + ".")
        playsound('C:/Users/customer/Documents/GitHub/FifaSniper/notify.mp3')
        sell = input(colors.MESSAGE + "Do you want to sell this player? (yes/no): ")
        if sell == "yes":
            bid = input(colors.WARNING + "What price do you want to set the" + colors.OK + " starting bid" + colors.WARNING + " price at?: ")
            saleprice = input(colors.WARNING + "What price do you want to" + colors.OK + " sell" + colors.WARNING + " this player at? (paid $" + str(price) + ").")
            SellPlayer(itemid, saleprice, bid)
        else:
            print(colors.WARNING + "You have kept this player, he will be in your unnasigned items.")
    if r.status_code == 458:
        print(colors.WARNING + "Captcha required.")
def SnipePlayer(id, maxbuynow, attempts):
    global tradeid
    global itemid

    tries = attempts + 1
    headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Host': 'utas.external.s2.fut.ea.com',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'X-UT-SID': sid,
    'Accept-Language': 'en-ie',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br'}

    url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa21/transfermarket?num=21&start=0&type=player&maskedDefId=' + str(id) + '&maxb=' + str(maxbuynow)
    r = requests.get(url, headers = headers)
    data = r.json()
    players = data["auctionInfo"]
    if r.status_code == 458:
        print(colors.WARNING + "Captcha required.")
    if "expired session" in r.text:
       print(colors.WARNING + "Access token has expired. Please renew your token. Possible Repatcha, check the app.")
    if "buyNowPrice" in r.text:
        for p in players:
            price = p["buyNowPrice"]
            #print(price)
            if price <= maxbuynow:
                    print(colors.SUCCESS + "Found cheaper than Max Buy Now!" + " $" + str(p["buyNowPrice"]) + " TradeID: " + str(p["tradeId"]))
                    bnprice = p["buyNowPrice"]
                    tradeid = p["tradeId"]
                    itemid = p["itemData"]["id"] #Used to if we wanna sell the item.
                    BuyPlayer(tradeid, bnprice)
                    break
    else:
        if(tries > 9):
            print(colors.FAIL + "Preventing market ban. Pausing for 15 seconds....")
            tries = 0
            time.sleep(15)
            print(colors.WARNING + "Preparing to search....")

        print(colors.FAIL + "Searching.... still nothing found. Searching again.")
        time.sleep(0.3)
        SnipePlayer(id, maxbuynow, tries)


def SearchPlayer(name):
    global pid
    global maxbuynow
    print(colors.LOADING + "Searching for " + name + ". This can take some time, please wait.")
    url = 'https://www.ea.com/fifa/ultimate-team/web-app/content/21D4F1AC-91A3-458D-A64E-895AA6D871D1/2021/fut/items/web/players.json?_=21069'
    r = requests.get(url)
    data = r.json()
    players = data["Players"]
    for p in players:
        lastname = p["l"]
        if name in lastname:
            print(colors.SUCCESS + "(" + str(p["r"]) + " rated)" + p["f"] + " " + p["l"] + " " + colors.OK + " - " + "ID: " + str(p["id"]))
    pid = int(input(colors.SUCCESS + "All players have loaded. Please type the ID of the player you want to snipe: "))
    #print(colors.OK + "Cheapest price found for " + name + " is: $" + str(GetCheapestPrice(pid)))
    maxbuynow = int(input(colors.WARNING + "Preparing to snipe for " + player + ", please input your max Buy Now: "))
    print(colors.SUCCESS + "Preparing to snipe " + name + " for $" + str(maxbuynow) + " or cheaper....")
    time.sleep(5)
    SnipePlayer(pid, maxbuynow, 0)

def grabSID(code):
    global sid
    global player
    headers = {
    'Host': 'utas.external.s2.fut.ea.com',
    'X-UT-PHISHING-TOKEN': '0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Accept-Language': 'en-ie',
    'Content-Type': 'application/json',
    'Origin': 'file://',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Connection': 'keep-alive',
    'Content-Length': '345'}
    url = 'https://utas.external.s2.fut.ea.com/ut/auth'
    payload = '{"isReadOnly":false,"sku":"FUT21IOS","clientVersion":7,"locale":"en-US","method":"authcode","priorityLevel":4,"identification":{"authCode":' + '"' + code + '"' + ',' + '"redirectUrl":"nucleus:rest"},"nucleusPersonaId":1005132993339,"gameSku":"FFA21PS4","ds":"a39ce0e1e68dc2835c1c581189025d1b5ae615bc8931e58382dc873f1322dbf4/8b4d"}'
    r = requests.post(url, data=payload, headers=headers)
    data = r.json()
    sid = data["sid"]
    print(colors.SUCCESS + "SID found: " + colors.OK + sid)
    print(colors.WARNING + "Logged in with " + str(GetPlayerCoins()) + " coins.")
    player = input(colors.MESSAGE + "What player would you like to snipe? (Last name only): ")
    SearchPlayer(player)

def Login(accesstoken):
    global code
    headers ={
        'Host':'accounts.ea.com',
        'Accept':'*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Accept-Language': 'en-ie',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    url = "https://accounts.ea.com/connect/auth?client_id=FOS-SERVER&redirect_uri=nucleus:rest&response_type=code&access_token=" + accesstoken + "&release_type=prod&client_sequence=shard2"
    r = requests.get(url, headers = headers)
    if "access_token is invalid" in r.text:
        print(colors.WARNING + "Access token has expired. Please renew your token.")
        exit()
    data = r.json()
    code = data["code"]
    print(colors.SUCCESS + "Logged in. Code has been found: " + colors.OK + code)
    grabSID(code)
print(colors.LOADING + "Welcome to Fifa Sniper - Developed by _WDM_. v1.0.3")
accesstoken = input(colors.MESSAGE + "Please input your access token in order to proceed: ")
print(colors.OK + "Access token inputted. Attempting login.")

Login(accesstoken)

