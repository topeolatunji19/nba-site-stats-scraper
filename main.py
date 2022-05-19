from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import pandas as pd

chrome_driver_path = "/Users/Temitope/Development Tools/chromedriver"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://www.nba.com/stats/leaders/")
time.sleep(5)

final_player_list = []
header_list = []


# Accessing and sorting all the data
def get_table_data():
    global header_list
    player_stats = driver.find_elements(by=By.CSS_SELECTOR, value='.nba-stat-table__overflow table tr')
    player_stats_list = [player_stat.text for player_stat in player_stats]
    # print(player_stats_list)

    new_list = []
    for stat in player_stats_list:
        new_item = stat.split(" ")
        new_list.append(new_item)

    header_list = new_list[0][1:]
    # print(header_list)

    for player_data in new_list[1:]:
        # To sort player names with more than 2 strings i.e length of 21 means the player has just 2 name on the site
        if len(player_data) == 21:
            player_data[0:2] = [' '.join(player_data[0:2])]
        else:
            player_data[0:3] = [' '.join(player_data[0:3])]
        # print(player_data)
        player_details = player_data[0].split("\n")
        # print(player_details)
        player_data[0] = player_details[1]
        # print(player_details)
        try:
            player_data.insert(1, player_details[2])
        except IndexError:
            player_data.insert(1, driver.find_element(by=By.XPATH,
                                                      value=f'/html/body/main/div/div/div[2]/div/div/nba-stat-table'
                                                            f'/div[2]/div[1]/table/tbody/'
                                                            f'tr[{player_details[0]}]/td[3]').text)
        final_player_list.append(player_data)


# Accept cookies
cookie = driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
cookie.click()
time.sleep(2)

get_table_data()
time.sleep(2)

# To get the data for the 3 other pages
for x in range(3):
    try:
        next_page = driver.find_element(by=By.XPATH,
                                        value='/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]')
        next_page.click()
    except NoSuchElementException:
        break
    else:
        get_table_data()

player = [player[0] for player in final_player_list]
gp = [player[1] for player in final_player_list]
minute = [player[2] for player in final_player_list]
pts = [player[3] for player in final_player_list]
fgm = [player[4] for player in final_player_list]
fga = [player[5] for player in final_player_list]
fgper = [player[6] for player in final_player_list]
threepm = [player[7] for player in final_player_list]
threepa = [player[8] for player in final_player_list]
threepper = [player[9] for player in final_player_list]
ftm = [player[10] for player in final_player_list]
fta = [player[11] for player in final_player_list]
ftper = [player[12] for player in final_player_list]
oreb = [player[13] for player in final_player_list]
dreb = [player[14] for player in final_player_list]
reb = [player[15] for player in final_player_list]
ast = [player[16] for player in final_player_list]
stl = [player[17] for player in final_player_list]
blk = [player[18] for player in final_player_list]
tov = [player[19] for player in final_player_list]
eff = [player[20] for player in final_player_list]

player_data_list = [player, gp, minute, pts, fgm, fga, fgper, threepm, threepa, threepper, ftm, fta, ftper, oreb, dreb,
                    reb, ast, stl, blk, tov, eff]

stats_dict = dict(zip(header_list, player_data_list))
# print(stats_dict)

nba_player_stats_data = pd.DataFrame(stats_dict)

nba_player_stats_data.to_csv("nba-player-stats.csv")
