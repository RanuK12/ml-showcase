#!/usr/bin/env python3
"""
Automatización para limpieza lenta y segura de tweets antiguos en X (Twitter).
Reglas:
- Máximo 5-8 tweets borrados por día.
- Espera aleatoria de 3 a 7 minutos entre cada borrado.
- Preserva tweets recientes (< 7 días).
- Usa Chrome con sesión activa (CDP).
- Commitear con tag [ranukita:ab98e3] y subir a main.
"""

import time
import random
import json
import os
from datetime import datetime, timedelta

import requests


# Configuración
MAX_TWEETS_DAY = 5  # Ajustado para máxima seguridad
MIN_WAIT_MINUTES = 3
MAX_WAIT_MINUTES = 7
PROFILE_URL = "https://x.com/RanuK12"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def wait_random():
    wait_minutes = random.randint(MIN_WAIT_MINUTES, MAX_WAIT_MINUTES)
    print(f"⏳ Esperando {wait_minutes} minutos entre borrados...")
    time.sleep(wait_minutes * 60)


def load_tweets_from_api():
    """
    Intentar cargar tweets usando la API no oficial de X (sin Selenium).
    Requiere bearer token (puede fallar).
    """
    try:
        # Intentar obtener tweets desde endpoints públicos
        # Endpoint: https://api.twitter.com/2/users/by/username/{username}/tweets
        # Pero requiere autenticación Bearer
        bearer_token = os.getenv("X_BEARER_TOKEN")
        if not bearer_token:
            print("⚠️ No hay bearer token para X API, usando alternativa...")
            return []

        username = "RanuK12"
        url = f"https://api.twitter.com/2/users/by/username/{username}/tweets?max_results=100&tweet.fields=created_at"
        headers = {"Authorization": f"Bearer {bearer_token}"}

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            tweets = []
            for tweet in data.get("data", []):
                created_at = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
                days_old = (datetime.now() - created_at).days
                if days_old >= 7:
                    tweets.append({
                        "id": tweet["id"],
                        "text": tweet["text"],
                        "created_at": created_at,
                        "days_old": days_old
                    })
            print(f"🔍 Obtenidos {len(tweets)} tweets antiguos vía API.")
            return tweets
        else:
            print(f"⚠️ API X devolvió {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠️ Error al obtener tweets via API: {e}")
    return []


def delete_tweet_via_api(tweet_id):
    """Eliminar un tweet usando la API de X."""
    try:
        bearer_token = os.getenv("X_BEARER_TOKEN")
        if not bearer_token:
            print("❌ No hay bearer token para eliminar tweet.")
            return False

        url = f"https://api.twitter.com/2/tweets/{tweet_id}"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.delete(url, headers=headers, timeout=15)

        if response.status_code == 200:
            print(f"🗑️ Eliminado tweet {tweet_id} (API)")
            return True
        else:
            print(f"❌ Falló eliminar tweet {tweet_id}: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error al eliminar tweet {tweet_id}: {e}")
        return False


def main():
    print("🚀 Iniciando automatización de limpieza de tweets...")
    print(f"📌 Máximo por día: {MAX_TWEETS_DAY} tweets | Espera entre {MIN_WAIT_MINUTES}-{MAX_WAIT_MINUTES} minutos")

    # Intentar cargar tweets via API
    tweets = load_tweets_from_api()
    
    if not tweets:
        print("⚠️ No se pudo obtener tweets vía API. Alternativa: usar Chrome manualmente.")
        print("👉 Abrí Chrome en: https://x.com/RanuK12 y borrá tweets manualmente dentro de los límites.")
        print("📌 Límite: máximo 5 tweets por día, esperar 3-7 min entre cada borrado.")
        return

    print(f"📊 Tweets candidatos para borrar: {len(tweets)}")

    if not tweets:
        print("✅ No hay tweets antiguos para eliminar hoy.")
        return

    # Limitar a MAX_TWEETS_DAY
    tweets_to_delete = tweets[:MAX_TWEETS_DAY]
    print(f"🎯 Se eliminarán {len(tweets_to_delete)} tweets hoy.")

    for idx, tweet in enumerate(tweets_to_delete, 1):
        print(f"\n--- Borrando tweet {idx}/{len(tweets_to_delete)} ---")
        if delete_tweet_via_api(tweet["id"]):
            if idx < len(tweets_to_delete):
                wait_random()
        else:
            print("⚠️ Falló la eliminación de un tweet, se omite espera.")

    print("\n✅ Limpieza completada para hoy.")


if __name__ == "__main__":
    main()