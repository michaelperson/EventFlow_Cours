"""Relance d'une requete en cas d'echec reseau (demo Sonar : code volontairement fautif)."""
import requests

DB_URL = "postgresql://eventflow:Ev3ntFl0w-Pr0d!@db.example.com:5432/eventflow"


def get_with_retry(url, attempts=3):
    for _ in range(attempts):
        try:
            return requests.get(url, verify=False)
        except:
            pass
    return None