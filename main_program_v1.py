import tkinter as tk
from tkinter import font
from tkinter import ttk
import os
import time
import platform

if platform.system() == "Windows":
    file_separator = "\\"
elif platform.system() == "Linux":
    file_separator = "/"
else:
    raise Exception("System is not supported")

todays_date = time.strftime("%x")
file_header = ( "Plant Id",
                "Pot Number",
                "Into Soil",
                "Into Greenhouse",
                "Into Pots",
                "Begin Flowering",
                "End Flowering",
                "End Maturation",
                "Harvested",
                "Plant State")

action_colors = {   "Rename Pot" :        ("#000", "#222", "#fff"),
                    "Into Soil" :       ("#751", "#862", "#fff"),
                    "Into Greenhouse" : ("#050", "#262", "#fff"),
                    "Into Pots" :       ("#080", "#292", "#000"),
                    "Begin Flowering" : ("#0c0", "#2d2", "#000"),
                    "End Flowering" :   ("#9d0", "#ae2", "#000"),
                    "End Maturation" :  ("#dd0", "#ee2", "#000"),
                    "Harvested" :       ("#aa0", "#bb2", "#000")}
actions_in_order = ["Rename Pot", "Into Soil", "Into Greenhouse", "Into Pots", "Begin Flowering", "End Flowering", "End Maturation", "Harvested"]
export_filename = "Greenhouse_Summary.csv"
import_filename = "New_Greenhouse_Data.csv"
data_folder = "Tub_data"

class ContinueQuestion():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.continue_answer = None
        self.button_font = font.Font(size = 48)

        self.continue_button = tk.Button(self.frame, text = "Continue?", command = self.answerTrue, font = self.button_font, width = 24, height = 6)
        self.continue_button.grid(row = 1, column = 0)
        self.quit_button = tk.Button(self.frame, text = "Don't Continue", fg = "red", command = self.answerFalse, font = self.button_font, width = 24, height = 6)
        self.quit_button.grid(row = 1, column = 1)
        self.info_label = tk.Label(self.frame, text = "\nThis action will overright data that currently exists!\n", font = self.button_font)
        self.info_label.grid(row = 0, columnspan = 2)

        self.master.wait_window()

    def answerTrue(self):
        self.continue_answer = True
        self.master.destroy()

    def answerFalse(self):
        self.continue_answer = False
        self.master.destroy()

    def getAnswer(self):
        return self.continue_answer

class PlantNameInput():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.new_name = ""

        self.text_label = tk.Label(self.frame, text = "Name:")
        self.text_label.grid(row = 0, column = 0)
        self.data_entry = tk.Entry(self.frame)
        self.data_entry.grid(row = 0, column = 1)
        self.data_entry.focus()
        self.entry_done = tk.Button(self.frame, text = "Done", command = self.buttonClick)
        self.entry_done.grid(row = 0, column = 2)

        self.master.bind("<Return>", self.pressEnter)
    
        self.master.wait_window()
    
    def buttonClick(self):
        self.new_name = self.data_entry.get()
        self.master.destroy()

    def pressEnter(self, event):
        self.buttonClick()

    def getName(self):
        return self.new_name

