from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from pathlib import Path
import datetime
import requests
import os
import json
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

# Consumer keys for splitwise
consumer_key = ""
consumer_secret = ""

# Access token for splitwise
access_token = {'oauth_token': '', 'oauth_token_secret': ''}

# Splitwise group id e.g. "192136318"
group_id = "192136318"

# Create member dictionary of {"member_id_pokerrrr2": member_id_splitwise} e.g. {"#AB0X7": 6167766, "#X4S0D": 31283953}
members = {"#AB0X7": 6167766, "#X4S0D": 31283953}

# OCR API key
ocr_api_key = ""

# Screenshot directory on mobile
dirpath = "/storage/emulated/0/DCIM/Screenshots/"
# Get latest screenshot from dirpath directory
results = str(sorted(Path(dirpath).iterdir(), key=os.path.getmtime, reverse=True)[0])

def get_profit(text):
    word_list = text.split("\t")
    profit = None
    for word in word_list:
        if word.startswith("+") or word.startswith("-") or word == "0" or word == "O" or word == "o":
            profit = int(word.replace(",", "").replace(".", "").replace("o", "0").replace("O", "0").replace(" ", ""))
            break
    return profit

def get_frequency(elem, list):
    count = 0
    for element in list:
        if elem == element:
            count = count + 1
    return count

def deduce_profit_of_none_player(results_dict):
    total = 0
    for member in results_dict:
        if results_dict[member] is not None:
            total = total + results_dict[member]
    profit = -total
    for member in results_dict:
        if results_dict[member] is None:
            results_dict[member] = profit
            break
    return results_dict

def get_member_from_id(word):
    if word in members:
        return word
    for id in members:
        if id.startswith(word):
            return id
    return word

def get_results_dict(scale = True):
    payload = {'apikey': ocr_api_key, 'scale': scale, 'isTable': True,}
    with open(results, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image', files={results: f}, data=payload,)
        text = json.loads(r.content.decode())["ParsedResults"][0]["ParsedText"].splitlines()
        print(text)
        results_dict = {}
        num_players = 0
        for i in range(0, len(text)):
            word_list = text[i].split("\t")
            word = word_list[-2]
            word = word.replace(" ", "", 2)
            # Player Id
            if word.startswith("#") and len(word) <= 6:
                word = word.replace("o", "0").replace("O", "0")
                member = get_member_from_id(word)
                results_dict[member] = get_profit(text[i-2] + text[i-1])
        if get_frequency(None, results_dict.values()) == 1:
            results_dict = deduce_profit_of_none_player(results_dict)
        print(results_dict)
        return(results_dict)

# Convert image to text
results_dict = get_results_dict()
if get_frequency(None, results_dict.values()) != 0 or sum(results_dict.values()) != 0 :
    # Try with scale as False
    results_dict = get_results_dict(False)

# Convert results to splitwise expense
s = Splitwise(consumer_key, consumer_secret)
s.setAccessToken(access_token)
expense = Expense()
expense.setGroupId(group_id)
total = 0
for member in results_dict:
    if not member in members:
        continue
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
    expense.addUser(user1)
expense.setCost(str(total))
date = (datetime.date.today()).strftime("%d %B")
expense.setDescription(date)
expense.setCategory(Category({"id": 20, "name": "Games"}))
expense.setReceipt(results)
nExpense, errors = s.createExpense(expense)
if errors:
    print(errors.getErrors())
else:
    os.remove(results)
