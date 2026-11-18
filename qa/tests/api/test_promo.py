import time

import requests

URL = "http://localhost:8000"


def get_token():
    r = requests.post(
        URL + "/api/auth/token",
        timeout=10,
        data={"username": "admin@eventflow.test", "password": "admin1234"},
    )
    return r.json()["access_token"]


def test_1():
    token = get_token()
    h = {"Authorization": "Bearer " + token}
    r = requests.post(
        URL + "/api/admin/promo",
        headers=h,
        timeout=10,
        json={"code": "TEST" + str(int(time.time())), "percent_off": 20, "max_uses": 5},
    )
    # print(r.json()) #NE jamais mettre de print --> log l'info au besoin
    assert r.status_code == 201


def test_promo2():
    token = get_token()
    h = {"Authorization": "Bearer " + token}
    r = requests.get(URL + "/api/admin/promo", headers=h, timeout=10)
    promos = r.json()
    for p in promos:
        if p["code"] == "WELCOME10":
            assert p["percent_off"] == 10


def test_disable_promo():
    token = get_token()
    h = {"Authorization": "Bearer " + token}
    # try:
    r = requests.post(
        URL + "/api/admin/promo",
        headers=h,
        timeout=10,
        json={"code": "DIS" + str(int(time.time())), "percent_off": 5, "max_uses": 1},
    )
    prom_id = r.json()["id"]
    r2 = requests.post(URL + "/api/admin/promo/" + str(prom_id) + "/disable", headers=h, timeout=10)
    assert r2.json()["expires_at"] != None
    # except:
    #     pass


def test_client_cant_see_promos():
    r = requests.post(
        URL + "/api/auth/token",
        data={"username": "client@eventflow.test", "password": "client1234"},
        timeout=10,
    )
    token = r.json()["access_token"]
    r = requests.get(
        URL + "/api/admin/promo", timeout=10, headers={"Authorization": "Bearer " + token}
    )
    assert r.status_code == 403


def test_lol():
    token = get_token()
    h = {"Authorization": "Bearer " + token}
    # try:
    r = requests.post(
        URL + "/api/admin/promo",
        timeout=10,
        headers=h,
        json={"code": "DIS" + str(int(time.time())), "percent_off": 5, "max_uses": 1},
    )
    prom_id = r.json()["id"]
    r2 = requests.post(URL + "/api/admin/promo/" + str(prom_id) + "/disable", headers=h, timeout=10)
    assert r2.json()["expires_at"] != None
    # except:
    #   pass
