# -*- coding: utf-8 -*-
import time

import requests

from Util.Logger import logger
from Util.SettingsReader import read_authentication, read_config
from Vortex.Trainer import Trainer
from Util.Translation import translation
import re

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class http_wrapper():
    """Http Class"""

    def __init__(self):
        self.s = requests.session()
        self.a = read_authentication()
        self.c = read_config()
        self.l = logger()
        self.trainer = Trainer()
        self.tl = translation()

    @property
    def do_login(self):
        try:
            self.l.writelog(self.tl.getLanguage("logining"), "info")
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/checklogin.php"
            data = {"myusername": self.a["Username"], "mypassword": self.a["Password"]}
            r = self.s.post(url, data)
            if "dashboard" in str(r.url):
                self.l.writelog(self.tl.getLanguage("loginSuccess"), "info")
            else:
                self.l.writelog(self.tl.getLanguage("loginFailed"), "error")
            return True
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(5)
            self.do_login()

    def start_bot(self):
        try:
            self.select_battle()
            self.start_battle()
        except Exception as e:
            self.l.writelog(str(e), "critical")
            time.sleep(5)
            self.do_login()

    def select_battle(self):
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle_select.php?type=member"
            data = {"battle": "Username", "buser": self.c["Traniner"], "submitb": "Battle!"}
            r = self.s.post(url, data)
            self.l.writelog(self.tl.getLanguage("battleSelected"), "info")
            ph = BeautifulSoup(r.text, "html.parser")
            active_pokemon = ph.find('input', attrs={'name': 'active_pokemon', 'type': 'radio', 'checked': 'checked'})

            if active_pokemon is None:
                self.l.writelog(self.tl.getLanguage("nonePokemonSelected"), "info")
            else:
                active_pokemon = active_pokemon["value"]

            self.l.writelog("Active pokemon : " + active_pokemon, "info")
            nojssolvea = ph.find('input', attrs={'id': 'nojs-solve-a'})
            nojssolveb = ph.find('input', attrs={'id': 'nojs-solve-b'})
            if (nojssolvea is not None and nojssolveb is not None):
                self.l.writelog("no-js-solve-a : " + nojssolvea["value"], "info")
                self.l.writelog("no-js-solve-b : " + nojssolveb["value"], "info")
                nojscheck = int(nojssolvea["value"]) + int(nojssolveb["value"])
                self.l.writelog("no-js-check : " + str(nojscheck), "error")
            else:
                self.l.writelog(self.tl.getLanguage("jsQuestionsNotFound"), "error")
            self.nojscheck = str(nojscheck)
            self.active_pokemon = str(active_pokemon)
        except Exception as e:
            self.l.writelog(str(e), "critical")

    def start_battle(self):
        try:
            url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
            data = {"active_pokemon": self.active_pokemon, "action": "select_attack", "": "", "": "",
                    "nojs-check": self.nojscheck}
            r = self.s.post(url, data)
            self.l.writelog(self.tl.getLanguage("battleStarted"), "info")
            while(True):
                if("has fainted" in r.text):
                    data = {"choose": "pokechu"}
                    r = self.s.post(url, data)
                    self.l.writelog(self.tl.getLanguage("won"), "info")
                    if ("You won the battle" not in r.text):
                        url = "http://" + self.a["Server"] + ".pokemon-vortex.com/battle.php?&ajax=1"
                        data = {"active_pokemon": self.active_pokemon, "action": "select_attack"}
                        r = self.s.post(url, data)
                        self.l.writelog(self.tl.getLanguage("reselectPokemon"), "info")
                else:
                    time.sleep(self.c["SleepSecondsAfterBattle"])
                    if ("You won the battle" in r.text):
                        self.l.writelog(self.tl.getLanguage("battleWon"), "info")
                        time.sleep(self.c["SleepSecondsAfterAttack"])
                        self.start_bot()
                        break
                    else:
                        data = {"attack": "1", "action": "attack"}
                        r = self.s.post(url, data)
                        self.l.writelog(self.tl.getLanguage("notWon"), "info")

        except Exception as e:
            self.l.writelog(str(e), "critical")
