import krakenex
import pprint
import json
import sys
data = {}


def keyWizard():
    global data
    data['krakenAPIKey'] = input("Please enter your API key: ")
    data['krakenAPISecret'] = input("Please enter your secret key: ")
    with open('secrets.json', 'w') as f:
        json.dump(data, f)


# JSON API key and secret values imported from a seperate file and turned into a dictionary
try:
    with open('secrets.json') as f:
        data = json.load(f)
except FileNotFoundError:
    confirmMessage = input("Secrets file not found. Would you like to start the secrets file creation wizard? (y/n) ")
    while confirmMessage != "y" and confirmMessage != "n":
        confirmMessage = input()

    if confirmMessage == "y":
        keyWizard()
    elif confirmMessage == "n":
        print("Goodbye!")
        sys.exit()

# values of krakenAPIKey and krakenAPISecret taken from the dictionary and stored in variables:
krakenAPIKey = data["krakenAPIKey"]
krakenAPISecret = data["krakenAPISecret"]

# Holds the API key and secret key for Kraken account. Read only API key, less security danger

k = krakenex.API(key= krakenAPIKey, secret= krakenAPISecret)

# balance returns a dictionary of values for all currencies held in portfolio
try:
    balance = k.query_private('Balance')['result']
except KeyError:
    print("There was a problem with your access keys.")
    sys.exit()
except:
    print("Failed to recieve response from Kraken. Please check your connection.")
    sys.exit()

# portfolio_EUR stores the value of the EUR amount currently in Balance
portfolio_EUR = float(balance.get('ZEUR'))
# portfolio_Ethereum stores the number of Eth currently in Balance
portfolio_Ethereum = float(balance.get('XETH'))

# stores a number of different current values for Ethereum:
# <pair_name> = pair name
#     a = ask array(<price>, <whole lot volume>, <lot volume>),
#     b = bid array(<price>, <whole lot volume>, <lot volume>),
#     c = last trade closed array(<price>, <lot volume>),
#     v = volume array(<today>, <last 24 hours>),
#     p = volume weighted average price array(<today>, <last 24 hours>),
#     t = number of trades array(<today>, <last 24 hours>),
#     l = low array(<today>, <last 24 hours>),
#     h = high array(<today>, <last 24 hours>),
#     o = today's opening price
eth_Price = k.query_public('Ticker', {'pair': 'ETHEUR'})

# grabs the current Ethereum value from eth_Price
current_Ethereum_Price = float(eth_Price.get('result').get('XETHZEUR').get('a')[0])

# calculates the current balance of Eth + Eur
total_Crypto_Balance = portfolio_EUR + (portfolio_Ethereum * current_Ethereum_Price)

pprint.pprint(total_Crypto_Balance)
pprint.pprint(current_Ethereum_Price)

# TODO
# Use API to get current value of S&P500 ETF
