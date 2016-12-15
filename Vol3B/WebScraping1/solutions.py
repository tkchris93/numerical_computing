"""Volume 3B: Web Scraping 1. Solutions file."""

from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Three Stooges</title></head>
<body>
<p class="title"><b>The Three Stooges</b></p>
<p class="story">Have you ever met the three stooges? Their names are
<a href="http://example.com/larry" class="stooge" id="link1">Larry</a>,
<a href="http://example.com/mo" class="stooge" id="link2">Mo</a> and
<a href="http://example.com/curly" class="stooge" id="link3">Curly</a>;
and they are really hilarious.</p>
<p class="story">...</p>
"""

# Problem 1
def Prob1():
    """Returns a list of tags used and the value of
    the type attribute associated with the style tag
    """
    tags_used = ['html', 'head', 'title', 'meta', 'style', 'body', 'div', 'h1', 'p', 'a']
    value = "text/css"
    return tags_used, value

# Problem 2
def Prob2():
    """Prints (not returns) the prettified
    string for the Three Stooges HTML.
    """
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup.prettify())

# Problem 3
def Prob3():
    """Returns [u'title'] from the Three Stooges soup"""
    soup = BeautifulSoup(html_doc, 'html.parser')
    tag = soup.p
    return tag['class']

# Problem 4
def Prob4():
    """Returns u'Mo' from the Three Stooges soup"""
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.a.next_sibling.next_sibling.string

# Problem 5
def Prob5(method):
    """Returns the u'More information...' using two different methods.
    If method is 1, it uses first method. If method is 2, it uses
    the second method.
    """
    example_soup = BeautifulSoup(open('example.htm'), 'html.parser')
    if method == 1:
        return example_soup.a.string
    if method == 2:
        return example_soup.p.next_sibling.next_sibling.a.string

# Problem 6
def Prob6(method):
    """Returns the tag associated with the "More information..."
    link using two different methods. If method is 1, it uses the
    first method. If method is 2, it uses the second method.
    """
    example_soup = BeautifulSoup(open('example.htm'), 'html.parser')
    if method == 1:
        return example_soup.find(href='http://www.iana.org/domains/example')
    if method == 2:
        return example_soup.find(string='More information...').parent

# Problem 7
def Prob7():
    """Loads 'SanDiegoWeather.htm' into BeautifulSoup and prints
    (not returns) the tags referred to the in the Problem 7 questions.
    """
    soup = BeautifulSoup(open('SanDiegoWeather.htm'), 'html.parser')
    # Question 1
    print soup.find(string="Thursday, January 1, 2015").parent
    # Question 2
    print soup.find(href='/history/airport/KSAN/2014/12/31/DailyHistory.html')
    print soup.find(href='/history/airport/KSAN/2015/1/2/DailyHistory.html')
    # Question 3
    print soup.find(string= 'Max Temperature').parent.parent.next_sibling.next_sibling.span.span

# Problem 8
def Prob8():
    """Loads 'Big Data dates.htm' into BeautifulSoup and uses find_all()
    and re to return a list of all tags containing links to bank data
    from September 30, 2003 to December 31, 2014.
    """
    soup = BeautifulSoup(open('Big Data dates.htm'), 'html.parser')
    # Pulls all data from years 2010-2014
    links = soup.find_all(href=True, string=re.compile("201[0-4]"))
    # Adds all data from years 2003-2009
    links += soup.find_all(href=True, string=re.compile("200[3-9]"))
    return links
