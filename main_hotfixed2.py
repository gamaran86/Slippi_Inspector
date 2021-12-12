# KIVY CONFIG - !ALWAYS ON TOP OF THE FILE
from kivy.config import Config
Config.set('graphics','width',600)
Config.set('graphics','height',400)

# KIVY IMPORTS
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooser
from kivy.uix.popup import Popup
from kivy.graphics import Canvas, Rectangle
# SLIPPI PARSING
from slippi import Game
from slippi.id import ActionState

# DATA ANALYSIS LIBS
import pandas as pd
import numpy as np

# STD PYTHON MODULES
from os import getcwd, chdir, listdir
from os.path import isfile, join, isdir


#TIME FUNCTIONS
import timesec as ts

# PD OPTIONS FOR WORKBOOK
# display x rows
#pd.set_option('display.min_rows',50)
# display all rows
#pd.set_option('display.max_rows',None)
pd.options.mode.chained_assignment = None  # default='warn'

# SLIPPI PALETTE FOR APP THEME (WIP)
# shark grey rgb(37,39,47)
# slippi greeen rgb(36,139,44)

# [GUI] POPUP FILE SELECTION
class FileSelecter(BoxLayout):
    fchooser = ObjectProperty()
    dbtn = ObjectProperty()
    defaultpath = getcwd()
    def __init__(self, **kwargs):
        super(FileSelecter,self).__init__(**kwargs)

# [GUI] MAIN WIDGET
class Selecter(FloatLayout):
    textinput = ObjectProperty()
    slippi_id = ObjectProperty()
    csv_name = ObjectProperty()
    load_status = ObjectProperty()
    exp_status = ObjectProperty()
    def __init__(self, **kwargs):
        super(Selecter,self).__init__(**kwargs)
        self.fs = FileSelecter()
        self.pup = Popup(title = 'Select replay folder',content=self.fs)
        self.textinput.text = self.fs.defaultpath

    def display_pup(self):
        self.pup.open()
        self.fs.dbtn.bind(on_release=self.dismiss_pup)
    def dismiss_pup(self,btn):
        self.textinput.text = self.fs.fchooser.selection[0]
        self.pup.dismiss()

    def analyze_w_id(self):
        self.load_status.color = [1,1,0,1]
        self.load_status.text = 'Loading...'
        self.g_data = GameInfo(self.textinput.text, self.slippi_id.text)#Load the game
        #print(self.slippi_id.text)
        try:
            diag = self.g_data.load_game(self.g_data.path)
            if diag == 0 :
                self.load_status.color = [0,1,0,1]
                self.load_status.text = 'Successfully loaded'
            else:
                self.load_status.color = [1,0,0,1]
                self.load_status.text = 'No valid files found in selected directory'
        except:
            self.load_status.color = [1,0,0,1]
            self.load_status.text = 'Critical Error'
    def print_data(self):
        self.g_data.print_df()

    def export(self):
        try:
            self.g_data.print_csv(self.csv_name.text)
            self.exp_status.color = [0,1,0,1]
            self.exp_status.text = self.csv_name.text + '.csv created in:\n' + getcwd()
        except:
            self.exp_status.color = [1,0,0,1]
            self.exp_status.text = 'Error: exportation impossible'

# [GUI] APP CREATION
class FrameApp(App):
    def build(self):
        return Selecter()

