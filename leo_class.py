# Librairie(s)
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
# Module(s)
from configuration import APP_CONFIG
from safe_actions import dprint

class Leo:
    email = APP_CONFIG.EMAIL
    password = APP_CONFIG.MDP
    base_url = APP_CONFIG.URL
    FireFox = webdriver.Firefox(executable_path=APP_CONFIG.DRIVER_LOCATION)

    day_infos = {
        "list_of_day_classes": list(),
        "list_of_day_classes_infos": list(),
        "current_classe_index": int(),
        "remaining_classes": bool(),
        "next_classe_start": [int(), int()],
        "next_classe_end": [int(), int()]
    }

    # Cheminement vers les releves de presence (Connexion, ...)
    def __init__(self):
        # Connexion login page
        self.FireFox.get(self.base_url)

        # Remplissage email
        balise_identifiant = self.FireFox.find_element(By.ID, "login")
        balise_identifiant.send_keys(self.email)

        # Next page
        balise_suivant = self.FireFox.find_element(By.ID, "btn_next")
        balise_suivant.click()

        # Remplissage password
        balise_password = self.FireFox.find_element(By.ID, "passwordInput")
        balise_password.send_keys(self.password)

        # Connexion
        balise_connexion = self.FireFox.find_element(By.ID, "submitButton")
        balise_connexion.click()

        # Go to "Relevés de présence"
        self.FireFox.implicitly_wait(5)
        balises_a = self.FireFox.find_elements(By.TAG_NAME, "a")

        for index, a in enumerate(balises_a):
            if(a.text == "Relevés de présence"):
                a.click()
                break

        self.day_infos["remaining_classes"] = False
        self.day_infos["current_classe_index"] = -1

    def next_classe(self):
        if len(self.day_infos["list_of_day_classes"]) > 0 and (self.day_infos["current_classe_index"] + 1) < len(self.day_infos["list_of_day_classes"]):
            self.day_infos["current_classe_index"] += 1
        else:
            self.day_infos["current_classe_index"] = -1


    def _get_classes(self) -> list():
        def __get_classe_infos(classe) -> dict():
            # 0 -> schedule | 1 -> name | 2 -> prof | 3 -> btn | 4 -> ZOOM's link
            infos = classe.find_elements(By.TAG_NAME, "td")

            schedule = infos[0].text.split(" -")
            # TODO: erreur ici peut etre format de l'heure %H:%M
            start = [int(schedule[0].split(":")[0]), int(schedule[0].split(":")[1])]
            end = [int(schedule[1].split(":")[0]), int(schedule[1].split(":")[1])]

            return {
                "start": start,
                "end": end,
                "name": infos[1].text,
                "prof": infos[2].text,
                "btn": infos[3],
                "ZOOM_link": infos[4].text
            }

        classes = self.FireFox.find_element(By.ID, "body_presences")
        self.day_infos["list_of_day_classes"] = classes.find_elements(By.TAG_NAME, "tr")
        if len(self.day_infos["list_of_day_classes"]) > 0:
            self.day_infos["current_classe_index"] = 0

            classes_infos = list()
            for classe in self.day_infos["list_of_day_classes"]:
                classes_infos.append(
                    __get_classe_infos(classe)
                )
            self.day_infos["list_of_day_classes_infos"] = classes_infos

        else:
            self.day_infos["current_classe_index"] = -1

    def refresh(self):
        # Refresh list_of_day_classes
        if self.day_infos["remaining_classes"] is False:
            now = [int(datetime.now().strftime("%H")), int(datetime.now().strftime("%M"))]
            # If we are between [00h00 and 00h01[
            if now[0] == 0 and now[1] == 0:
                self.FireFox.refresh()
                self._get_classes()
                # Wait 00h01
                while now[0] == 0 and now[1] == 0:
                    pass

        # Refresh remaining_classes
        if self.day_infos["current_classe_index"] in [
            -1,
            len(self.day_infos["list_of_day_classes"]) - 1,
        ]:
            self.day_infos["remaining_classes"] = False
        else:
            self.day_infos["remaining_classes"] = True

        if self.day_infos["remaining_classes"]:
            # Refresh next classe start and end
            next_classe_start = self.day_infos["list_of_day_classes_infos"][
                self.day_infos["current_classe_index"]
            ]["start"]
            next_classe_end = self.day_infos["list_of_day_classes_infos"][
                self.day_infos["current_classe_index"]
            ]["end"]

    def check_register(self) -> bool():
        # Click on the classe to see if the register is open
        self.day_infos["list_of_day_classes_infos"][self.day_infos["current_classe_index"]]["btn"].find_element(By.TAG_NAME, "a").click()
        return self.FireFox.find_element(By.ID, "body_presence").text != "L'appel n'est pas encore ouvert."






