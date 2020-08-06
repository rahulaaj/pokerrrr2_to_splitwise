from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from pathlib import Path
from requests_oauthlib import OAuth1
from requests import Request, sessions
import datetime
import requests
import os
import json
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

SPLITWISE_BASE_URL = "https://secure.splitwise.com/"
SPLITWISE_VERSION = "v3.0"
CREATE_EXPENSE_URL = SPLITWISE_BASE_URL + "api/" + SPLITWISE_VERSION + "/create_expense"

# Consumer keys for splitwise
consumer_key = ""
consumer_secret = ""

# Access token for splitwise
access_token = {'oauth_token': '', 'oauth_token_secret': ''}
auth = OAuth1(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token['oauth_token'], resource_owner_secret=access_token['oauth_token_secret'])

# Splitwise group id e.g. "192136318"
group_id = "192136318"

# Create member dictionary of {"member_id_pokerrrr2": member_id_splitwise} e.g. {"#AB0X7": 6167766, "#X4S0D": 31283953}
members = {"#AB0X7": 6167766, "#X4S0D": 31283953}

# OCR API key
ocr_api_key = ""

# Screenshot directory on mobile
dirpath = "/storage/emulated/0/DCIM/Screenshots/"

def get_profit(text):
    word_list = text.split("\t")
    profit = "0"
    for word in word_list:
        if word.startswith("+") or word.startswith("-"):
            profit = word
            break
    return int(profit.replace(",", "").replace(".", "").replace("o", "0").replace("O", "0"))

def postRequest(url, method="POST", data=None, files=None):
    request_obj = Request(method=method, url=url, data=data, auth=auth, files=files)
    prep_req = request_obj.prepare()
    with sessions.Session() as session:
        response = session.send(prep_req)
    if response.status_code == 200:
        if (response.content and hasattr(response.content, "decode")):
            return response.content.decode("utf-8")
        return response.content
    else:
        print(response.content)
        return None

def setUserArray(users, user_array):
    for count, user in enumerate(users):
        user_dict = user.__dict__
        for key in user_dict:
            if key == "id":
                gen_key = "user_id"
            else:
                gen_key = key
            user_array["users__" + str(count) + "__" + gen_key] = user_dict[key]

# Convert image to text
# Get latest screenshot from dirpath directory
results = str(sorted(Path(dirpath).iterdir(), key=os.path.getmtime, reverse=True)[0])
payload = {'apikey': ocr_api_key, 'scale': True, 'isTable': True,}
with open(results, 'rb') as f:
    r = requests.post('https://api.ocr.space/parse/image', files={results: f}, data=payload,)
    text = json.loads(r.content.decode())["ParsedResults"][0]["ParsedText"].splitlines()
    print(text)
    results_dict = {}
    num_players = 0
    for i in range(0, len(text)):
        word_list = text[i].split("\t")
        word = word_list[-2]
        if word.startswith("#"):
            results_dict[word] = get_profit(text[i-2] + text[i-1])
    print(results_dict)

# Convert results to splitwise expense
expense_data = {"group_id": group_id, "description": (datetime.date.today()).strftime("%d %B")}
expense_users = []
total = 0
for member in results_dict:
    profit = results_dict[member]
    user1 = ExpenseUser()
    user1.setId(members[member])
    if profit < 0:
        user1.setOwedShare(str(-profit))
        user1.setPaidShare('0')
    else:
        user1.setPaidShare(str(profit))
        user1.setOwedShare('0')
        total = total + profit
    expense_users.append(user1)
expense_data["cost"] = str(total)
setUserArray(expense_users, expense_data)
content = postRequest(CREATE_EXPENSE_URL, data=expense_data, files={"receipt": open(results, 'rb')})
content = json.loads(content)
if bool(content["errors"]):
    print(content["errors"])
