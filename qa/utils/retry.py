import logging

import requests

log = logging.getLogger(__name__)


def get_with_retry(url, attempts=3, timeout=5):
    for _ in range(attempts):
        try:
            return requests.get(url, timeout=timeout)
        except requests.RequestException as exc:
            log.warning("Echec de %s : %s", url, exc)
    return None