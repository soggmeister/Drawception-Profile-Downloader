#! python3

# Download every game, caption and drawings, by a user into a file on desktop.
import requests, os, getpass, shutil, unidecode, sys
import PySimpleGUI as sg
from bs4 import BeautifulSoup

os.system('color 3f')

# Get Username of CWD User
user = getpass.getuser()

# Change CWD to desktop, make a folder assigning to a user ID and Name (but keep track of original cwd)

nativePath = os.getcwd()

desktopPath = ("C:/Users/%s/Desktop/" % (user))
os.chdir(desktopPath)

# Create window to ask for information
# Define the profile which drawings will downloaded from
# Find out the maximum page that the games extend to.

while True:
    
    sg.theme('DarkTeal12')
    userRequest = [[sg.Text('Please enter a valid Drawception User ID.')],
               [sg.Input()],
               [sg.Text("Please enter the Drawceptioner's username, or use any name you'd like.")],
               [sg.Input()],
               [sg.OK()] ]
    
    # Access zip file native path for icon ;)
    os.chdir(nativePath + '\\icon')
    window = sg.Window('Drawception User Credentials', userRequest, icon="mascot-d.ico")
    
    event, values = window.read()
    window.close()
    
    userID, userName = values[0], values[1]
    try:
        if userName == '' or userID == '':
            sg.Popup('Please fill in all credential areas.')
            continue
        if not userID.isnumeric():
            sg.Popup('Please do not enter any letters in the user ID.')
            continue
    except AttributeError:
        raise Exception('Program was quit by the user.')
        os.system('@pause')
        sys.exit()
        
    userProfileURL = f'https://drawception.com/player/{userID}/{userName}/drawings/1'
    userPublicGamesURL = f'https://drawception.com/player/{userID}/{userName}/games/1'
    
    # Get the page of the user.

    userPage = requests.get(userProfileURL)
    html = BeautifulSoup(userPage.content, "html.parser")

    userPage = requests.get(userPublicGamesURL)
    html = BeautifulSoup(userPage.content, "html.parser")

    for i in range(2, 9):
        try:
            if str(html.select(f"#main > div.profile-layout > div.profile-layout-content > div.text-center > ul > li:nth-child({i}) > a")[0].text) == '»':
                continue
            maximumGame = str(html.select(f"#main > div.profile-layout > div.profile-layout-content > div.text-center > ul > li:nth-child({i}) > a")[0].text)
            continue
        except:
            continue
    try:
        sg.Popup(f'{userName} has {maximumGame} pages of games. That is approximately { 18 * int(maximumGame) } games.', 'Press OK to continue.')
        break
    except:
        maximumGame = 1
        sg.Popup(f'{userName} has {maximumGame} page of games. That is *about* 18 games.', 'Press OK to continue.')
        break
    
# Create a directory of the user, change cwd to that directory

os.chdir(desktopPath)
os.mkdir(userName + ' Games')
userFolder = userName + ' Games'
userFolderPath = desktopPath + f"/{userFolder}"
os.chdir(userFolderPath)
open(f'_{userName} Summary.txt', 'w').close()

os.mkdir('Own Games')
wholeFile = ("C:/Users/%s/Desktop/%s/" % (user, userFolder))
ownGamesPath = ("C:/Users/%s/Desktop/%s/Own Games" % (user, userFolder))

# Create a function or loop call that grabs every image on a page, then iterate to the next page, grabbing each image until all pages iterated
# Create a function that stores the image in a unique folder on the desktop.

def getDrawingContent(content):
    nameList, dateList, urlList = [], [], []
    container = str(content.select("#main > div.profile-layout > div.profile-layout-content > div.thumbpanel-container"))
    for number in range(1, 19):
        try:
            element = content.select(f'#main > div.profile-layout > div.profile-layout-content > div.thumbpanel-container > div:nth-child({number})')[0]
            finder = element.select("img")
            textMuted = element.select("span", class_="text-muted")[1]
            
            if finder == []:
                finder = element.select("span")[0]
                captionURL = content.select(f'#main > div.profile-layout > div.profile-layout-content > div.thumbpanel-container > div:nth-child({number}) > a')[0]

            for telemon in finder:
            # Don't mind my naming convention.
                try:
                    string = telemon.lstrip().rstrip()
                    nameList.append(string + 'CAPTION123123')
                    dateList.append(textMuted.text.lstrip().rstrip())
                    urlList.append(captionURL['href'])
                except:
                    nameList.append(telemon['alt'] + 'IMAGE123123')
                    dateList.append(textMuted.text.lstrip().rstrip())
                    urlList.append(telemon['src'])
        except:
            break
    return nameList, dateList, urlList

