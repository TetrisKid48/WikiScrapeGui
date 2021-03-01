import wikipedia
import urllib.request
import PySimpleGUI as sg

textfile = open('output.txt', 'w', encoding="utf-8")
linktemp = "https://en.wikipedia.org/wiki/"

sg.theme('Material1')

pagelayout = [[sg.Text("Enter the name of the page you would like to scrape.")],
              [sg.InputText(key='pagename')],
              [sg.Button("Get Content"), sg.Button("Get HTML")],
              [sg.Text(size=(80, 1))],
              [sg.Text(size=(80, 1), key="PAGE-STAT")],
              [sg.ML(size=(80, 8), key="PAGE-OUT")],
              [sg.Text(size=(80, 1))]]

catlayout = [[sg.Text("Enter the name of the category you would like to scrape.")],
             [sg.Text("Category:"), sg.InputText(key='catname')],
             [sg.Button("Scrape Subcategories"), sg.Button("Scrape Pages in Category")],
             [sg.Text(size=(80, 1))],
             [sg.Text(size=(80, 1), key="CAT-STAT")],
             [sg.ML(size=(80, 8), key="CAT-OUT")],
             [sg.Text(size=(80, 1))]]

mainlayout = [[sg.Image('wikiscrapegui.png', pad=((115, 115), (15, 10)), key='LOGO', size=(200, 25))],
              [sg.TabGroup([[sg.Tab('Page', pagelayout), sg.Tab('Category', catlayout)]], key='TAB-GROUP')]]

window = sg.Window('WikiScrapeGui', size=(430, 375)).Layout(mainlayout)
print("[LOG] Main menu has been launched.")
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == "Get Content":
        name = str(values['pagename'])
        window['PAGE-STAT'].update("")
        window['PAGE-OUT'].update("")

        try:
            content = wikipedia.page(name, auto_suggest=False).content
            textfile.write(content)

            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(content)

        except wikipedia.exceptions.PageError:
            window['PAGE-STAT'].update("Error Occured. Couldn't find a page with that title.", text_color='red')
        except wikipedia.exceptions.DisambiguationError:
            window['PAGE-STAT'].update("Error Occured. Page name is not specific enough.", text_color='red')

    if event == "Get HTML":
        window['PAGE-STAT'].update("")
        window['PAGE-OUT'].update("")
        pagename = str(values['pagename'])
        pagename = pagename.replace(" ", "_")
        link = linktemp + pagename

        try:
            fp = urllib.request.urlopen(link)
            mybytes = fp.read()
            htmlcode = mybytes.decode("utf8")
            fp.close()

            window['PAGE-STAT'].update("Success! This text was saved to output.txt:", text_color='green')
            window['PAGE-OUT'].update(htmlcode)

        except urllib.error.HTTPError:
            window['PAGE-STAT'].update("Error Occured. Page link could not be opened.", text_color='green')

    if event == "Scrape Subcategories" or "Scrape Pages in Category":
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
        window['CAT-STAT'].update("This feature is currently unfinished.", text_color='green')

    if event == "Scrape Pages in Category":
        print("[LOG] User pressed 'Page Names' button.")
        window['CAT-STAT'].update("This feature is currently unfinished.", text_color='green')

textfile.close()
window.close()
