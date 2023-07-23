#Ich werde diesen Weg Deutsch lernen

import numpy as np
from tkinter import *
from tkinter import ttk
import random
import pandas as pd
import os
import os.path
import time
import matplotlib.pyplot as plt

root = Tk()

#initially create the score tracking text file - only created once
path = 'historical_scores.txt'
check_file = os.path.isfile(path) #this is a BOOL variable

if check_file == False:
   with open('historical_scores.txt', 'w') as f:
      pass
else:
   pass

##########################################SET PARAMETERS##########################################################################################################

screen_scaler = 1.25 #this is just an int to scale the screen size. If want regular screen size, this value should be set to 1

screen_width = root.winfo_screenwidth() 
screen_height = root.winfo_screenheight()  #the purpose of -50 is to allow for space where the taskbar is on the bottom of the computer

screen_width_scaled = int(screen_width/screen_scaler)
screen_height_scaled = int(screen_height/screen_scaler)

screen_width_string = str(screen_width_scaled)
screen_height_string = str(screen_height_scaled)

gui_size = screen_width_string + "x" + screen_height_string

root.geometry(gui_size) #allows x,y size of GUI window to be set in terms of pixel number
root.resizable(True, True)
root.configure(background = 'gray89')

root.title("GERMAN SUCKS")

####################################################CREATE TABS####################################################################################################

master_notebook = ttk.Notebook(root)
master_notebook.grid(row = 0, column = 0)

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook.Tab', background = "gray70", font = ('Helvetica','14'))
style.map("TNotebook", background= [("selected", "gray70")])


#now start to create frames - these will be the tabs within the notebook (the different pages of the app)
page_1 = Frame(master_notebook, width = screen_width_scaled, height = screen_height_scaled, bg = 'gray89')
page_1.pack(fill = "both", expand = 1)
master_notebook.add(page_1, text = "Vocabulary: E -> G")

page_2 = Frame(master_notebook, width = screen_width_scaled, height = screen_height_scaled, bg = 'gray89')
page_2.pack(fill = "both", expand = 1)
master_notebook.add(page_2, text = "Vocabulary: G -> E")

##################################################PAGE 1#############################################################################################################
#build up page 1

number_of_words_attempted = 0

##ADD IN RE-TEST LOGIC
#global word_wrong_iterator
#global word_was_wrong
word_was_wrong = False
word_wrong_iterator = 0

def random_word_selector():

   global german_word
   global english_word
   global english_word_label
   global german_word_label

   global word_wrong_iterator

   print(word_was_wrong)
   print(word_wrong_iterator)

   #LOGIC FOR RE-TEST
   if word_was_wrong == True and word_wrong_iterator < 2:
      global number_of_words_attempted

      word_wrong_iterator = word_wrong_iterator + 1

      generate_word_button['state'] = DISABLED

      english_word, german_word = random.choice(list(english_to_german_dict.items()))
      #now display english word on screen and prompt german word entry
      german_word_label = Label(page_1, text = f"{german_word}", font= 25)
      german_word_label.place(relx=0.5, rely=0.35, anchor="center")

      number_of_words_attempted = number_of_words_attempted + 1

   elif word_was_wrong == True and word_wrong_iterator == 2:
      word_wrong_iterator = word_wrong_iterator + 1 #this pushes it to 3

      #global english_word
      english_word = wrong_word_english
      german_word = wrong_word

      german_word_label = Label(page_1, text = f"{wrong_word}", font= 25)
      german_word_label.place(relx=0.5, rely=0.35, anchor="center")

      #global number_of_words_attempted
      number_of_words_attempted = number_of_words_attempted + 1
   
   else:

      generate_word_button['state'] = DISABLED

      english_word, german_word = random.choice(list(english_to_german_dict.items()))
      #now display english word on screen and prompt german word entry
      german_word_label = Label(page_1, text = f"{german_word}", font= 25)
      german_word_label.place(relx=0.5, rely=0.35, anchor="center")

      #global number_of_words_attempted
      number_of_words_attempted = number_of_words_attempted + 1

generate_word_button = Button(page_1, text = "Generate German Word", command = random_word_selector)
generate_word_button.place(relx = 0.5, rely = 0.3, anchor = "center")

#create entry field
word_entry = Entry(page_1, width = 50)
word_entry.place(relx = 0.5, rely = 0.5, anchor = 'center')

#create insert buttons for the extra german characters
def a_button_function():
   word_entry.insert(len(word_entry.get()), "ä")

def capital_a_button_function():
   word_entry.insert(len(word_entry.get()), "Ä")

def o_button_function():
   word_entry.insert(len(word_entry.get()), "ö")

def capital_o_button_function():
   word_entry.insert(len(word_entry.get()), "Ö")