def sendToFolder(package):
    try:
        for element in range(0, 18):
            if package[0][element].endswith('IMAGE123123'):
                os.chdir(ownGamesPath)
                img = requests.get(package[2][element], stream=True)
                name = '[' + package[1][element] + '] ' + unidecode.unidecode(package[0][element]).replace(':', '.').replace('"', "'").replace('IMAGE123123', '')

                with open(name + ".png", "wb") as out_file:
                    shutil.copyfileobj(img.raw, out_file)
                del img

                os.chdir(wholeFile)
                writer = open(f'_{userName} Summary.txt', 'a')
                writer.write('[' + package[1][element] + '] ' + package[0][element].replace('IMAGE123123', '') + '\n')
                writer.write('https://drawception.com' + package[2][element] + '\n\n')
                writer.close()
        
            if package[0][element].endswith('CAPTION123123'):
                if captionCondition == False:
                    continue
                
                os.chdir(captionedGames)
                
                page = BeautifulSoup(requests.get('https://drawception.com' + package[2][element]).content, "html.parser")
                for entry in range(1, 25):
                    correctEntry = 1
                    try:
                        panelFinder = page.select(f'#main > div.row.add-margin-top3x > div:nth-child({entry}) > div.gamepanel-holder')[0]
                        text = panelFinder.select('p')[0].text.lstrip().rstrip()
                        if package[0][element].replace('CAPTION123123', '') == text:
                            correctEntry = entry - 1
                            break
                    except:
                        continue
                
                if correctEntry != 0:
                    
                    correctPanelFinder = page.select(f'#main > div.row.add-margin-top3x > div:nth-child({correctEntry}) > div.gamepanel-holder')[0]
                    creator = page.select(f'#main > div.row.add-margin-top3x > div:nth-child({correctEntry}) > div.gamepanel-holder > div.panel-details.flex-space-between > div.panel-user > a')[0].text
                    picture = correctPanelFinder.select('img')[0]['src']
                    title = text.replace(':', '.').replace('"', "'")

                    captionImage = requests.get(picture, stream=True)
                    name = '[CAPTIONED] ' + f'[{package[1][element]}] ' + unidecode.unidecode(title) + f', made by {creator}.'
                    with open(name + ".png", "wb") as out_file:
                        shutil.copyfileobj(captionImage.raw, out_file)
                    del captionImage
                        
                elif correctEntry == 0:
                    correctPanelFinder = page.select('#main > div.row.add-margin-top3x > div:nth-child(2) > div.gamepanel-holder')[0]
                    creator = page.select('#main > div.row.add-margin-top3x > div:nth-child(2) > div.gamepanel-holder > div.panel-details.flex-space-between > div.panel-user > a')[0].text
                    picture = correctPanelFinder.select('img')[0]['src']
                    title = text.replace(':', '.').replace('"', "'")
                    
                    captionImage = requests.get(picture, stream=True)
                    name = '[CAPTIONED] ' + f'[{package[1][element]}] ' + unidecode.unidecode(title) + f', made by {creator}.'
                    with open(name + ".png", "wb") as out_file:
                        shutil.copyfileobj(captionImage.raw, out_file)
                    del captionImage
                    
                os.chdir(wholeFile)        
                writer = open(f'_{userName} Summary.txt', 'a')
                writer.write('[' + package[1][element] + '] ' + package[0][element].replace('CAPTION123123', '') + f', in response to {creator}\'s drawing.\n')
                writer.write('https://drawception.com' + package[2][element] + '\n\n')
                writer.close()
    except:
        return None


######################################################################################


sg.theme('DarkTeal12')
os.chdir(nativePath + '\\icon')
assertOtherUserDrawings = sg.popup_yes_no('Store drawings from other users?', icon="mascot-d.ico")

if assertOtherUserDrawings == 'No' or assertOtherUserDrawings == None:
    captionCondition = False
else:
    captionCondition = True
    os.chdir(userFolderPath)
    os.mkdir('Captioned Games')
    captionedGames = ("C:/Users/%s/Desktop/%s/Captioned Games" % (user, userFolder))
    

print('You can stop the program at anytime.\nUse the Ctrl+C keyboard interrupt, or quit the command prompt.')
    
for page in range(1, int(maximumGame) + 1):
    userProfileURL = f"https://drawception.com/player/{userID}/{userName}/games/{page}"
    drawings = BeautifulSoup(requests.get(userProfileURL).content, "html.parser")
    
    drawingCollection = getDrawingContent(drawings)
    sendToFolder(drawingCollection)

os.chdir(nativePath + '\\icon')
sg.Popup('All done!', icon="mascot-d.ico")
os.chdir(desktopPath)
os.startfile(userFolder)


    



