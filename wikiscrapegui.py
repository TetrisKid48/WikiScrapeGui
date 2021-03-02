import wikipedia
import urllib.request
import PySimpleGUI as sg

textfile = open('output.txt', 'w', encoding="utf-8")
linktemp = "https://en.wikipedia.org/wiki/"

icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAEdJREFUWIXt1LERACAIBMHH0iyKIiiK1jA1xIjAu5iRHQIlot8zSfIdNbE80m1NLL4DAAAAAHsZ7v6Ykd5+d/wCAAAAAEBEBwkWCCdsOlQrAAAAAElFTkSuQmCC'

sg.theme('Material1')

pagelayout = [[sg.Text("Enter the name of the page you would like to scrape.")],
              [sg.InputText(size=(40, 1), key='pagename', font="Courier")],
              [sg.Button("Get Content"), sg.Button("Get HTML", k="PAGE-HTML")],
              [sg.Text(size=(40, 1))],
              [sg.Text(size=(40, 1), key="PAGE-STAT")],
              [sg.ML(size=(50, 12), key="PAGE-OUT", font=("Courier", 10))],
              [sg.Text(size=(40, 1))]]

catlayout = [[sg.Text("Enter the name of the category you would like to scrape.")],
             [sg.Text("Category:", font="Courier"), sg.InputText(size=(30, 1), key='catname', font="Courier")],
             [sg.Button("Get HTML", k="CAT-HTML"), sg.Button("Scrape Subcategories"), sg.Button("Scrape Pages in Category")],
             [sg.Text(size=(40, 1))],
             [sg.Text(size=(40, 1), key="CAT-STAT")],
             [sg.ML(size=(50, 12), key="CAT-OUT", font=("Courier", 10))],
             [sg.Text(size=(40, 1))]]

aboutlayout = [[sg.Text("")],
               [sg.Text("WikiScrapeGui by TetrisKid48", justification='center', font="Courier", size=(40, 1))],
               [sg.Text("Developed in 2021", justification='center', font="Courier", size=(40, 1))],
               [sg.Text("")],
               [sg.Text("Special Thanks to:", justification='center', font="Courier", size=(40, 1))],
               [sg.Text("PySimpleGui", justification='center', font="Courier", size=(40, 1))],
               [sg.Text("jgoldsmith", justification='center', font="Courier", size=(40, 1))]]

mainlayout = [[sg.Image('wikiscrapegui.png', pad=((0, 0), (15, 15)), key='LOGO', size=(400, 50))],
              [sg.TabGroup([[sg.Tab('Page', pagelayout, element_justification='c'), sg.Tab('Category', catlayout, element_justification='c'),
                             sg.Tab('About', aboutlayout, element_justification='c')]],
                           key='TAB-GROUP', tab_location='top', border_width=10, pad=((10, 10), (10, 10)))]]

window = sg.Window('WikiScrapeGui', size=(500, 500), element_justification='c',
                   icon=icon).Layout(mainlayout)
print("[LOG] Main menu has been launched.")
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event == "Get Content":
        name = str(values['pagename'])

        try:
            content = wikipedia.page(name, auto_suggest=False).content
            textfile.write(content)

            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(content)

        except wikipedia.exceptions.PageError:
            window['PAGE-STAT'].update("Error Occured. Couldn't find a page with that title.", text_color='red')
        except wikipedia.exceptions.DisambiguationError:
            window['PAGE-STAT'].update("Error Occured. Page name is not specific enough.", text_color='red')

    elif event == "PAGE-HTML":
        pagename = str(values['pagename'])
        pagename = pagename.replace(" ", "_")
        link = linktemp + pagename

        try:
            fp = urllib.request.urlopen(link)
            mybytes = fp.read()
            htmlcode = mybytes.decode("utf8")
            fp.close()

            textfile.write(htmlcode)
            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(htmlcode)

        except urllib.error.HTTPError:
            window['PAGE-STAT'].update("Error Occured. Page link could not be opened.", text_color='red')

    elif event == "CAT-HTML":
        catname = str(values['catname'])
        catname = catname.replace(" ", "_")
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
            window['CAT-STAT'].update("Error Occured. Page link could not be opened.", text_color='red')

    elif event == "Scrape Subcategories" or "Scrape Pages in Category":
        print("[LOG] A scrape button was pressed in the Category tab.")

        window['CAT-STAT'].update("")
        catname = str(values['catname'])
        catname = catname.replace(" ", "_")
        catname = "Category:" + catname
        link = linktemp + catname

        try:
            fp = urllib.request.urlopen(link)
            mybytes = fp.read()
            htmlcode = mybytes.decode("utf8")
            fp.close()
        except urllib.error.HTTPError:
            window['CAT-STAT'].update("Error Occured. Category page link could not be opened.", text_color='red')
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
window.close()
