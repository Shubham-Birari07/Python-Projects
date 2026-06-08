import tkinter
from tkinter import *
from tkinter import ttk, filedialog, colorchooser, font
from googletrans import Translator, LANGUAGES
from tkinter import PhotoImage
import pyttsx3
import speech_recognition as sr

# Global Variables for History and Fonts
translation_history = []
current_font = ("Arial", 16, "bold")

def change(text="type", src="English", dest="Hindi"):
    trans = Translator()
    trans1 = trans.translate(text, src=src, dest=dest)
    return trans1.text

def data():
    s = comb_sor.get()
    d = comb_dest.get()
    masg = Sor_txt.get(1.0, END)
    textget = change(text=masg, src=s, dest=d)
    dest_txt.delete(1.0, END)
    dest_txt.insert(END, textget)
    translation_history.append((masg.strip(), textget.strip()))

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            Sor_txt.delete(1.0, END)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            Sor_txt.insert(END, text)
        except sr.UnknownValueError:
            Sor_txt.insert(END, "Sorry, I could not understand the audio.")
        except sr.RequestError:
            Sor_txt.insert(END, "Could not request results; check your network connection.")

def clear_all():
    Sor_txt.delete(1.0, END)
    dest_txt.delete(1.0, END)

def save_translation():
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text file", ".txt"), ("All files", ".*")])
    if file:
        file.write(f"Source: {Sor_txt.get(1.0, END)}\nTranslation: {dest_txt.get(1.0, END)}")
        file.close()

def load_translation():
    file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("Text file", ".txt"), ("All files", ".*")])
    if file:
        lines = file.readlines()
        Sor_txt.delete(1.0, END)
        dest_txt.delete(1.0, END)
        Sor_txt.insert(END, lines[0].replace("Source: ", ""))
        dest_txt.insert(END, lines[1].replace("Translation: ", ""))
        file.close()

def change_font():
    global current_font
    new_font = font.Font(family=current_font[0], size=current_font[1], weight=current_font[2])
    Sor_txt.configure(font=new_font)
    dest_txt.configure(font=new_font)
    current_font = new_font

def change_theme():
    color = colorchooser.askcolor()[1]
    if color:
        Sor_txt.config(bg=color)
        dest_txt.config(bg=color)

def bold_text():
    Sor_txt.tag_add("bold", SEL_FIRST, SEL_LAST)
    Sor_txt.tag_config("bold", font=(current_font[0], current_font[1], "bold"))

def italic_text():
    Sor_txt.tag_add("italic", SEL_FIRST, SEL_LAST)
    Sor_txt.tag_config("italic", font=(current_font[0], current_font[1], "italic"))

def underline_text():
    Sor_txt.tag_add("underline", SEL_FIRST, SEL_LAST)
    Sor_txt.tag_config("underline", font=(current_font[0], current_font[1], "underline"))

def view_history():
    history_window = Toplevel(root)
    history_window.title("Translation History")
    history_window.geometry("400x400")
    history_text = Text(history_window, wrap=WORD)
    history_text.pack(expand=True, fill=BOTH)
    for src, trans in translation_history:
        history_text.insert(END, f"Source: {src}\nTranslation: {trans}\n\n")

def auto_translate(event):
    data()

def highlight_button(widget):
    widget.config(bg="darkorange", fg="white", activebackground="orange", activeforeground="white")

root = Tk()
root.title("Translator")
root.geometry("600x800")

image_path = PhotoImage(file=r"C:\Users\Shubham Anil Birari\OneDrive\Pictures\Screenshots\Screenshot (4).png")
bg_image = tkinter.Label(root, image=image_path)
bg_image.place(relheight=1, relwidth=1)

# Background and Title
lab_txt = Label(root, text="Translator", font=("Arial", 30, "bold"), bg="cyan")
lab_txt.place(x=150, y=20, height=50, width=300)

frame = Frame(root)
frame.pack(side=BOTTOM, padx=10, pady=10)

# Source Text
lab_txt = Label(root, text="Source Text", font=("Arial", 16, "bold"), bg="lightblue")
lab_txt.place(x=50, y=100, height=30, width=200)

Sor_txt = Text(root, font=current_font, wrap=WORD, bg="white", fg="black", padx=5, pady=5, bd=2, relief=GROOVE)
Sor_txt.place(x=50, y=140, height=150, width=500)
Sor_txt.bind("<KeyRelease>", auto_translate)

# Language Selectors
list_text = list(LANGUAGES.values())
comb_sor = ttk.Combobox(root, values=list_text)
comb_sor.place(x=50, y=300, height=40, width=150)
comb_sor.set("English")

comb_dest = ttk.Combobox(root, values=list_text)
comb_dest.place(x=400, y=300, height=40, width=150)
comb_dest.set("Hindi")

# Destination Text
lab_txt = Label(root, text="Destination Text", font=("Arial", 16, "bold"), bg="lightblue")
lab_txt.place(x=50, y=350, height=30, width=200)

dest_txt = Text(root, font=current_font, wrap=WORD, bg="white", fg="black", padx=5, pady=5, bd=2, relief=GROOVE)
dest_txt.place(x=50, y=390, height=150, width=500)

# Buttons with Highlight Effect
button_change = Button(root, text="Translate", command=data, font=("Arial", 14))
button_change.place(x=240, y=300, height=40, width=150)
highlight_button(button_change)

button_recognize_speech = Button(root, text="Speak to Text", command=recognize_speech, font=("Arial", 14))
button_recognize_speech.place(x=50, y=560, height=40, width=150)
highlight_button(button_recognize_speech)

button_speak_original = Button(root, text="Speak Original", command=lambda: speak_text(Sor_txt.get(1.0, END)), font=("Arial", 14))
button_speak_original.place(x=50, y=620, height=40, width=150)
highlight_button(button_speak_original)

button_speak_translated = Button(root, text="Speak Translated", command=lambda: speak_text(dest_txt.get(1.0, END)), font=("Arial", 14))
button_speak_translated.place(x=400, y=620, height=40, width=150)
highlight_button(button_speak_translated)

button_clear_all = Button(root, text="Clear All", command=clear_all, font=("Arial", 14))
button_clear_all.place(x=400, y=560, height=40, width=150)
highlight_button(button_clear_all)

button_save = Button(root, text="Save Translation", command=save_translation, font=("Arial", 14))
button_save.place(x=50, y=680, height=40, width=150)
highlight_button(button_save)

button_load = Button(root, text="Load Translation", command=load_translation, font=("Arial", 14))
button_load.place(x=400, y=680, height=40, width=150)
highlight_button(button_load)

button_history = Button(root, text="View History", command=view_history, font=("Arial", 14))
button_history.place(x=240, y=740, height=40, width=150)
highlight_button(button_history)

root.mainloop()