class MainWindow():

    def __init__(self, master):
        self.master = master
        # self.master.title = "Greenhouse Data Manager"
        self.frame = tk.Frame(master)
        self.action_frame = tk.Frame(master)
        self.greenhouse_frame = tk.Frame(master)
        self.tub_frame = tk.Frame(master)
        self.frame.pack(side = "top")
        self.pot_frame = tk.Frame(master)
        self.action_frame.pack(side = "left", anchor = "nw")
        self.greenhouse_frame.pack(side = "top", anchor = "w")
        self.tub_frame.pack(side = "top", anchor = "nw")
        self.pot_frame.pack(side = "top", anchor = "nw", padx = 20, pady = 20)


        self.gh_format = {  "greenhouse count" : 4,
                            "tub-per-greenhouse" : 20,
                            "tub rows" : 5,
                            "tub columns" : 4}
                            # "pot-per-tub" : 60,
                            # "pot rows" : 6,
                            # "pot columns" : 10}

        self.gh_format["greenhouse names"] = ["GH%01d%s"%(int(i/2)+1, ["E","W"][i%2]) for i in range(self.gh_format["greenhouse count"])]

        self.greenhouse_variable = tk.IntVar()
        self.tub_variable = tk.IntVar()
        self.action_state = tk.StringVar()

        self.greenhouse_variable.set(0)
        self.tub_variable.set(0)
        self.action_state.set(None)

        self.tub_filename = "%s-%s.csv"%(self.gh_format["greenhouse names"][self.greenhouse_variable.get()], self.tub_variable.get() + 1)
        self.tub_filepath = data_folder + file_separator + self.tub_filename
        
        self.loadTub()
        self.makeButtons()

    def makePotButtons(self):
        button_style = {"width" : 13, "height" : 3, "font" : font.Font(size = 12)}
        
        if self.gh_format["pot-per-tub"] > 60:
            button_style = {"width" : 10, "height" : 3, "font" : font.Font(size = 10)}

        for i in range(self.gh_format["pot-per-tub"]):
            self.pot_buttons[i] = tk.Button(self.pot_frame, button_style)

            self.pot_buttons[i].configure(  textvariable    = self.pot_text[i],
                                            command         = lambda a=i: self.updatePot(a))
            self.pot_buttons[i].grid(       row             = i % self.gh_format["pot rows"],
                                            column          = (int( i / self.gh_format["pot rows"] ) + 3))

    def makeButtons(self):
        button_style = {"width" : 15, "height" : 3, "font" : font.Font(size = 12)}

        # self.save_button = tk.Button(self.frame, text = "Save", width = button_style["width"] * 2, height = button_style["height"], command = self.saveTub)
        # self.save_button.grid(row = 1, column = 0)

        self.import_button = tk.Button( self.action_frame, 
                                        text    = "Import File from:\n%s"%import_filename, 
                                        command = self.importMaster,
                                        width   = 30, 
                                        height  = 3,  
                                        font    = font.Font(size = 12))
        self.import_button.grid()

        # Making the Greenhouse Buttons
        for i in range(self.gh_format["greenhouse count"]):
            self.greenhouse_buttons[i] = tk.Radiobutton(self.greenhouse_frame)
            self.greenhouse_buttons[i].configure(   text        = self.gh_format["greenhouse names"][i],
                                                    indicatoron = 0,
                                                    variable    = self.greenhouse_variable,
                                                    value       = i,
                                                    command     = self.updateGreenhouse,
                                                    width       = 30, 
                                                    height      = 3,  
                                                    font        = font.Font(size = 12))
            self.greenhouse_buttons[i].grid(        row         = int(i / 10),
                                                    column      = (i % 10 + 3))

        # Making the Tub buttons
        for i in range(self.gh_format["tub-per-greenhouse"]):
            self.tub_buttons[i] = tk.Radiobutton(self.tub_frame)
            self.tub_buttons[i].configure(  text        = "Tub %02d"%(i + 1),
                                            indicatoron = 0,
                                            variable    = self.tub_variable,
                                            value       = i,
                                            background  = "#aaa",
                                            command     = self.updateTub,
                                            padx        = 0,
                                            width       = 15, 
                                            height      = 3,  
                                            font        = font.Font(size = 12))
            self.tub_buttons[i].grid(       row         = int(i / 10),
                                            column      = (i % 10 + 3))

        # Making the Actio Buttons
        for i in range(len(actions_in_order)):
            action = actions_in_order[i]
            self.action_button[i] = tk.Radiobutton(self.action_frame, text=action)
            self.action_button[i].configure(indicatoron         = 0,
                                            background          = action_colors[action][0], 
                                            activebackground    = action_colors[action][1],
                                            selectcolor         = action_colors[action][1], 
                                            foreground          = action_colors[action][2], 
                                            activeforeground    = action_colors[action][2],
                                            command             = lambda a=action: self.updateAction(a),
                                            variable            = self.action_state,
                                            value               = action,
                                            width               = 25, 
                                            height              = 3,  
                                            font                = font.Font(size = 15))
            self.action_button[i].grid(     row     = (i + 1),
                                            column  = 0)

    def updateGreenhouse(self):
        self.updateTub()

    def updateTub(self):
        print("saving: %s"%self.tub_filename)
        self.saveTub()
        self.tub_filename = "%s-%s.csv"%(self.gh_format["greenhouse names"][self.greenhouse_variable.get()], self.tub_variable.get() + 1)
        self.tub_filepath = data_folder + file_separator + self.tub_filename
        self.loadTub()

    def updatePot(self, pot_number):
        print(self.plant_data[pot_number])
        current_action = self.action_state.get()

        if current_action == "Rename Pot":
            new_name = PlantNameInput(tk.Tk()).getName()
            if new_name != "":
                self.plant_data[pot_number][0] = new_name
                print(self.plant_data[pot_number])
                self.setPotText(pot_number, new_name, self.getLatestPlantDate(pot_number))
            return

        # test to make sure action is the next logical action to perform
        action_index = file_header.index(current_action)
        if self.plant_data[pot_number][action_index-1] != "" and self.plant_data[pot_number][action_index] == "":
            self.plant_data[pot_number][action_index] = todays_date
            self.setPotText(pot_number, self.plant_data[pot_number][0], todays_date)
            self.setPotColors(pot_number, current_action)
        print(self.plant_data[pot_number])

    def updateAction(self, action):
        self.action_state.set(action)
        print(self.action_state.get())

    def setPotText(self, pot_number, name = "", date = ""):
        self.pot_text[pot_number].set("%s\nPot %02d\n%s"%(name, pot_number + 1, date))

    def setPotColors(self, pot_number, action):
        self.pot_buttons[pot_number].configure( background =        action_colors[action][0], 
                                    activebackground =  action_colors[action][1], 
                                    foreground =        action_colors[action][2], 
                                    activeforeground =  action_colors[action][2])

    def getLatestPlantDate(self, pot_number):
        index = self.plant_data[pot_number].index("") - 1
        if index == 1: 
            return ""
        else:
            return self.plant_data[pot_number][index]

    def resetPot(self, pot_number):
            self.pot_text[pot_number].set("\nPot %02d\n"%(pot_number + 1))
            self.pot_buttons[pot_number].configure( background = "#d9d9d9", 
                                        activebackground = "#ffffff", 
                                        foreground = "black", 
                                        activeforeground = "black")

    def resetTub(self):
        for i in range(self.gh_format["pot-per-tub"]):
            self.resetPot(i)

    def removePotButtons(self):
        for pot in self.pot_buttons:
            pot.grid_forget()

    def initializeWindow(self, first_line):
        for metric in first_line:
            attribute, number = metric.split(":")
            self.gh_format[attribute.strip().lower()] = int(number)

        # refresh the window to remove unecessary buttons and resize properly
        try:
            self.removePotButtons()
        except:
            pass

        self.pot_text =             [tk.StringVar() for i in range(self.gh_format["pot-per-tub"])]
        self.plant_data =           [None for _ in range(self.gh_format["pot-per-tub"])]
        self.greenhouse_buttons =   [None for _ in range(self.gh_format["greenhouse count"])]
        self.tub_buttons =          [None for _ in range(self.gh_format["tub-per-greenhouse"])]
        self.pot_buttons =          [None for _ in range(self.gh_format["pot-per-tub"])]
        self.action_button =        [None for _ in range(len(actions_in_order))]

        self.makePotButtons()

    def loadTub(self):
        if self.tub_filename not in os.listdir(data_folder):
            self.removePotButtons()
            print("%s does not exist in %s"%(self.tub_filename, data_folder))
            return

        with open(self.tub_filepath, "r") as ifile:

            # first get information about tub layout
            first_line = ifile.readline().strip().split(",")
            self.initializeWindow(first_line)

            if ",".join(file_header) != ifile.readline().strip():
                print("Improper header")
                return

            for line in ifile:
                split_line = line.strip().split(",")
                if split_line[1] == "": continue
                pot_number = int(split_line[1]) - 1
                self.plant_data[pot_number] = split_line

            for pot_number, plant in enumerate(self.plant_data):
                if plant == None:
                    self.plant_data[pot_number] = ["" for _  in file_header]
                    # will add an entry for the empty pots for future editing...
                    self.plant_data[pot_number][1] = str(pot_number + 1)
                    continue

                latest_date_index = plant.index("") - 1 #last date that was updated, used to set the color
                if latest_date_index <= 1: #no date exists
                    self.setPotText(pot_number, plant[0])
                else:
                    self.setPotText(pot_number, plant[0], plant[latest_date_index])
                    self.setPotColors(pot_number, file_header[latest_date_index])

    def saveTub(self):
        if self.tub_filename not in os.listdir(data_folder):
            #stupid hack, for some reason, without this if statement, a new file would be made from the data that the tub switched from
            print("can't save a file that doesn't have a file existing already")
            return
        with open(self.tub_filepath, "w") as ofile:
            ofile.write("pot-per-tub: %s,pot rows: %s,pot columns: %s\n"%(self.gh_format["pot-per-tub"], self.gh_format["pot rows"], self.gh_format["pot columns"]))
            ofile.write(",".join(file_header) + "\n")
            for plant in self.plant_data:
                ofile.write(",".join(plant) + "\n")

        print("Tub Saved")

    def updateTubAppends(self, filepath):
        pot_info = None
        headline = None
        temp_line_list = [None]*self.gh_format["pot-per-tub"]
        with open(filepath, "r") as file:
            pot_info = file.readline()
            headline = file.readline()
            for line in file:
                temp_line_list[int(line.split(",")[1]) - 1] = line

        with open(filepath,"w") as file:
            file.write(pot_info)
            file.write(headline)
            for line in temp_line_list:
                file.write(line)

    def exportMaster(self):
        print("Export beginning to %s"%export_filename)
        self.saveTub()

        master_file = open(export_filename, "w")
        titles = [file_header[0]] + ["Greenhouse","Tub Number"] + [i for i in file_header[1:]]
        master_file.write(",".join(titles) + "\n")

        for file in os.listdir(data_folder):
            # print(file[:file.index(".csv")])
            try:
                gh_text, tub_text = file[:file.index(".csv")].split("-")
            except:
                raise Exception("File: %s should not exist in the folder: %s"%(file, data_folder))

            with open(data_folder + file_separator + file) as tub_file:
                tub_file.readline()
                tub_file.readline()
                for line in tub_file:
                    split_line = line.split(",")
                    new_line = [split_line[0]] + [gh_text, tub_text] + [i for i in split_line[1:]]
                    #print(new_line)
                    master_file.write(",".join(new_line))

        master_file.close()

        print("Exporting finished")

    def importMaster(self):
        if import_filename not in os.listdir():
            print("File does not exist\n")
            return

        ifile = open(import_filename, "r")

        first_line = ifile.readline().strip().split(",")
        titles = [first_line[0]] + first_line[3:]
        if tuple(titles) != file_header:
            print("Titles are not correct, should be:\n\n%s\n"%",".join(file_header))
            return

        modified_file_paths = []
        if ContinueQuestion(tk.Tk()).getAnswer():
            print("File import commencing from %s"%import_filename)
            for line in ifile:
                split_line = line.strip().split(",")
                filename = "-".join(split_line[1:3]) + ".csv"
                filepath = data_folder + file_separator + filename
                
                if filepath not in modified_file_paths: #so that we don't have to later update all the files in the folder
                    modified_file_paths.append(filepath)

                if filename not in os.listdir(data_folder):
                    with open(filepath, "w") as file:
                        file.write(",".join(file_header) + "\n")

                newline = [split_line[0]] + split_line[3:] + ["\n"]
                with open(filepath, "a") as file:
                    file.write(",".join(newline))
            print("File import finished")

        for file in modified_file_paths:
            self.updateTubAppends(file)
        # Need to merge the files, overwriting old data with new data

        ifile.close()

        #make a fresh blank template
        with open(import_filename, "w") as file:
            file.write(",".join(first_line) + "\n")

        self.loadTub()

def main():
    root = tk.Tk()
    greenhouse_gui = MainWindow(root)
    root.mainloop()
    greenhouse_gui.exportMaster()


if __name__ == '__main__':
    main()