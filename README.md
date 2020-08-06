# pokerrrr2_to_splitwise
Converts pokerrr2 game screenshot to a splitwise expense on android

# Docs
https://github.com/namaggarwal/splitwise

# Deps
Install qpython3 app from playstore https://play.google.com/store/apps/details?id=org.qpython.qpy3 (you can use any other python engine)\
Install splitwise package :\
$ pip install splitwise\

# Edit the following paramters before running:
Register and generate keys for splitwise https://secure.splitwise.com/oauth_clients \
consumer_key = "<obfuscated>"\
consumer_secret = "<obfuscated>"\
\
Generate oauth1 token using https://splitwise.readthedocs.io/en/latest/user/authenticate.html\
oauth_token = "<obfuscated>"\
oauth_token_secret = "<obfuscated>"\
access_token = {'oauth_token': "<obfuscated>", 'oauth_token_secret': "<obfuscated>"}\
\
Splitwise group id e.g. "192136318"\
group_id = "192136318"\
\
Create member dictionary of {member_id_pokerrr2: member_id_splitwise} e.g. {"#AB0X7": 6167766}\
members = {"#AB0X7": 6167766}\
\
Generate OCR API Key at https://ocr.space/OCRAPI "Register here for your free OCR API key"\
ocr_api_key = '<obfuscated>'\
