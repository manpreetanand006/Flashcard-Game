import tkinter
from tkinter import ttk
from tkinter import messagebox, simpledialog
import random

window = tkinter.Tk()
window.title('FLASHCARD GAME')

bg_image = tkinter.PhotoImage(file="letters1.png")

canvas = tkinter.Canvas(window, width=bg_image.width(), height=bg_image.height())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")

class Flashcards:

    def __init__(self):
        self.flashcards = {}

    def adding_flashcards(self):
        number_of_cards = simpledialog.askstring(title="Input", prompt="How many flashcards you want to add?")
        try:
            if number_of_cards is not None:
                for i in range(int(number_of_cards)):
                    term = simpledialog.askstring(title='Input', prompt=f'Enter the term {i + 1}.')
                    if term in self.flashcards.keys():
                        tkinter.messagebox.showwarning(title='Error', message=f'{term} already exists')
                        term = simpledialog.askstring(title='Input', prompt=f'Enter the term {i + 1}')

                    definition = simpledialog.askstring(title='Input', prompt=f'Enter the Definition {i + 1}')
                    if definition in self.flashcards.values():
                        tkinter.messagebox.showwarning(title='Error', message=f'{definition} already exists')
                        definition = simpledialog.askstring(title='Input', prompt=f'Enter the Definition {i + 1}.')

                    self.flashcards[term.lower()] = definition.lower()
                    i += 1
        except ValueError:
            tkinter.messagebox.showerror(title='Error', message='number of cards should be a number')

    def remove_flashcards(self, term):
        if term in self.flashcards.keys():
            del self.flashcards[term]
            tkinter.messagebox.showinfo(title='Message', message=f'{term} has been removed successfully')
        else:
            tkinter.messagebox.showwarning(title='Error', message=f"Can't remove '{term}': there is no such card")

    def ask_question(self, number_of_questions):
        while number_of_questions > 0:
            question = random.choice(list(self.flashcards.keys()))
            answer = simpledialog.askstring(title='Input', prompt=f"Print the definition of '{question}': ")
            if answer is None:
                break
            elif self.flashcards[question] == answer:
                messagebox.showinfo(title="Message", message="Your answer is right!")
            elif answer in self.flashcards.values():
                for k, v in self.flashcards.items():
                    if answer == v:
                        messagebox.showinfo(
                            title="Message",
                            message=f"Wrong. The right answer is '{self.flashcards[question].title()}', but your definition is correct for '{k}'."
                        )
                        break
            else:
                messagebox.showinfo(
                    title='Message',
                    message=f"Wrong. The right answer is '{self.flashcards[question].title()}'."
                )
            number_of_questions -= 1

    #
    def import_flashcards(self, file_name):
        try:
            with open(file_name, 'r') as flash:
                for line in flash:
                    key, value = line.strip().split(';')
                    self.flashcards[key.lower()] = value.lower()
            tkinter.messagebox.showinfo(title='Message', message="Flashcards imported successfully.")
        except FileNotFoundError:
            tkinter.messagebox.showerror(title='Error', message=f"The file {file_name} does not exist.")
        except IOError as e:
            tkinter.messagebox.showerror(title='Error',
                                         message=f'An error occurred while importing flashcards file: {e}')

    #
    def export_flashcards(self, export_file_name):
        # export_file_name = input("Enter the name of the file you want to export to: ")
        try:
            with open(export_file_name, 'a') as flash3:
                for key, value in self.flashcards.items():
                    flash3.write(key + ';' + value + '\n')
            tkinter.messagebox.showinfo(title = 'Message', message="Flashcards has been exported successfully!")
        except IOError as e:
            tkinter.messagebox.showerror(title='Error',
                                         message=f'An error occurred while importing flashcards file: {e}')


clue = Flashcards()


def submit_action():
    user_option = optioncombo.get()
    if user_option == "Add Flashcard":
        clue.adding_flashcards()
    elif user_option == "Remove flashcards":
        term = simpledialog.askstring(title='Input', prompt="Enter the term you want to delete")
        if term:
            clue.remove_flashcards(term.lower())
    elif user_option == "Import Flashcards from a text file":
        file_name = simpledialog.askstring(title="Input", prompt="Enter the name of the file you want to import")
        if file_name:
            clue.import_flashcards(file_name.lower())
    elif user_option == "Play with flashcards":
        number_of_guesses = simpledialog.askstring(title='Input', prompt="How many times to ask?")
        if number_of_guesses:
            clue.ask_question(int(number_of_guesses))
    elif user_option == "Export Flashcards to a file":
        export_file_name = simpledialog.askstring(title="Input",
                                                  prompt="Enter the name of the file you want to export to:")
        if export_file_name:
            clue.export_flashcards(export_file_name.lower())
    elif user_option == "Exit":
        window.destroy()
    else:
        tkinter.messagebox.showinfo(title = "Message", message = "Select option from the dropdown")


frame = tkinter.Frame(canvas, borderwidth=2, relief="solid", bg='coral2')
frame.place(relx=0.5, rely=0.5, anchor="center")

userinfoframe = tkinter.LabelFrame(frame, text='User Information', bg='coral2', width=10, height=4)
userinfoframe.grid(row=0, column=0)

fnamelabel = tkinter.Label(userinfoframe, text="Name", bg='coral2')
fnamelabel.grid(row=0, column=0)

fnameentry = tkinter.Entry(userinfoframe)
fnameentry.grid(row=0, column=1)

agelabel = tkinter.Label(userinfoframe, text="Age", bg='coral2', width=10, height=4)
agelabel.grid(row=0, column=2)

agespinbox = tkinter.Spinbox(userinfoframe, from_=14, to=100)
agespinbox.grid(row=0, column=3)

playgameframe = tkinter.LabelFrame(frame, text='Play Game', bg='coral2', width=10, height=4)
playgameframe.grid(row=1, column=0)

optionlabel = tkinter.Label(playgameframe, text='Options', bg='coral2', width=10, height=4)
optionlabel.grid(row=0, column=0)

optioncombo = ttk.Combobox(playgameframe,
                           values=["Add Flashcard", "Remove flashcards", "Import Flashcards from a text file",
                                   "Play with flashcards", "Export Flashcards to a file", "Exit"])
optioncombo.grid(row=0, column=1)
#
submitbtn = tkinter.Button(frame, text="SUBMIT", command=submit_action)
submitbtn.grid(row=2, column=0)

window.mainloop()
