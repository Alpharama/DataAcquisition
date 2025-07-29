import time
import os
import json
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from utils import get_last_boosted_tokens, get_pairs_by_token

seen_tokens = []
tokens_to_look = []
threshold_times = {}

def run():
    print(f"🚀 Lancement du pipeline à {datetime.now()}")

    boosted_tokens = get_last_boosted_tokens()
    if len(boosted_tokens) == 0:
        print("⚠️ Aucun token boosté trouvé.")
        return

    results = []
    for token_data in tqdm(boosted_tokens):
        token = {'chainId': token_data['chainId'], 'tokenAddress': token_data['tokenAddress']}
        token_tuple = (token_data['chainId'], token_data['tokenAddress'])

        if token_tuple in tokens_to_look:
            if threshold_times[token_tuple] < int(time.time() * 1000) + 24 * 60 * 60 * 1000:
                try:
                    pair_data = get_pairs_by_token(token)
                    if pair_data:
                        results.append(pair_data)
                except Exception as e:
                    print(f"❌ Erreur lors de la récupération des paires : {e}")
            else:
                tokens_to_look.remove(token_tuple)
        else:
            if token_tuple not in seen_tokens:
                try:
                    pair_data = get_pairs_by_token(token)
                    if pair_data:
                        threshold_times[token_tuple] = pair_data['pairCreatedAt']
                        if threshold_times[token_tuple] < int(time.time() * 1000) + 24 * 60 * 60 * 1000:
                            results.append(pair_data)
                            tokens_to_look.append(token_tuple)
                            seen_tokens.append(token_tuple)
                except Exception as e:
                    print(f"❌ Erreur lors de la récupération des paires : {e}")

    if results:
        print(f"✅ Données sauvegardées ({len(results)} tokens)")
    else:
        print("⚠️ Aucun résultat à sauvegarder.")

    timestamp = int(time.time() * 1000)
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"results_{timestamp}.json")
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"💾 Résultats sauvegardés dans '{file_path}'")


if __name__ == "__main__":
    run()
