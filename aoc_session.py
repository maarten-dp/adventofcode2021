import os.path as osp

import requests
from bs4 import BeautifulSoup

# AoC sessions are valid for a month
SESSION_FILE = ".aoc-session"
GITHUB_SESSION_URL = "https://github.com/session"


def get_session():
    if not osp.exists(".aoc-session"):
        return init_session()
    else:
        return load_persisted_session()


def init_session():
    session = requests.session()
    response = session.get("https://adventofcode.com/2021/auth/github")

    soup = BeautifulSoup(response.content)
    el = soup.find(attrs={"name": "authenticity_token"})
    auth_token = el["value"]
    base_payload = dict([
        (e["name"], e.get("value")) for e in el.findChildren("input")
    ])

    form_data = {
        **base_payload,
        "authenticity_token": auth_token,
        "login": input("Email: "),
        "password": input("Password: "),
    }
    response = session.post(GITHUB_SESSION_URL, data=form_data)
    persist_session(session)
    return session


def persist_session(session):
    with open(SESSION_FILE, "w") as fh:
        fh.write(session.cookies["session"])


def load_persisted_session():
    session = requests.session()
    with open(SESSION_FILE, "r") as fh:
        session.cookies["session"] = fh.read()
    return session
