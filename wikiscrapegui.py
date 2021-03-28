import wikipedia
import urllib.request
import PySimpleGUI as sg
import os
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

textfile = open('Outputs/output.txt', "w", encoding="utf-8")
config.read_file(open('settings.ini'))
linktemp = "https://en.wikipedia.org/wiki/"
infodata = ""
results = ""

theme = config.get('Options', 'Theme')
oneoutput = config.get('Options', 'OneOutput')

print(theme)
print(oneoutput)

iconcode = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAEdJREFUWIXt1LERACAIBMHH0iyKIiiK1jA1xIjAu5iRHQIlot8zSfIdNbE80m1NLL4DAAAAAHsZ7v6Ykd5+d/wCAAAAAEBEBwkWCCdsOlQrAAAAAElFTkSuQmCC'

sg.theme(theme)


def encode_url(s):
    htmlcodes = (
        ('%', '%25'),
        ("'", '%27'),
        (' ', '_'),
        ('&', '%26'),
        ('+', '%2B')
    )
    for code in htmlcodes:
        s = s.replace(code[0], code[1])
    return s


def make_window():

    right_click_menu_def = [[], ['Open Github Repo', 'Exit']]

    pagelayout = [[sg.Text("Enter the name of the page you would like to scrape.")],
                  [sg.InputText(size=(40, 1), key='pagename', font="Courier", justification="center")],
                  [sg.Button("Get Content"), sg.Button("Get HTML", k="PAGE-HTML")],
                  [sg.Text(size=(40, 1))],
                  [sg.Text(size=(50, 1), key="PAGE-STAT", justification="center")],
                  [sg.ML(size=(65, 12), key="PAGE-OUT", font=("Courier", 10))],
                  [sg.Text(size=(40, 1))]]

    catlayout = [[sg.Text("Enter the name of the category you would like to scrape.")],
                 [sg.Text("Category:", font="Courier"), sg.InputText(size=(30, 1), key='catname', font="Courier")],
                 [sg.Button("Get HTML", k="CAT-HTML"), sg.Button("Scrape Subcategories"), sg.Button("Scrape Pages in Category")],
                 [sg.Text(size=(40, 1))],
                 [sg.Text(size=(50, 1), key="CAT-STAT", justification="center")],
                 [sg.ML(size=(65, 12), key="CAT-OUT", font=("Courier", 10))],
                 [sg.Text(size=(40, 1))]]

    searchlayout = [[sg.Text("Search for specific page names here.")],
                    [sg.InputText(size=(40, 1), key='searchbar', font="Courier", justification="center")],
                    [sg.Button("Search!")],
                    [sg.Text(size=(40, 1))],
                    [sg.Text(size=(50, 1), key="SEARCH-STAT", justification="center")],
                    [sg.ML(size=(65, 12), key="SEARCH-OUT", font=("Courier", 10), justification="center")]]

    settingslayout = [[sg.Text("Change the theme of the GUI here!")],
                      [sg.Listbox(values=sg.theme_list(), size=(30, 12), key='THEME_LISTBOX', enable_events=True),
                       sg.Frame('Options (WIP)', font='Courier 15', layout=[
                                [sg.Radio('1 output file', 'RadioOutput', k='1OUT', enable_events=True),
                                 sg.Radio('New file for each output', 'RadioOutput', k='MULTIOUT', enable_events=True)]])],
                      [sg.Button("Set Theme")],
                      [sg.Button("Set to Default")]]

    aboutlayout = [[sg.Text("")],
                   [sg.Text("WikiScrapeGui by TetrisKid48", justification='center', font="Courier", size=(40, 1))],
                   [sg.Text("Developed in 2021", justification='center', font="Courier", size=(40, 1))],
                   [sg.Text("")],
                   [sg.Text("Special Thanks to:", justification='center', font="Courier", size=(40, 1))],
                   [sg.Text("PySimpleGui", justification='center', font="Courier", size=(40, 1))],
                   [sg.Text("jgoldsmith", justification='center', font="Courier", size=(40, 1))]]

    mainlayout = [[sg.Image('wikiscrapegui.png', pad=((0, 0), (15, 15)), key='LOGO', size=(400, 50))],
                  [sg.TabGroup([[sg.Tab('Page', pagelayout, element_justification='c'), sg.Tab('Category', catlayout, element_justification='c'),
                                 sg.Tab('Search', searchlayout, element_justification='c'), sg.Tab('Settings', settingslayout),
                                 sg.Tab('About', aboutlayout, element_justification='c')]],
                               key='TAB-GROUP', tab_location='top', border_width=10, pad=((10, 10), (10, 10)))]]

    return sg.Window('WikiScrapeGui', size=(600, 500), element_justification='c', icon=iconcode, right_click_menu=right_click_menu_def).Layout(mainlayout)


