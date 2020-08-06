# pokerrrr2_to_splitwise
Converts pokerrr2 game screenshot to a splitwise expense on android

## Docs
https://github.com/namaggarwal/splitwise

## Deps
Install qpython3 app from playstore https://play.google.com/store/apps/details?id=org.qpython.qpy3 (you can use any other python engine)\
Install splitwise package :\
$ pip install splitwise

## Edit the following paramters before running:
#### Register and generate keys for splitwise https://secure.splitwise.com/oauth_clients
consumer_key = ""
\
consumer_secret = ""

#### Generate oauth1 token using https://splitwise.readthedocs.io/en/latest/user/authenticate.html
s = Splitwise(consumer_key, consumer_secret)
\
url, oauth_token_secret = s.getAuthorizeURL()
\
Login to splitwise in a browser, run above url in the browser and authorize access to your account
\
You will find a oauth_verifier after you authorize the account "Click to show out of band authentication information"
\
oauth_verifier = ""
\
Take oauth_token from authorize url query parameter
\
access_token = s.getAccessToken(oauth_token, oauth_token_secret, oauth_verifier)
\
save this access_token for future re-use access_token = {'oauth_token': '', 'oauth_token_secret': ''}

#### Splitwise group id e.g. "192136318"
group_id = "192136318"

#### Create member dictionary of {member_id_pokerrr2: member_id_splitwise} e.g. {"#AB0X7": 6167766, "#X4S0D": 31283953}
members = {"#AB0X7": 6167766, "#X4S0D": 31283953}

#### Generate OCR API Key at https://ocr.space/OCRAPI "Register here for your free OCR API key"
ocr_api_key = ""
