import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def nfldictionary():
    page = requests.get("http://www.espn.com/nfl/players")
    soup = BeautifulSoup(page.content, 'html.parser')
    teams = soup.find(id="my-players-table")
    rosters = teams.find_all("div", style="float:left;")
    teamnames = [x.get_text() for x in rosters]
    
    x = []
    for a in teams.find_all('a', href=True):
        x.append("http://www.espn.com" + a['href'])

    matchwebsites = []
    for i in x:
        if len(re.findall(r".*roster.*", i)) > 0:
            matchwebsites.append(re.findall(r".*roster.*", i)[0])
    namewebsite = {teamnames[i]: matchwebsites[i]
                   for i in range(len(teamnames))}
    return namewebsite


def getplayers(website):
    page = requests.get(str(website))
    soup = BeautifulSoup(page.content, 'html.parser')
    offenseplayerstable = soup.find(class_="Offense")
    offensenames1 = offenseplayerstable.find_all("a", class_="AnchorLink")
    offensenames2 = [e.get_text() for e in offensenames1]
    offensenames3 = []
    for i in offensenames2:
        if len(re.findall(r".*\s.*", i)) > 0:
            offensenames3.append(re.findall(r".*\s.*", i)[0])

    offensex = []
    for a in offenseplayerstable.find_all('a', href=True):
        offensex.append(a['href'])
    offensematchwebsites = []
    for i in offensex:
        if len(re.findall(r".*id.*", i)) > 0:
            offensematchwebsites.append(re.findall(r".*id.*", i)[0])
    offenseplayerstats = [*set(offensematchwebsites)]

    defplayerstable = soup.find(class_="Defense")
    defnames1 = defplayerstable.find_all("a", class_="AnchorLink")
    defnames2 = [e.get_text() for e in defnames1]
    defnames3 = []
    for i in defnames2:
        if len(re.findall(r".*\s.*", i)) > 0:
            defnames3.append(re.findall(r".*\s.*", i)[0])
    defx = []
    for a in defplayerstable.find_all('a', href=True):
        defx.append(a['href'])
    defmatchwebsites = []
    for i in defx:
        if len(re.findall(r".*id.*", i)) > 0:
            defmatchwebsites.append(re.findall(r".*id.*", i)[0])
    defplayerstats = [*set(defmatchwebsites)]

    stplayerstable = soup.find(class_="Special")
    stnames1 = stplayerstable.find_all("a", class_="AnchorLink")
    stnames2 = [e.get_text() for e in stnames1]
    stnames3 = []
    for i in stnames2:
        if len(re.findall(r".*\s.*", i)) > 0:
            stnames3.append(re.findall(r".*\s.*", i)[0])
    stx = []
    for a in stplayerstable.find_all('a', href=True):
        stx.append(a['href'])
    stmatchwebsites = []
    for i in stx:
        if len(re.findall(r".*id.*", i)) > 0:
            stmatchwebsites.append(re.findall(r".*id.*", i)[0])
    stplayerstats = [*set(stmatchwebsites)]

    websiteplayerstats = offenseplayerstats + defplayerstats + stplayerstats
    allplayernames = offensenames3 + defnames3 + stnames3

    
    playerdictionary = {}
    for i in allplayernames:
        for j in websiteplayerstats:
            test = i.lower()
            test2 = test.split()
            helper = re.findall(rf".*{test2[0]}[-]?{test2[1]}.*", j)
            if len(helper) > 0:
                playerdictionary[i] = j

    return playerdictionary


def getstats(website):
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')
    htmlstats = soup.find(class_="Card PlayerStats")
    if htmlstats == None:
        print("This player has no stats!")
    else:
        stats = htmlstats.find_all("td")
        table = htmlstats.find_all("th")

        table2 = [x.getText() for x in table]
        stats2 = [x.getText() for x in stats]
        seasons = []
        for i in range(3):
            seasons.append(stats2[i])
        for i in range(3):
            stats2.pop(0)
        seasons.insert(0, table2[0])
        table2.pop(0)

        statistics = {seasons[0]: [seasons[x] for x in range(1, 4)]}

        for x in table2:
            index = table2.index(x)
            statistics[x] = [stats2[i]
                            for i in (index, index + len(table2), index + (len(table2)*2))]

   
        statstable = pd.DataFrame(statistics)
        print(statstable)




while True:
    team = input("Team? ")
    teamwebsite = nfldictionary()[team]
    if teamwebsite != None:
        player = input("Name of Player? ")
        playerwebsite = getplayers(teamwebsite)
        if playerwebsite[player] != None:
            x = playerwebsite[player]

            getstats(x)