window = make_window()

print("[LOG] Main menu has been launched.")
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break

    elif event == 'Open Github Repo':
        os.startfile("https://github.com/TetrisKid48/WikiScrapeGui")

    elif event == '1OUT':
        oneoutput = 'True'

    elif event == 'MULTIOUT':
        oneoutput = 'False'

    elif event == "Set Theme":
        print("[LOG] Clicked Set Theme!")
        theme = values['THEME_LISTBOX'][0]
        print("[LOG] User Chose Theme: " + str(theme))
        window.close()
        sg.theme(theme)
        window = make_window()

    elif event == "Set to Default":
        theme = "Material1"
        print("[LOG] Theme set to default: Material1")
        window.close()
        sg.theme(theme)
        window = make_window()

    elif event == "Search!":
        query = str(values['searchbar'])
        try:
            resultslist = wikipedia.search(query, results=50)

            for x in range(len(resultslist)):
                results = results + resultslist[x] + "\n"

            window['SEARCH-STAT'].update("Here are your search results:", text_color='green')
            window['SEARCH-OUT'].update(results)

        except wikipedia.exceptions.WikipediaException:
            window['SEARCH-STAT'].update("")
            window['SEARCH-OUT'].update("")

        resultslist = ""
        results = ""

    elif event == "Get Content":
        name = str(values['pagename'])

        try:
            content = wikipedia.page(name, auto_suggest=False).content
            textfile.write(content)

            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(content)

        except wikipedia.exceptions.PageError:
            window['PAGE-STAT'].update("PageError Occured: Couldn't find a page with that title.", text_color='red')
            window['PAGE-OUT'].update("")
        except wikipedia.exceptions.DisambiguationError:
            window['PAGE-STAT'].update("DisambiguationError Occured: Page name is not specific enough.", text_color='red')
            window['PAGE-OUT'].update("")

    elif event == "PAGE-HTML":
        pagename = str(values['pagename'])

        try:
            htmlcode = wikipedia.page(pagename).html()

            textfile.write(htmlcode)
            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(htmlcode)

        except wikipedia.exceptions.PageError:
            window['PAGE-STAT'].update("PageError Occured: Couldn't find a page with that title.", text_color='red')
            window['PAGE-OUT'].update("")
        except wikipedia.exceptions.DisambiguationError:
            window['PAGE-STAT'].update("DisambiguationError Occured: Page name is not specific enough.", text_color='red')
            window['PAGE-OUT'].update("")

    elif event == 'INFO-SCRAPE':  # currently not accessable through gui
        pagename = str(values['pagename'])

        try:
            htmlcode = wikipedia.page(pagename).html()

            try:
                while True:
                    location1 = htmlcode.index("scope=\"row\">")
                    location2 = htmlcode.index("</th>")
                    infotemp = htmlcode[location1:location2]
                    infodata = infodata + infotemp
                    break

                textfile.write(infodata)
                window['PAGE-STAT'].update("This feature is currently unfinished.", text_color='black')
                window['PAGE-OUT'].update(infodata)

            except ValueError:
                window['PAGE-STAT'].update("ValueError: Couldn't find infobox contents.", text_color='red')
                window['PAGE-OUT'].update("")

        except wikipedia.exceptions.PageError:
            window['PAGE-STAT'].update("PageError Occured: Couldn't find a page with that title.", text_color='red')
            window['PAGE-OUT'].update("")
        except wikipedia.exceptions.DisambiguationError:
            window['PAGE-STAT'].update("DisambiguationError Occured: Page name is not specific enough.", text_color='red')
            window['PAGE-OUT'].update("")

    elif event == "CAT-HTML":
        catname = str(values['catname'])
        catname = encode_url(catname)
        catname = "Category:" + catname
        link = linktemp + catname

        try:
            fp = urllib.request.urlopen(link)
            mybytes = fp.read()
            htmlcode = mybytes.decode("utf8")
            fp.close()

            textfile.write(htmlcode)
            window['CAT-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['CAT-OUT'].update(htmlcode)

        except urllib.error.HTTPError:
            window['CAT-STAT'].update("HTTPError Occured: Page link could not be opened:", text_color='red')
            window['CAT-OUT'].update(link)

    elif event == "Scrape Subcategories" or "Scrape Pages in Category":

        window['CAT-STAT'].update("")
        catname = str(values['catname'])
        catname = encode_url(catname)
        catname = "Category:" + catname
        link = linktemp + catname

        try:
            fp = urllib.request.urlopen(link)
            mybytes = fp.read()
            htmlcode = mybytes.decode("utf8")
            fp.close()

        except urllib.error.HTTPError:
            window['CAT-STAT'].update("HTTPError Occured: Page link could not be opened:", text_color='red')
            window['CAT-OUT'].update(link)
            event = "Pass"

        if event == "Scrape Subcategories":
            print("[LOG] User pressed 'Subcategories' button.")

            location1 = htmlcode.index("<div class=\"mw-category-group\"><h3>") - 6
            location2 = htmlcode.index("</div></div></div>")
            htmlcode = htmlcode[location1:location2]

            catlist = htmlcode.split("\n")
            del catlist[0]
            listlen = len(catlist)

            catliststr = ""

            for x in range(0, listlen):
                location1 = catlist[x].index(" title=\"") + 8
                location2 = catlist[x].index("</a>")
                catlist[x] = catlist[x][location1:location2]

                location2 = catlist[x].index("\">")
                catlist[x] = catlist[x][:location2]

                catliststr = catliststr + catlist[x] + "\n"

            textfile.write(catliststr)
            window['CAT-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['CAT-OUT'].update(catliststr)

        if event == "Scrape Pages in Category":
            print("[LOG] User pressed 'Page Names' button.")

            location1 = htmlcode.index("This list may not reflect recent changes")
            location2 = htmlcode.index("<div class=\"printfooter\">") + 1
            htmlcode = htmlcode[location1:location2]

            location1 = htmlcode.index("<li>")
            location2 = htmlcode.index("</ul></div></div>")
            crudelist = htmlcode[location1:location2]

            pagelist = crudelist.split("\n")
            listlen = len(pagelist)

            pageliststr = ""

            for x in range(0, listlen):

                if "<span class=\"redirect-in-category\">" in pagelist[x]:
                    pagelist[x] = pagelist[x].replace("<span class=\"redirect-in-category\">", "")

                location1 = pagelist[x].index(" title=\"") + 8
                location2 = pagelist[x].index("\">")
                pagelist[x] = pagelist[x][location1:location2]

                pageliststr = pageliststr + pagelist[x] + "\n"

            textfile.write(pageliststr)
            window['CAT-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['CAT-OUT'].update(pageliststr)

textfile.close()

config['Options']['Theme'] = theme
config['Options']['OneOutput'] = oneoutput

with open('settings.ini', 'w') as configfile:
    config.write(configfile)

window.close()
