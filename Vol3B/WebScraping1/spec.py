"""Volume 3B: Web Scraping 1. Spec file."""

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
    tags_used = []
    value = ""
    return tags_used, value

# Problem 2
def Prob2():
    """Prints (not returns) the prettified
    string for the Three Stooges HTML.
    """
    print ""

# Problem 3
def Prob3():
    """Returns [u'title'] from the Three Stooges soup"""
    return None

# Problem 4
def Prob4():
    """Returns u'Mo' from the Three Stooges soup"""
    return None

# Problem 5
def Prob5(method):
    """Returns the u'More information...' using two different methods.
    If method is 1, it uses first method. If method is 2, it uses
    the second method.
    """
    if method == 1:
        return None
    if method == 2:
        return None

# Problem 6
def Prob6(method):
    """Returns the tag associated with the "More information..."
    link using two different methods. If method is 1, it uses the
    first method. If method is 2, it uses the second method.
    """
    if method == 1:
        return None
    if method == 2:
        return None

# Problem 7
def Prob7():
    """Loads 'SanDiegoWeather.htm' into BeautifulSoup and prints
    (not returns) the tags referred to the in the Problem 7 questions.
    """
    # Question 1
    print ""
    # Question 2
    print ""
    print ""
    # Question 3
    print ""

# Problem 8
def Prob8():
    """Loads 'Big Data dates.htm' into BeautifulSoup and uses find_all()
    and re to return a list of all tags containing links to bank data
    from September 30, 2003 to December 31, 2014.
    """
    return None