def u_button_function():
   word_entry.insert(len(word_entry.get()), "ü")

def capital_u_button_function():
   word_entry.insert(len(word_entry.get()), "Ü")

def sharp_s_function():
   word_entry.insert(len(word_entry.get()), "ß")

a_button = Button(page_1, text = "ä", command=a_button_function)
a_button.place(relx=0.7, rely=0.3, anchor="center")

capital_a_button = Button(page_1, text = "Ä", command=capital_a_button_function)
capital_a_button.place(relx=0.7, rely=0.27, anchor="center")

o_button = Button(page_1, text = "ö", command=o_button_function)
o_button.place(relx=0.72, rely=0.3, anchor="center")

capital_o_button = Button(page_1, text = "Ö", command=capital_o_button_function)
capital_o_button.place(relx=0.72, rely=0.27, anchor="center")

u_button = Button(page_1, text = "ü", command=u_button_function)
u_button.place(relx=0.74, rely=0.3, anchor="center")

capital_u_button = Button(page_1, text = "Ü", command=capital_u_button_function)
capital_u_button.place(relx=0.74, rely=0.27, anchor="center")

sharp_s_button = Button(page_1, text = "ß", command=sharp_s_function)
sharp_s_button.place(relx=0.68, rely=0.285, anchor="center")

#other stuff
correct_counter = 0 #counts the numbers of correct answers
incorrect_counter = 0

correct_label = Label(page_1, text = "Correct Answers:")
correct_label.place(relx=0.3, rely=0.2, anchor="e")
correct_number_label = Label(page_1, text = f"{correct_counter}")
correct_number_label.place(relx=0.31, rely=0.2, anchor="center")

incorrect_label = Label(page_1, text = "Incorrect Answers:")
incorrect_label.place(relx= 0.3, rely=0.24, anchor="e")
incorrect_number_label = Label(page_1, text = f"{incorrect_counter}")
incorrect_number_label.place(relx = 0.31, rely=0.24, anchor="center")

def submit_function():
   #print(english_word)
   word_guess = word_entry.get()
   global word_wrong_iterator
   global word_was_wrong

   if word_guess == english_word and word_was_wrong == False:
      global correct_counter
      global correct_number_label

      correct_label = Label(page_1, text = "DU BIST NICHT BEHINDERT", font=35, fg = 'green')
      correct_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)
      german_word_label.destroy()
      correct_label.destroy()

      #again enable button
      generate_word_button['state'] = NORMAL
      #also clear the entry field
      word_entry.delete(0, END)

      #global correct_counter
      #global correct_number_label

      correct_counter = correct_counter + 1
      correct_number_label.destroy()
      correct_number_label = Label(page_1, text = f"{correct_counter}")
      correct_number_label.place(relx=0.31, rely=0.2, anchor="center")
      root.update()
   elif word_guess != english_word and word_was_wrong == False:
      incorrect_label = Label(page_1, text = "DU BIST BEHINDERT", font=35, fg = 'red')
      incorrect_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)

      incorrect_label.destroy()
      #word_entry.delete(0, END) #maybe don't clear the entry field
   elif word_guess == english_word and word_wrong_iterator != 3 and word_was_wrong == True:
      correct_label = Label(page_1, text = "DU BIST NICHT BEHINDERT", font=35, fg = 'green')
      correct_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)
      german_word_label.destroy()
      correct_label.destroy()

      #again enable button
      generate_word_button['state'] = NORMAL
      #also clear the entry field
      word_entry.delete(0, END)

      correct_counter = correct_counter + 1
      correct_number_label.destroy()
      correct_number_label = Label(page_1, text = f"{correct_counter}")
      correct_number_label.place(relx=0.31, rely=0.2, anchor="center")
      root.update()
   elif word_guess == english_word and word_wrong_iterator == 3 and word_was_wrong == True:
      #global word_was_wrong
      word_was_wrong = False
      word_wrong_iterator = 0

      correct_label = Label(page_1, text = "DU BIST NICHT BEHINDERT", font=35, fg = 'green')
      correct_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)
      german_word_label.destroy()
      correct_label.destroy()

      #again enable button
      generate_word_button['state'] = NORMAL
      #also clear the entry field
      word_entry.delete(0, END)

      #global correct_counter
      #global correct_number_label

      correct_counter = correct_counter + 1
      correct_number_label.destroy()
      correct_number_label = Label(page_1, text = f"{correct_counter}")
      correct_number_label.place(relx=0.31, rely=0.2, anchor="center")
      root.update()
   elif word_guess != english_word and word_wrong_iterator == 3 and word_was_wrong == True:
      #so here is what happens if you get it wrong a second time
      #keep the boolean as true but reset the iterator so it retests again in a few turns
      word_was_wrong = True
      word_wrong_iterator = 0

      #and then the normal wrong actions
      incorrect_label = Label(page_1, text = "DU BIST BEHINDERT", font=35, fg = 'red')
      incorrect_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)

      incorrect_label.destroy()


   elif word_guess != english_word and word_wrong_iterator != 3 and word_was_wrong == True:
      incorrect_label = Label(page_1, text = "DU BIST BEHINDERT", font=35, fg = 'red')
      incorrect_label.place(relx=0.5, rely=0.4, anchor="center")
      root.update()
      time.sleep(1)

      incorrect_label.destroy()
      #word_entry.delete(0, END) #maybe don't clear the entry field