# [DATA] GAME METADATA STRUCTURE
class GameInfo():
    def __init__(self,path,code):
        self.state_base = create_state_base()
        self.path = path
        self.game_name = None
        self.player = None
        self.player_id = str(code)
        self.opponent = None
        self.stage = None
        self.df = pd.DataFrame()

    class Player():
        def __init__(self,port,id,name,isp,char):
            self.port = port
            self.id = id
            self.name = name
            self.isplayer = isp
            self.char = char

    def set_player_id(self):
        pass

    def print_game_info(self):
        print('game: ' + self.game_name)
        print('stage: ' + self.stage)
        print('player: ')
        print('\tid: ' + self.player.id)
        print('\tname: ' + self.player.name)
        print('\tport: ' + str(self.player.port))
        print('\tcharacter: ' + self.player.char)

        print('\n')

        print('opponent: ')
        print('\tid: ' + self.opponent.id)
        print('\tname: ' + self.opponent.name)
        print('\tport: ' + str(self.opponent.port))
        print('\tcharacter: ' + self.opponent.char)

    def load_game(self,path):
    #SELECTION CONTROL
        if isdir(path): #Case dir
            try:
                games_path_0 = [join(path,f) for f in listdir(path) if isfile(join(path,f))]
                games_path = [f for f in games_path_0 if f.split('.')[f.count('.')] == 'slp'] 

                print(str(len(games_path)) + ' games found')
            except:
                print('no valid files in directory')
                print(listdir(path))
                for f in listdir(path):
                    print(join(path,f))
                return 1

        elif isfile(path): #Case file
            path_split = path.split('\\')
            f = path_split[len(path_split)-1]

            if f.split('.')[1] == 'slp':
                games_path = [path]
                print ('1 game found')
            else:
                print('invalid file format')
                return 1

        else:
            print('invalid file format')
            return 1

        for path in games_path:
            try:
                g = Game(path)
            

                print('\nLoading game @ ',path)

                # METADATA - GAME NAME
                split_path = path.split('\\')
                filename = split_path[len(split_path)-1].split('.')
                self.game_name = filename[0]

                # METADATA - STAGE
                self.stage = str(g.start.stage).split('.')[1]

                # METADATA - PLAYERS DATA (See. GameInfo.Player Class)
                players = g.metadata.players
                i = 0
                for p in players: #Scan all ports for a player
                    i += 1
                    pchar = str()
                    if p != None: # = if player in port
                        for n,c in enumerate(p.characters.keys()):
                            if n == 0:
                                temp = str(c).split('.')
                                pchar = temp[1]
                            else:
                                temp = str(c).split('.')
                                pchar = pchar + '\\' + temp[1]

                        if p.netplay.code == self.player_id:
                            self.player = self.Player(i,
                                    p.netplay.code,
                                    p.netplay.name,
                                    True,
                                    pchar)
                        else:
                            self.opponent = self.Player(i,
                                    p.netplay.code,
                                    p.netplay.name,
                                    False,
                                    pchar)
                # FRAMEDATA
                inputdf = pd.DataFrame()

                # Player Action state number
                f_state = [
                        f.ports[self.player.port-1]
                        .leader
                        .post
                        .state
                        for f in g.frames
                        ]
                inputdf['P_STATE_NUM'] = f_state

                # Action state name
                inputdf['P_STATE_NAME'] = [
                        self.state_base[str(int(k))]
                        for k in f_state
                        ]
                # Player %
                inputdf['P_DMG'] = [
                        f.ports[self.player.port-1]
                        .leader
                        .post
                        .damage
                        for f in g.frames
                        ]

                # Opponent %
                inputdf['OPP_DMG'] = [
                        f.ports[self.opponent.port-1]
                        .leader
                        .post
                        .damage
                        for f in g.frames
                        ]
                # Player LCL (Seem bugged)
                inputdf['P_LCL'] = [
                        f.ports[self.player.port-1]
                        .leader
                        .post
                        .l_cancel
                        for f in g.frames
                        ]
                # Time
                timelist = [ts.convert_f_to_time(ts.convert_to_frame(0,8,2,3)-f)
                        for f in inputdf.index]
                timelist2 = [ts.format_time(*i) for i in timelist]
                inputdf['TIME'] = timelist2

                # Dumping redondant frames
                outputdf = inputdf.loc[inputdf["P_STATE_NAME"].shift(-1)
                        != inputdf["P_STATE_NAME"]]

                # Player Action state end
                outputdf["END"] = outputdf.index

                # Player Action state start
                outputdf["START"] = outputdf["END"].shift()

                # Player Action state duration
                outputdf["DURATION"] = outputdf["END"] - outputdf["START"]

                # Game ID
                outputdf['G_NAME'] = self.game_name

                # Stage
                outputdf['STAGE'] = self.stage

                # Player Slippi ID
                outputdf["P_ID"] = self.player.id

                # Player Character
                outputdf['P_CHAR'] = self.player.char

                # Opponent Slippi ID
                outputdf['OPP_ID'] = self.opponent.id

                # Opponent Character
                outputdf['OPP_CHAR'] = self.opponent.char

                self.df = self.df.append(outputdf)
                print('\nSuccessfully loaded data for file \n' + self.game_name)

            except:
                    print('game @ ',path , 'corrupted')
        return 0

    def print_df(self): #DEBUG ONLY
        print(self.df)

    def print_csv(self,name):
        self.df.to_csv(getcwd() + '\\' + name + '.csv')

# [DATA] ACTION STATE DATABASE FROM PYSLIPPI
def create_state_base():
    base = {}

    for k, v in enumerate(ActionState):
        base[str(k)] = str(v).split('.')[1]
    return base


if __name__ == "__main__":
    FrameApp().run()
