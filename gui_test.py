import tkinter as tk
import os, time

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
					"Into Soil" : 		("#050", "#272", "#fff"),
					"Into Greenhouse" : ("#070", "#292", "#000"),
					"Into Pots" : 		("#0a0", "#2c2", "#000"),
					"Begin Flowering" : ("#0d0", "#2f2", "#000"),
					"End Flowering" : 	("#8d0", "#af2", "#000"),
					"End Maturation" : 	("#ad0", "#cf2", "#000"),
					"Harvested" : 		("#dd0", "#ff2", "#000")}

actions_in_order = ["Pot Info", "Into Soil", "Into Greenhouse", "Into Pots", "Begin Flowering", "End Flowering", "End Maturation", "Harvested"]
data_folder = "Tub_data"


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

		self.buttonInitilize()
		self.resetTub()

	def buttonInitilize(self):
		self.current_state_label = tk.Label(self.frame, textvariable = self.action_state)
		self.current_state_label.grid(row = 0, column = 3)
		self.current_date_label = tk.Label(self.frame, text = todays_date)
		self.current_date_label.grid(row = 0, column = 4)
		self.update_button = tk.Button(self.frame, text = "Update", width = self.button_width, height = self.button_height, command = self.importFile)
		self.update_button.grid(row = 0, column = 0)
		self.reset_button = tk.Button(self.frame, text = "Reset", width = self.button_width, height = self.button_height, command = self.resetTub)
		self.reset_button.grid(row = 1, column = 0)

		start_row = 1
		for i in range(self.number_of_greenhouses):
			self.greenhouse_list[i] = tk.Radiobutton(self.frame, text = "GH%01d-%s"%(int(i / 2) + 1, "E" * (i % 2) + "W" * ((i+1) % 2) ))
			self.greenhouse_list[i].configure(	indicatoron = 0,
												width = self.button_width, 
												height = self.button_height,
												variable = self.greenhouse_variable,
												value = i,
												command = self.updateGreenhouse)
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
										command = self.updateTub)
			self.tub_list[i].grid(		row = (int(i / 10) + start_row),
										column = (i % 10 + 3))

		start_row = start_row + 2
		for i in range(self.number_of_pots):
			self.pot_list[i] = tk.Button(self.frame)
			self.pot_list[i].configure(	textvariable = self.pot_text[i],
										command = lambda a=i: self.updatePot(a),
										width = self.button_width, 
										height = self.button_height)
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
											height 				= self.button_height,
											command 			= lambda a=action: self.updateAction(a),
											variable 			= self.action_state,
											value				= action)
			self.action_button[i].grid(		row = (i+2),
											column = 0)

	def updateGreenhouse(self):
		self.importFile()

	def updateTub(self):
		self.importFile()

	def updatePot(self, i):
		#print("Pot Number is: %s"%(i+1))
		if self.action_state.get() == "Pot Info":
			return

		is_data_updated = False

		state_colors = action_colors[self.action_state.get()]
		new_name_list = self.pot_text[i].get().split("\n")
		new_name = "\n".join((new_name_list[0], new_name_list[1], todays_date))

		gh = self.greenhouse_variable.get()
		tub = self.tub_variable.get()
		filename =  "GH%01d%s-%s.csv"%(int(gh / 2) + 1, "E" * (gh % 2) + "W" * ((gh +1) % 2), tub + 1)
		file_path = data_folder + "\\" + filename
		#print("Searching in " + filename)

		temp_file = open("Tub_data/temp_tub.csv", "w")
		with open(file_path, "r") as ifile:
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

		os.remove(file_path)
		os.rename("Tub_data/temp_tub.csv", file_path)
		self.pot_text[i].set(new_name)
		self.pot_list[i].configure(	background = state_colors[0], 
									activebackground = state_colors[1], 
									foreground = state_colors[2], 
									activeforeground = state_colors[2])
	
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
		for i in range(self.number_of_pots): 
			self.pot_text[i].set("\nPot %02d\n"%(i+1))
			self.pot_list[i].configure(	background = "SystemButtonFace", 
										activebackground = "SystemButtonHighlight", 
										foreground = "black", 
										activeforeground = "black")

	def updateAction(self, action):
		self.action_state.set(action)
		print(self.action_state.get())

	def importFile(self):
		gh = self.greenhouse_variable.get()
		tub = self.tub_variable.get()
		#"%s\nPot %02d\n%s"%(self.plant_names[i].get(), i + 1, self.plant_dates[i].get())
		self.resetTub()
		filename =  "GH%01d%s-%s.csv"%(int(gh / 2) + 1, "E" * (gh % 2) + "W" * ((gh +1) % 2), tub + 1)
		file_path = data_folder + "\\" + filename
		print("importing " + filename)
		
		if filename not in os.listdir(data_folder):
			print("Not Found")
			return

		with open(file_path) as ifile:
			ifile.readline()
			for line in ifile:
				data_list = line.rstrip().split(",")
				name = data_list[0]
				pot_number = int(data_list[1]) - 1
				latest_date_index = data_list.index("") - 1
				latest_date = data_list[latest_date_index]
				self.pot_text[pot_number].set("%s\nPot %02d\n%s"%(name, pot_number + 1, latest_date))
				self.action_state.set(info_list[latest_date_index])
				self.setPot(pot_number)
				#rint(self.pot_text[pot_number].get())
		self.action_state.set(info_list[0])
		return

def main():
	root = tk.Tk()
	Program(root)
	root.mainloop()


if __name__ == '__main__':
	main()