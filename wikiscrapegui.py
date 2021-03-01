import wikipedia
import urllib.request
import PySimpleGUI as sg

textfile = open('output.txt', 'w', encoding="utf-8")
linktemp = "https://en.wikipedia.org/wiki/"

sg.theme('Material1')

mainlayout = [[sg.Image('wikiscrapegui.png', pad=((100, 100), (15, 10)), key='LOGO', size=(200, 25))],
              [sg.Text('Would you like to scrape one page, or an entire category?', justification='center')],
              [sg.Button('Page', size=(10, 1)), sg.Button('Category', size=(10, 1))]]

window = sg.Window('WikiScrapeGui', size=(400, 125)).Layout(mainlayout)
print("[LOG] Main menu has been launched.")

while True:  # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    if event == "Page":
        pagelayout = [[sg.Text("Enter the name of the page you would like to scrape.")],
                      [sg.InputText(key='pagename')],
                      [sg.Button("Get Content"), sg.Cancel()]]

        pagewindow = sg.Window("Scrape Page").Layout(pagelayout)
        while True:
            event, values = pagewindow.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                pagewindow.close()
                break
            if event == "Cancel":
                pagewindow.close()
                break
            if event == "Get Content":
                name = str(values['pagename'])
                try:
                    content = wikipedia.page(name, auto_suggest=False).content
                    textfile.write(content)

                    outputlayout = [[sg.Text("Success!")],
                                    [sg.Text("This text was saved to output.txt:")],
                                    [sg.ML(content, size=(80, 8))],
                                    [sg.Button("Back")]]

                    pageoutput = sg.Window("Output Success").Layout(outputlayout)
                    while True:
                        event, values = pageoutput.read()
                        if event in (sg.WIN_CLOSED, 'Exit'):
                            pageoutput.close()
                            break
                        if event == "Back":
                            pageoutput.close()
                            break

                except wikipedia.exceptions.PageError:
                    sg.popup("Error Occured", "Couldn't find a page with that title.")
                    pagewindow.close()
                    break
                except wikipedia.exceptions.DisambiguationError:
                    sg.popup("Error Occured", "Page name is not specific enough.")
                    pagewindow.close()
                    break

    if event == "Category":
        catelayout = [[sg.Text("Enter the name of the category you would like to scrape.")],
                      [sg.Text("Category:"), sg.InputText(key='catname')],
                      [sg.Text("Would you like to scrape the subcategories or the page names?")],
                      [sg.Button("Subcategories"), sg.Button("Page Names"), sg.Cancel()]]

        catwindow = sg.Window("Scrape Category").Layout(catelayout)
        while True:
            event, values = catwindow.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                catwindow.close()
                break
            if event == "Cancel":
                catwindow.close()
                break
            if event == "Subcategories" or "Page Names":
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
                    sg.popup("Error Occured", "Category page link could not be opened.")
                    catwindow.close()
                    break

            if event == "Subcategories":
                print("[LOG] User pressed 'Subcategories' button.")
                subcatlayout = [[sg.Text("This feature is not yet finished.", text_color='green', key='SUBCAT-STATUS')],
                                [sg.ML(size=(80, 8), key='SUBCAT-OUTPUT')],
                                [sg.Button("OK")]]

                subcatwindow = sg.Window("Subcategory Output").Layout(subcatlayout)
                while True:
                    event, values = subcatwindow.read()
                    if event in (sg.WIN_CLOSED, 'OK'):
                        subcatwindow.close()
                        break

            if event == "Page Names":
                print("[LOG] User pressed 'Page Names' button.")
                pageslayout = [[sg.Text("This feature is not yet finished.", text_color='green', key='SUBCAT-STATUS')],
                               [sg.ML(size=(80, 8), key='SUBCAT-OUTPUT')],
                               [sg.Button("OK")]]

                pageswindow = sg.Window("Category Pages Output").Layout(pageslayout)
                while True:
                    event, values = pageswindow.read()
                    if event in (sg.WIN_CLOSED, 'OK'):
                        pageswindow.close()
                        break

textfile.close()
window.close()
