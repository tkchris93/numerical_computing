"""Volume III: Web Scraping 1.
<Name>
<Class>
<Date>
"""

from bs4 import BeautifulSoup
import urllib2
import re
import numpy as np
from matplotlib import pyplot as plt
import sqlite3 as sql
from selenium import webdriver

# Problem 1
def Prob1():
    """Load the Big Bank Info file and return a 2-D numpy array
    containing Bank Name, Rank, ID, Domestic Assets, and Domestic Branches
    for JP Morgan, Capital One, and Discover banks.
    """
    # Create BeautifulSoup object
    soup = BeautifulSoup(open('Big_Bank_Info.htm'), 'html.parser')
    # Initialize array with column names
    A = np.array([['Bank Name', 'Rank', 'ID', 'Domestic Assets', 'Domestic Branches']])
    # Create dictionary of how many calls to next_sibling for each attribute
    d = {'Bank Name': 0, 'Rank': 1, 'ID': 2, 'Domestic Assets': 6, 'Domestic Branches': 9}
    # Create list of strings to search for
    banks = ['JPMORGAN', 'CAPITAL ONE', 'DISCOVER']
    for bank in banks:
        # Initialize next row
        B = np.zeros_like(A[0])
        for i, attr in enumerate(A[0]):
            # Finds the bank name
            data = soup.find(string=re.compile(bank))
            # Move to next piece of information
            for _ in xrange(d[attr]):
                data = data.parent.parent.next_sibling.span.next_sibling
            # Adds information to row
            B[i] = data
        A = np.vstack((A,b))
    return A

# Problem 2
def Prob2():
    """Use urllib2 and BeautifulSoup to return the actual max temperature,
    the tag containing the link for 'Next Day', and the url associated
    with that link.
    """
    # Read into BeautifulSoup
    url = "http://www.wunderground.com/history/airport/KSAN/2015/1/1/DailyHistory.html?req_city=San+Diego&req_state=CA&req_statename=California&reqdb.zip=92101&reqdb.magic=1&reqdb.wmo=99999&MR=1"
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    # Find and store information
    actual_max_temp = soup.table.find(string="Max Temperature").parent.parent.next_sibling.next_sibling.span.span.contents[0]
    tag = soup.find(string=re.compile('Next Day')).parent
    ref = tag['href']
    return int(actual_max_temp), tag, ref

# Problem 3
def Prob3():
    """Mimic the Wunderground Weather example to create a list of average
    max temperatures of the year 2014 in San Diego. Use matplotlib to draw
    a graph depicting the data, then return the list.
    """
    # Edited code from example
    weather_url = 'https://www.wunderground.com/history/airport/KSAN/2014/1/1/DailyHistory.html'
    weather_content = urllib2.urlopen(weather_url).read()
    weather_soup = BeautifulSoup(weather_content)
    average = []

    while ('2015' not in weather_soup.find(class_='history-date').string):
        while(len(weather_soup.find_all(string='Average ')) != 1):
            weather_content = urllib2.urlopen(weather_url).read()
            weather_soup = BeautifulSoup(weather_content)
        average_temp = weather_soup.find(string='Max Temperature').parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.span.span.text
        average.append(int(average_temp))
        next_url = weather_soup.find(string=re.compile('Next Day')).parent['href']
        weather_url = 'https://www.wunderground.com' + next_url
        weather_content = urllib2.urlopen(weather_url).read()
        weather_soup = BeautifulSoup(weather_content)
    # Plot the data
    plt.plot(average)
    plt.xlabel("Day")
    plt.ylabel("Average Max Temperature")
    plt.show()
    # Return the list
    return average

