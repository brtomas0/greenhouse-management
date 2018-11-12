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
info_list =	 (	"Plant Id",
				"Pot Number",
				"Into Soil",
				"Into Greenhouse",
				"Into Pots",
				"Begin Flowering",
				"End Flowering",
				"End Maturation",
				"Harvested",
				"Plant State")

action_colors = {	"Pot Info" :		("#000", "#222", "#fff"),
					"Into Soil" : 		("#751", "#862", "#fff"),
					"Into Greenhouse" : ("#050", "#262", "#fff"),
					"Into Pots" : 		("#080", "#292", "#000"),
					"Begin Flowering" : ("#0c0", "#2d2", "#000"),
					"End Flowering" : 	("#9d0", "#ae2", "#000"),
					"End Maturation" : 	("#dd0", "#ee2", "#000"),
					"Harvested" : 		("#aa0", "#bb2", "#000")}

actions_in_order = ["Pot Info", "Into Soil", "Into Greenhouse", "Into Pots", "Begin Flowering", "End Flowering", "End Maturation", "Harvested"]
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

class Program():

	def __init__(self, master):

		self.frame = tk.Frame(master)
		self.frame.pack()

		self.number_of_greenhouses = 4
		self.number_of_tubs = 20
		self.number_of_pots = 60

		self.greenhouse_list = [None] * self.number_of_greenhouses
		self.tub_list = [None] * self.number_of_tubs
		self.pot_list = [None] * self.number_of_pots
		self.pot_text = [tk.StringVar() for i in range(self.number_of_pots)]

		self.current_tub = 0
		self.greenhouse_variable = tk.IntVar()
		self.tub_variable = tk.IntVar()

		self.action_button = [None] * len(actions_in_order)
		self.action_state = tk.StringVar()
		self.action_state.set("Pot Info")

		self.tub_rows = 6
		self.tub_columns = 10
		self.app_rows = 8
		self.app_columns = 12
		self.button_width = 15
		self.button_height = 3
		self.pot_font = font.Font(size = 12)
		self.label_font = font.Font(size = 12)

		self.buttonInitilize()
		self.importTub()

	def buttonInitilize(self):
		#self.current_state_label = tk.Label(self.frame, textvariable = self.action_state, font = self.label_font)
		#self.current_state_label.grid(row = 0, column = 3)
		#self.current_date_label = tk.Label(self.frame, text = todays_date, font = self.label_font)
		#self.current_date_label.grid(row = 0, column = 4)
		#self.export_button = tk.Button(self.frame, text = "Export", width = self.button_width, height = self.button_height, command = self.exportMaster, font = self.label_font)
		#self.export_button.grid(row = 0, column = 0)
		self.import_button = tk.Button(self.frame, text = "Import File from:\n%s"%import_filename, width = self.button_width * 2, height = self.button_height, command = self.importMaster, font = self.label_font)
		self.import_button.grid(row = 1, column = 0)

		start_row = 1
		for i in range(self.number_of_greenhouses):
			self.greenhouse_list[i] = tk.Radiobutton(self.frame, text = "GH%01d-%s"%(int(i / 2) + 1, "E" * (i % 2) + "W" * ((i+1) % 2) ))
			self.greenhouse_list[i].configure(	indicatoron = 0,
												width = self.button_width, 
												height = self.button_height,
												variable = self.greenhouse_variable,
												value = i,
												command = self.updateGreenhouse,
												font = self.pot_font)
			self.greenhouse_list[i].grid(		row = (int(i / 10) + start_row),
												column = (i % 10 + 3))

		start_row = 2
		for i in range(self.number_of_tubs):
			self.tub_list[i] = tk.Radiobutton(self.frame, text = "Tub %02d"%(i + 1))
			self.tub_list[i].configure(	indicatoron = 0,
										width = self.button_width, 
										height = self.button_height,
										variable = self.tub_variable,
										value = i,
										background = "#aaa",
										command = self.updateTub,
										font = self.pot_font)
			self.tub_list[i].grid(		row = (int(i / 10) + start_row),
										column = (i % 10 + 3))

		start_row = start_row + 2
		for i in range(self.number_of_pots):
			self.pot_list[i] = tk.Button(self.frame)
			self.pot_list[i].configure(	textvariable = self.pot_text[i],
										command = lambda a=i: self.updatePot(a),
										width = self.button_width, 
										height = self.button_height,
										font = self.pot_font)
			self.pot_list[i].grid(		row = (i % self.tub_rows + start_row),
										column = (int( i / self.tub_rows ) + 3))

		for i in range(len(actions_in_order)):
			action = actions_in_order[i]
			self.action_button[i] = tk.Radiobutton(self.frame, text=action)
			self.action_button[i].configure(indicatoron 		= 0,
											background 			= action_colors[action][0], 
											activebackground 	= action_colors[action][1],
											selectcolor			= action_colors[action][1], 
											foreground 			= action_colors[action][2], 
											activeforeground 	= action_colors[action][2], 
											width 				= self.button_width*2, 
											height 				= int(self.button_height),
											command 			= lambda a=action: self.updateAction(a),
											variable 			= self.action_state,
											value				= action,
											font 				= self.label_font)
			self.action_button[i].grid(		row = (i+2),
											column = 0)

	def updateGreenhouse(self):
		self.importTub()

	def updateTub(self):
		self.importTub()

	def updatePotOriginal(self, i):
		#print("Pot Number is: %s"%(i+1))
		if self.action_state.get() == "Pot Info":
			plant_name = PlantNameInput(tk.Tk()).getName()
			print("new name is: %s"%plant_name)
			return

		is_data_updated = False

		try:
			state_colors = action_colors[self.action_state.get()]
		except KeyError as e:
			print("Could not set colors based on %s"%e)
			return


		new_name_list = self.pot_text[i].get().split("\n")
		new_name = "\n".join((new_name_list[0], new_name_list[1], todays_date))

		gh = self.greenhouse_variable.get()
		tub = self.tub_variable.get()
		filename =  "GH%01d%s-%s.csv"%(int(gh / 2) + 1, "E" * (gh % 2) + "W" * ((gh +1) % 2), tub + 1)
		filepath = data_folder + file_separator + filename
		#print("Searching in " + filename)

		temp_file = open("Tub_data/temp_tub.csv", "w")
		with open(filepath, "r") as ifile:
			for line in ifile:
				if new_name_list[0] in line:
					line_list = line.split(",")
					index = info_list.index(self.action_state.get())

					if line_list[index-1] != "" and line_list[index] == "":
						is_data_updated = True
						line_list[index] = todays_date
						new_line = ",".join(line_list)
						#print(new_line)
						temp_file.write(new_line)
						continue

				temp_file.write(line)
		temp_file.close()

		if not is_data_updated:
			os.remove("Tub_data/temp_tub.csv")
			return

		os.remove(filepath)
		os.rename("Tub_data/temp_tub.csv", filepath)
		self.pot_text[i].set(new_name)
		self.pot_list[i].configure(	background = state_colors[0], 
									activebackground = state_colors[1], 
									foreground = state_colors[2], 
									activeforeground = state_colors[2])
	
	def updatePot(self, i):
		#print("Pot Number is: %s"%(i+1))
		gh = self.greenhouse_variable.get()
		tub = self.tub_variable.get()
		filename =  "GH%01d%s-%s.csv"%(int(gh / 2) + 1, "E" * (gh % 2) + "W" * ((gh +1) % 2), tub + 1)
		filepath = data_folder + file_separator + filename
		if filename not in os.listdir(data_folder):
			print("Cannot update plants that don't exist. Initilize tub by importing from a file.")
			return

		if self.action_state.get() == "Pot Info":
			self.renamePot(i, filepath)
			return
			
		is_data_updated = False

		try:
			state_colors = action_colors[self.action_state.get()]
		except KeyError as e:
			print("Could not set colors based on %s"%e)
			return


		new_name_list = self.pot_text[i].get().split("\n")
		new_name = "\n".join((new_name_list[0], new_name_list[1], todays_date))

		
		#print("Searching in " + filename)
		pot_updated = False
		header = None
		new_line_list = []
		with open(filepath, "r") as ifile:
			header = ifile.readline()
			for line in ifile:
				new_line = line

				if new_name_list[0] in line:
					# only possbly update the plant with the new line
					line_list = line.split(",")
					index = info_list.index(self.action_state.get())

					if line_list[index-1] != "" and line_list[index] == "":
					#making sure that the update is only going to the next stage, and not skipping stages
						pot_updated = True
						line_list[index] = todays_date
						new_line = ",".join(line_list)
						print(new_line)
				new_line_list.append(new_line)

		with open(filepath, "w") as file:
			file.write(header)
			for line in new_line_list: file.write(line)

		if not pot_updated:
			return


		self.pot_text[i].set(new_name)
		self.pot_list[i].configure(	background = state_colors[0], 
									activebackground = state_colors[1], 
									foreground = state_colors[2], 
									activeforeground = state_colors[2])

	def renamePot(self, pot_number, filepath):
		new_plant_name = PlantNameInput(tk.Tk()).getName()
		if new_plant_name == "":
			return
		new_name_list = self.pot_text[pot_number].get().split("\n")
		new_name = "\n".join((new_plant_name, new_name_list[1], todays_date))
		self.pot_text[pot_number].set(new_name)
		current_plant_name = new_name_list[0]
		#print("Searching in " + filename)

		header = None
		new_line_list = []
		with open(filepath, "r") as file:
			header = file.readline()
			for line in file:
				new_line = line

				if new_name_list[0] in line:
					# only possbly update the plant with the new line
					line_list = line.split(",")
					new_line = [new_plant_name] + line_list[1:]
					new_line = ",".join(new_line)
				new_line_list.append(new_line)

		with open(filepath, "w") as file:
			file.write(header)
			for line in new_line_list: file.write(line)

	def setPot(self, i):
		#print("Pot Number is: %s"%(i+1))
		if self.action_state.get() == "Pot Info":
			return
		state_colors = action_colors[self.action_state.get()]
		self.pot_list[i].configure(	background = state_colors[0], 
									activebackground = state_colors[1], 
									foreground = state_colors[2], 
									activeforeground = state_colors[2])

	def resetTub(self):
		if platform.system() == "Windows":
			for i in range(self.number_of_pots): 
				self.pot_text[i].set("\nPot %02d\n"%(i+1))
				self.pot_list[i].configure(	background = "SystemButtonFace", 
											activebackground = "SystemButtonHighlight", 
											foreground = "black", 
											activeforeground = "black")
		elif platform.system() == "Linux":
			for i in range(self.number_of_pots): 
				self.pot_text[i].set("\nPot %02d\n"%(i+1))
				self.pot_list[i].configure(	background = "#d9d9d9", 
											activebackground = "#ffffff", 
											foreground = "black", 
											activeforeground = "black")
		else:
			raise Exception("Operating system is not supported")

	def updateAction(self, action):
		self.action_state.set(action)
		print(self.action_state.get())

	def importTub(self):
		gh = self.greenhouse_variable.get()
		tub = self.tub_variable.get()
		#"%s\nPot %02d\n%s"%(self.plant_names[i].get(), i + 1, self.plant_dates[i].get())
		self.resetTub()
		filename =  "GH%01d%s-%s.csv"%(int(gh / 2) + 1, "E" * (gh % 2) + "W" * ((gh +1) % 2), tub + 1)
		filepath = data_folder + file_separator + filename
		#print("importing " + filename)
		
		if filename not in os.listdir(data_folder):
			print("File Does not exist in %s"%data_folder)
			return

		with open(filepath) as ifile:
			ifile.readline()
			for line in ifile:
				data_list = line.rstrip().split(",")
				name = data_list[0]
				pot_number = int(data_list[1]) - 1
				latest_date_index = data_list.index("") - 1
				if latest_date_index == 1: #no date exists
					self.pot_text[pot_number].set("%s\nPot %02d\n"%(name, pot_number + 1))
					continue

				latest_date = data_list[latest_date_index]
				self.pot_text[pot_number].set("%s\nPot %02d\n%s"%(name, pot_number + 1, latest_date))
				self.action_state.set(info_list[latest_date_index])
				self.setPot(pot_number)
				#print(self.pot_text[pot_number].get())
		self.action_state.set(actions_in_order[0])
		return

	def exportMaster(self):
		print("Export beginning to %s"%export_filename)

		master_file = open(export_filename, "w")
		titles = [info_list[0]] + ["Greenhouse","Tub Number"] + [i for i in info_list[1:]]
		master_file.write(",".join(titles) + "\n")

		for file in os.listdir(data_folder):
			print(file[:file.index(".csv")])
			try:
				gh_text, tub_text = file[:file.index(".csv")].split("-")
			except:
				raise Exception("File: %s should not exist in the folder: %s"%(file, data_folder))

			

			with open(data_folder + file_separator + file) as tub_file:
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
		if tuple(titles) != info_list:
			print("Titles are not correct, should be:\n\n%s\n"%",".join(info_list))
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
						file.write(",".join(info_list) + "\n")

				newline = [split_line[0]] + split_line[3:] + ["\n"]
				with open(filepath, "a") as file:
					file.write(",".join(newline))
			print("File import finished")

		for file in modified_file_paths:
			self.updateTubAppends(file)
		# Need to merge the files, overwriting old data with new data

		ifile.close()
		with open(import_filename, "w") as file:
			file.write(",".join(first_line) + "\n")

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
	greenhouse_gui = Program(root)
	root.mainloop()
	greenhouse_gui.exportMaster()


if __name__ == '__main__':
	main()