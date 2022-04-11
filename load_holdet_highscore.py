import time
import pandas as pd
import numpy as np
import unidecode
from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup

output_folder = Path(__file__).parent

def load_holdet_highscore_data(run, Liga_all, n_pages):
    URL_all = ["https://www.holdet.dk/da/premier-league-fantasy-spring-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/la-liga-fantasy-spring-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/bundes-fantasy-spring-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/super-manager-spring-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/serie-a-fantasy-spring-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/champions-manager-2021-2022/leaderboards/praemiepuljen",
               "https://www.holdet.dk/da/champions-manager-knockout-2022/leaderboards/praemiepuljen"]

    URL_team_all = ["https://www.holdet.dk/da/premier-league-fantasy-spring-2022/userteams/",
               "https://www.holdet.dk/da/la-liga-fantasy-spring-2022/userteams/",
               "https://www.holdet.dk/da/bundes-fantasy-spring-2022/userteams/",
               "https://www.holdet.dk/da/super-manager-spring-2022/userteams/",
               "https://www.holdet.dk/da/serie-a-fantasy-spring-2022/userteams/",
               "https://www.holdet.dk/da/champions-manager-2021-2022/userteams/",
               "https://www.holdet.dk/da/champions-manager-knockout-2022/userteams/"]


    URL = URL_all[run[0] - 1]

    Liga_all.append("88. Champions League Knockout")
    driver_path = Path(__file__).parent / "chromedriver"
    driver = webdriver.Chrome(executable_path=str(driver_path))
    driver.get(URL)
    driver.maximize_window()

    time.sleep(4.0)
    cookie_buttons = driver.find_elements_by_class_name("CybotCookiebotDialogBodyButton")
    for button in cookie_buttons:
        if button.text == "TILLAD ALLE":
            button.click()
            break
    time.sleep(3)

    html_list = []
    html_list_liga = []

    for idx, item in enumerate(run):
        Liga = Liga_all[idx]
        for i in range(n_pages):
            buttons = driver.find_elements_by_class_name("all")[4::2]
            for idx1, item1 in enumerate(buttons):
                buttons = driver.find_elements_by_class_name("all")[4::2]
                buttons[idx1].click()
                time.sleep(1)
                check1 = driver.find_elements_by_class_name("StyledDynamicComponent-sc-198zoyl-0-div.cUSjfJ")
                if len(check1) == 0:
                    time.sleep(1)
                    html_list.append(driver.page_source)
                else:
                    team = buttons[idx1].text.replace('.', '_').replace(' ', '_').replace('’', '_').replace('æ', 'ae'). \
                        replace('ø', 'oe').replace('å', 'aa').replace('Æ', 'ae').replace('Ø', 'oe').replace('Å', 'aa'). \
                        replace(',', '_').replace('!', '').replace('/', '_').replace('-', '_').replace("'", '_'). \
                        replace('´', '_').replace('&', '').replace('%', '').replace('#', '').replace('—', ''). \
                        replace('>', '_').replace('…', '').replace('$', '_').replace('@', '').replace('€', '').replace('__', '_').replace('__', '_')  #
                    team = unidecode.unidecode(team)
                    if right(team, 1) == "_":
                        team = team[:-1]
                    URL_team = URL_team_all[idx] + team
                    driver.get(URL_team)
                    time.sleep(1.5)
                    check = driver.find_elements_by_class_name("byline")
                    if len(check) > 0:
                        html_list.append(driver.page_source)
                    else:
                        html_list.append("ERROR, team: " + URL_team)
                html_list_liga.append(Liga)
                driver.back()
                time.sleep(1.5)
            if i+1 < n_pages:
                driver.find_elements_by_class_name('arrow')[1].click()
        if idx+1 < len(URL_all):
            URL = URL_all[idx+1]
            driver.get(URL)
            time.sleep(0.5)

    driver.quit()

    di = {'manager': [], 'rank': [], 'Kaptajn': [], 'bankbeholdning': [], 'liga': []}
    for idx, item in enumerate(html_list):
        if left(html_list, 5) != "ERROR":
            soup = BeautifulSoup(item, 'html.parser')
            manager_data = soup.findAll(True, {"byline"})[1]
            values = soup.findAll(True, {"default tradesearchres compact"})
            team_data = soup.findAll(True, {"soccer wrapper field view sport-soccer"})[0].contents[2].contents[2].contents
            spillere = team_data[1:12]
            for idx1, item1 in enumerate(spillere):
                c_check = len(item1.contents[2].contents[0].attrs)
                if c_check == 1:
                    di["Kaptajn"].append(item1.contents[3].contents[0].contents[0].contents[1].contents[0].contents[0].contents[0].contents[0].contents[1].text)
            di["manager"].append(manager_data.contents[3].text)
            di["rank"].append(int(manager_data.contents[6].split("\n")[0].split(" ")[1].replace('.', '')))
            di["bankbeholdning"].append(int(values[0].contents[1].contents[2].contents[2].text.split(" kr")[0].replace('.','')))
            di["liga"].append(html_list_liga[idx])
        else:
            di["Kaptajn"].append("fejl")
            di["manager"].append(html_list[idx])
            di["rank"].append("fejl")
            di["bankbeholdning"].append("fejl")
            di["liga"].append(html_list_liga[idx])
        print(idx)


    df = pd.DataFrame(di)

    csv_name_G = "holdet_highscore.csv"
    df.to_csv(str(output_folder) + '/data/' + csv_name_G, index=False, header=True, encoding='utf-8-sig')
    print("Holdet - Hold hentet")
    return

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset + amount]