submit_button = Button(page_1, text = "SUBMIT", command = submit_function)
submit_button.place(relx = 0.6, rely = 0.5, anchor="center")

#wrong_again = False

def skip_function():

   #if word_was_wrong == True: #so if this has already been true and not reset yet and you press again, as in getting this word wrong a second time
      #wrong_again = True

   #BUILD IN RE-TEST LOGIC
   global wrong_word
   wrong_word = german_word
   global wrong_word_english
   wrong_word_english = english_word
   global word_was_wrong
   word_was_wrong = True

   #set this back to 0
   global word_wrong_iterator
   word_wrong_iterator = 0

   ##################################################
   generate_word_button["state"] = NORMAL
   root.update()

   global incorrect_counter
   global incorrect_number_label

   incorrect_counter = incorrect_counter + 1
   incorrect_number_label.destroy()
   incorrect_number_label = Label(page_1, text = f"{incorrect_counter}")
   incorrect_number_label.place(relx=0.31, rely=0.24, anchor="center")
   root.update()

   the_answer_was = Label(page_1, text = f"{english_word}", font=35, fg = 'blue')
   the_answer_was.place(relx=0.5, rely=0.4, anchor="center")
   root.update()
   time.sleep(3)
   the_answer_was.destroy()
   german_word_label.destroy()
   root.update()


skip_button = Button(page_1, text = "SKIP", command=skip_function)
skip_button.place(relx = 0.65, rely=0.5, anchor="center")

#also create function to generate a text file with your score for the day
def output_score():

   score_percentage = str((correct_counter/number_of_words_attempted)*100)
   score_string = score_percentage + "," + str(number_of_words_attempted)

   with open('historical_scores.txt', 'r') as f:
      lines = f.readlines()

   with open('historical_scores.txt', 'w') as f:
      f.writelines(lines)
      f.writelines(score_string + '\n')

   root.quit()
   #so HERE:
       #TWO THINGS: first thing is each time generate a new text file with all the results from the most recent run

output_score_button = Button(page_1, text = "Finish & Output Data File", command=output_score)
output_score_button.place(relx=0.5, rely=0.6, anchor="center")


def plot_historical_data():
   with open('historical_scores.txt', 'r') as f:
      read_data = f.readlines()
      #sort data into arrays for plotting

      score_value = []
      #score_value = np.array(score_value)
      number_of_questions_value = []
      #number_of_questions_value = np.array(number_of_questions_value)

      for object in read_data:
         cleaned = object.strip() #strip out bloody newline characters
         cleaned = cleaned.split(",")

         score_value.append(cleaned[0])
         number_of_questions_value.append(cleaned[1]) #keep as strings cause will use for titles in bar chart

         score_value = [float(x) for x in score_value]
         #number_of_questions_value = [float(x) for x in number_of_questions_value]

   plt.bar(number_of_questions_value, score_value, color='blue', edgecolor='black')
   plt.xlabel('Number of Questions Attempted')
   plt.ylabel('Percentage Score')
   plt.title('Du Wirst Weniger Behindert Sein')
   plt.show()

plot_button = Button(page_1, text = "Plot Historical Data", command=plot_historical_data)
plot_button.place(relx=0.8, rely=0.6, anchor="center")

#####################################################DATA STRUCTURES##############################################################################################

#can define dictionary out here?

#try excel import dictionary method using PANDAS
english_to_german_dict = {}

df = pd.read_csv('dictionary.csv', encoding= 'unicode_escape') #had to add in this encoding thing, must be because of the weird german alphabet
dict_english_words = df['English Word']
dict_german_words = df['German Word']

dict_fill_iterator = 0
while dict_fill_iterator <= len(dict_english_words) - 1:

   english_to_german_dict[dict_english_words[dict_fill_iterator]] = dict_german_words[dict_fill_iterator]

   dict_fill_iterator = dict_fill_iterator + 1

#######################################################LOOP######################################################################################################33
root.mainloop() #loop the window
