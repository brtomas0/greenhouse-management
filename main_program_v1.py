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

action_colors = {   "Pot Info" :        ("#000", "#222", "#fff"),
                    "Into Soil" :       ("#751", "#862", "#fff"),
                    "Into Greenhouse" : ("#050", "#262", "#fff"),
                    "Into Pots" :       ("#080", "#292", "#000"),
                    "Begin Flowering" : ("#0c0", "#2d2", "#000"),
                    "End Flowering" :   ("#9d0", "#ae2", "#000"),
                    "End Maturation" :  ("#dd0", "#ee2", "#000"),
                    "Harvested" :       ("#aa0", "#bb2", "#000")}
actions_in_order = ["Pot Info", "Into Soil", "Into Greenhouse", "Into Pots", "Begin Flowering", "End Flowering", "End Maturation", "Harvested"]
export_filename = "Greenhouse_Summary.csv"
import_filename = "New_Greenhouse_Data.csv"
data_folder = "Tub_data"

class MainWindow():

    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.gh_format = {  "greenhouse count" : 4,
                            "tub-per-greenhouse" : 20,
                            "tub rows" : 5,
                            "tub columns" : 4,
                            "pot-per-tub" : 60,
                            "pot rows" : 6,
                            "pot columns" : 10}

        self.gh_format["greenhouse names"] = ["GH%01d%s"%(int(i/2)+1, ["E","W"][i%2]) for i in range(self.gh_format["greenhouse count"])]
        print(self.gh_format["greenhouse names"])

        self.plant_data = [None] * self.gh_format["pot-per-tub"] #stores the plant data from the file

        self.initializeVariables()
        self.initializeButtons()

    def initializeVariables(self):
        self.pot_text = [tk.StringVar() for i in range(self.gh_format["pot-per-tub"])]

        self.greenhouse_variable = tk.IntVar()
        self.tub_variable = tk.IntVar()
        self.action_state = tk.StringVar()

        self.greenhouse_variable.set(0)
        self.tub_variable.set(0)
        self.action_state.set("Pot Info")

        self.greenhouse_list = [None] * self.gh_format["greenhouse count"]
        self.tub_list = [None] * self.gh_format["tub-per-greenhouse"]
        self.pot_list = [None] * self.gh_format["pot-per-tub"]
        self.action_button = [None] * len(actions_in_order)

    def initializeButtons(self):
        # self.import_button = tk.Button(self.frame, text = "Import File from:\n%s"%import_filename, width = self.button_width * 2, height = self.button_height, command = self.importMaster, font = self.label_font)
        # self.import_button.grid(row = 1, column = 0)

        button_style = {"width" : 15, "height" : 3, "font" : font.Font(size = 12)}

        start_row = 1
        for i in range(self.gh_format["greenhouse count"]):
            self.greenhouse_list[i] = tk.Radiobutton(self.frame, button_style)
            self.greenhouse_list[i].configure(  text = self.gh_format["greenhouse names"][i],
                                                indicatoron = 0,
                                                variable = self.greenhouse_variable,
                                                value = i,
                                                command = self.updateGreenhouse,)
            self.greenhouse_list[i].grid(       row = (int(i / 10) + start_row),
                                                column = (i % 10 + 3))

        start_row = 2
        for i in range(self.gh_format["tub-per-greenhouse"]):
            self.tub_list[i] = tk.Radiobutton(self.frame, button_style)
            self.tub_list[i].configure( text = "Tub %02d"%(i + 1),
                                        indicatoron = 0,
                                        variable = self.tub_variable,
                                        value = i,
                                        background = "#aaa",
                                        command = self.updateTub,)
            self.tub_list[i].grid(      row = (int(i / 10) + start_row),
                                        column = (i % 10 + 3))

        start_row = start_row + 2
        for i in range(self.gh_format["pot-per-tub"]):
            self.pot_list[i] = tk.Button(self.frame, button_style)
            self.pot_list[i].configure( textvariable = self.pot_text[i],
                                        command = lambda a=i: self.updatePot(a))
            self.pot_list[i].grid(      row = (i % self.gh_format["pot rows"] + start_row),
                                        column = (int( i / self.gh_format["pot rows"] ) + 3))

        for i in range(len(actions_in_order)):
            action = actions_in_order[i]
            self.action_button[i] = tk.Radiobutton(self.frame, text=action)
            self.action_button[i].configure(indicatoron         = 0,
                                            background          = action_colors[action][0], 
                                            activebackground    = action_colors[action][1],
                                            selectcolor         = action_colors[action][1], 
                                            foreground          = action_colors[action][2], 
                                            activeforeground    = action_colors[action][2], 
                                            width               = button_style["width"] * 2, 
                                            height              = int(button_style["height"]),
                                            command             = lambda a=action: self.updateAction(a),
                                            variable            = self.action_state,
                                            value               = action,
                                            font                = button_style["font"])
            self.action_button[i].grid(     row = (i+2),
                                            column = 0)

    def updateGreenhouse(self):
        self.importTub()

    def updateTub(self):
        self.importTub()

    def updatePot(self, i):
        print("%s pot_updated"%i)

    def updateAction(self, action):
        self.action_state.set(action)
        print(self.action_state.get())

    def setPotText(self, pot_number, name = "", date = ""):
        self.pot_text[pot_number].set("%s\nPot %02d\n%s"%(name, pot_number + 1, date))

    def importTub(self):
        filename = "%s-%s.csv"%(self.gh_format["greenhouse names"][self.greenhouse_variable.get()], self.tub_variable.get() + 1)
        filepath = data_folder + file_separator + filename

        if filename not in os.listdir(data_folder):
            print("%s does not exist in %s"%(filename, data_folder))
            return

        with open(filepath, "r") as ifile:
            if ",".join(file_header) != ifile.readline().strip():
                print("Improper header")
                return

            for line in ifile:
                split_line = line.strip().split(",")
                pot_number = int(split_line[1]) - 1
                self.plant_data[pot_number] = split_line

                latest_date_index = split_line.index("") - 1
                if latest_date_index == 1: #no date exists
                    self.setPotText(pot_number, split_line[0])
                    continue
                self.setPotText(pot_number, split_line[0], split_line[latest_date_index])

    def updateTubAppends(self, filepath):
        headline = None
        temp_line_list = [None]*self.number_of_pots
        with open(filepath, "r") as file:
            headline = file.readline()
            for line in file:
                temp_line_list[int(line.split(",")[1]) - 1] = line

        with open(filepath,"w") as file:
            file.write(headline)
            for line in temp_line_list:
                file.write(line)



def main():
    root = tk.Tk()
    greenhouse_gui = MainWindow(root)
    root.mainloop()
    # greenhouse_gui.exportMaster()


if __name__ == '__main__':
    main()