# Problem 4
def Prob4():
    """Load the selected option into BeautifulSoup. Find the requested
    information for the selected option and make a SQL table that
    stores this information.

    Note for solutions file:
        The following code gives a possible outline for each of the three
        possible options. Because the options are all current websites that
        could change format without notice, there is no way to guarantee
        that it will compile properly in the future, but it should give a
        good idea of how to implement the function.
    """
    # Create location for tables
    db = sql.connect("prob4")
    cur = db.cursor()

    # Option 1 (Financial Data)
    # Create table and list all sectors
    cur.execute('CREATE TABLE Finance (Name TEXT, Abbrev TEXT, PerChange TEXT, MktCap REAL);')
    sectors = ['Energy', 'Basic Materials', 'Industrials', 'Cyclical Cons. Goods ...', 'Non-Cyclical Cons. Goods...', 'Financials', 'Healthcare', 'Technology', 'Telecommunications Servi...', 'Utilities']
    # Create BeautifulSoup object
    url = 'https://www.google.com/finance'
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    # Initialize rows variable
    rows = []
    # Scrape data
    for sector in sectors:
        # Create url to visit
        new_url = soup.find(href=True, string=sector).attrs['href']
        # Read urls into BeautifulSoup
        link_url = 'https://www.google.com' + new_url
        link_content = urllib2.urlopen(link_url).read()
        link_soup = BeautifulSoup(link_content, 'html.parser')
        # Find necessary information
        if link_soup.find(string=re.compile('Gainers')) is not None: # This if statement may be necessary
            name = link_soup.find(string=re.compile('Gainers')).parent.parent.a.string
            abbrev = link_soup.find(string=name).parent.next_sibling.next_sibling.a.string
            PerChange = link_soup.find(string=name).parent.parent.span.next_sibling.next_sibling.string
            MktCap = link_soup.find(string=name).parent.parent.td.td.td.td.contents[0]
            # Add info to rows
            rows.append((name, abbrev, PerChange, MktCap))
    # Add info in rows to SQL table
    cur.executemany("INSERT INTO Finance VALUES (?, ?, ?, ?);", rows)

    # Option 2 (Basketball Stats)
    # Create table and list strings to search
    cur.execute('CREATE TABLE Basketball (Name TEXT, GamesPlayed INT, Mins REAL, PPG REAL, FGPer REAL);')
    strings = ['1. ', '2. ', '3. ', '4. ', '5. ']
    # Create BeautifulSoup object
    url = 'http://www.espn.go.com/nba/statistics'
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    # Initialize rows variable
    rows = []
    # Scrape data
    for string in strings:
        # Scrape tag for player
        tag = soup.find(string=string).parent.a
        # Store player name for later use
        name = tag.string
        # Read url into BeautifulSoup
        link_url = tag['href']
        link_content = urllib2.urlopen(link_url).read()
        link_soup = BeautifulSoup(link_content, 'html.parser')
        # Find other information
        career_stats_tag = link_soup.find(string='STATS').parent.parent.parent.tr.tr.next_sibling
        games_played = int(career_stats_tag.td.next_sibling.string)
        mins = float(career_stats_tag.td.next_sibling.next_sibling.string)
        ppg = float(career_stats_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string)
        fgper = float(career_stats_tag.td.next_sibling.next_sibling.next_sibling.next_sibling.string)
        # Add all info to rows
        rows.append((name, games_played, mins, ppg, fgper))
    # Add info in rows to SQL table
    cur.executemany("INSERT INTO Basketball VALUES (?, ?, ?, ?, ?);", rows)

    # Option 3 (Soccer Stats)
    # Create table and BeautifulSoup object
    cur.execute('CREATE TABLE Players (Name TEXT, Hometown TEXT, Position TEXT, NumGames INT);')
    url = 'http://www.foxsports.com/soccer/united-states-women-team-stats'
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    # Create list of player tags
    players = soup.find_all(href=re.compile('^/soccer/[a-z-]+-player-stats$'))
    # Initialize rows variable
    rows = []
    # Scrape data
    for player in players:
        # Store player name, position, and number of games
        name = player.span.string
        position = player.next_sibling.next_sibling.span.string
        games_played = int(player.parent.parent.next_sibling.next_sibling.string)
        # Create url and read into BeautifulSoup
        link_url = 'http://www.foxsports.com' + player['href']
        link_content = urllib2.urlopen(link_url).read()
        link_soup = BeautifulSoup(link_content, 'html.parser')
        # Store player hometown
        hometown = link_soup.find(string='From').parent.next_sibling.next_sibling.string
        # Add all info to rows
        rows.append((name, hometown, position, games_played))
    # Add info to SQL table
    cur.executemany("INSERT INTO Players VALUES (?, ?, ?, ?);", rows)

    # Commit and close database
    try:
        db.commit()
    except sql.Error as e:
        db.rollback()
        raise sql.DatabaseError(e)
    finally:
        cur.close()

# Problem 5
def Prob5():
    """Use selenium to return a list of all the a tags containing each of the
    30 NBA teams. Return only one tag per team.
    """
    url = 'http://stats.nba.com/league/team/#!/?sort=W&dir=1'
    # Open driver and scrape data into soup
    driver = webdriver.Firefox()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    # Find requested tags
    tags = soup.find_all(name='a', class_='ng-binding', href=re.compile('/team/#%21/'))[60:]
    return tags

# Problem 6
def Prob6():
    """Creates a database called 'prob6' and a SQL table called 'Basketball',
    then uses selenium's Firefox webdriver to load and navigate a
    BeautifulSoup object.

    It loads and scrapes all the necessary webpages. If the load and scrape
    is successful, it prints the name, home wins, and away wins for the
    team just scraped. If it is not successful, it prints that it failed
    to open the webpage.
    """
    # Create database and table
    db = sql.connect('prob6')
    cur = db.cursor()
    cur.execute('CREATE TABLE Basketball (Name TEXT, HW REAL, AW REAL);')
    # Pull list of tags
    tags = Prob5()
    # Initialize rows variable
    rows = []
    # Go through each tag
    for tag in tags:
        # Create link_url and make soup via selenium
        link_url = 'http://stats.nba.com/team/#!' + tag['href'][10:]
        # Create while loop that breaks when page loads correctly
        while True:
            try:
                driver = webdriver.Firefox()
                driver.get(link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                driver.quit()
                # Initialize variables
                name = ''
                hw = float()
                aw = float()
                # Get name
                name = tag.string
                # Get hw
                for i, tag in enumerate(soup.find(string='Home ').parent.next_siblings):
                    if i == 11:
                        hw = float(tag.string)
                # Get aw
                for i, tag in enumerate(soup.find(string='Road ').parent.next_siblings):
                    if i == 11:
                        aw = float(tag.string)
                # Add info to rows
                rows.append((name, hw, aw))
                break
            # If an error arises, try again to open the page and get the info
            except:
                pass
    # Put info into table
    cur.executemany('INSERT INTO Basketball VALUES (?, ?, ?);', rows)
    # Commit and close database
    try:
        db.commit()
    except sql.Error as e:
        db.rollback()
        raise sql.DatabaseError(e)
    finally:
        cur.close()
