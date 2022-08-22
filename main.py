# Librairie(s)
from datetime import datetime, timedelta
import requests

# Module(s)
from configuration import APP_CONFIG
from leo_class import Leo
from safe_actions import dprint

def Telegram_bot_sendtext(bot_message):
    bot_token = APP_CONFIG.TOKEN
    bot_chatID = APP_CONFIG.CHATID
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    response = requests.post(send_url, json={'chat_id': bot_chatID, 'text': bot_message})
    dprint("A Telegram notification has just been sent !", priority_level=6)
    return response.json()


dprint("Run notif presence script !", priority_level=1)
dprint("The leo web page is loading", priority_level=2)
web = Leo()
dprint("The leo object is ready to be used", priority_level=3)
dprint("\n", hashtag_display=False)

while True:
    dprint("Get current date:", priority_level=2)
    now = [
        int(datetime.today().strftime("%H")),
        int(datetime.today().strftime("%M"))
    ]
    delta_now = [
        int((datetime.today() + timedelta(minutes=10)).strftime("%H")),
        int((datetime.today() + timedelta(minutes=10)).strftime("%M"))
    ]
    dprint(f"Current date {now[0]}h{now[1]}", priority_level=3)
    dprint(f"Delta date (date + 10min) {delta_now[0]}h{delta_now[1]}", priority_level=3)

    dprint("Refresh web page infos", priority_level=2)
    web.refresh()

    dprint("Inspect classes", priority_level=2)
    if web.day_infos["remaining_classes"]:
        dprint("Classes are coming ! Let's check them", priority_level=3)

        if web.day_infos["next_classe_start"][0] <= delta_now[0] and \
                web.day_infos["next_classe_start"][1] <= delta_now[1]:

            dprint("A classe is currently taking place", priority_level=4)

            if web.check_register():
                dprint("The register is open !", priority_level=5)
                classe_infos = web.day_infos["list_of_day_classes_infos"][web.day_infos["current_classe_index"]]

                # Notif
                alert_msg = f"#--- APPEL ---#\n" \
                            f"#- Cours :\n" \
                            f"#-- {classe_infos['name']}\n\n" \
                            f"#- Lien présence :\n" \
                            f"#-- {web.FireFox.current_url}\n\n" \
                            f"#- Lien ZOOM :\n" \
                            f"#-- {classe_infos['ZOOM_link']}\n\n"

                while True:
                    try:
                        Telegram_bot_sendtext(alert_msg)
                        break
                    except: pass

                web.next_classe()

            else:
                dprint("The register is not open", priority_level=5)
            web.FireFox.back()

        elif web.day_infos["next_classe_end"][0] <= now[0] and \
                web.day_infos["next_classe_end"][1] < now[1]:
            dprint("No classes are currently taking place", priority_level=4)
            web.next_classe()

    dprint("\n", hashtag_display=False)
