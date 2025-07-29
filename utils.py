import requests
import pandas as pd

def get_last_tokens():
    url = "https://api.dexscreener.com/token-profiles/latest/v1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une erreur si status != 200
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête : {e}")
        return pd.DataFrame()

def get_last_boosted_tokens():
    url = "https://api.dexscreener.com/token-boosts/latest/v1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une erreur si status != 200
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête : {e}")
        return pd.DataFrame()
    
def get_most_boosted_tokens():
    url = "https://api.dexscreener.com/token-boosts/top/v1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une erreur si status != 200
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête : {e}")
        return pd.DataFrame()
    


def get_pairs_by_token(token):
    chainId = token['chainId']
    tokenAddress = token['tokenAddress']  # attention au nom, c’est pas tokenAdresses au pluriel ?
    url = f"https://api.dexscreener.com/tokens/v1/{chainId}/{tokenAddress}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[0]

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête : {e}")
        return {}
