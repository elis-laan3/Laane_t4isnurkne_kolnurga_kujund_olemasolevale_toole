from tkinter import Frame, Text, messagebox
from tkinter.ttk import Combobox, Button, Label, Entry

from Circle import Circle
from Rectangle import Rectangle


class TaskGui:
    def __init__(self, main):
        self.main = main
        main.title("Task GUI") # Võib ka ilma self. antud versioonis
        self.main.geometry("500x280")

        # Frame
        self.frame = Frame(self.main, background="#e6a902")
        self.frame.pack(fill="both", expand=True)

        # Create Combobox
        self.cmb = Combobox(self.frame, values=("Vali kujund", "Ring", "Ristkülik"))
        self.cmb.current(0) # Vali kujund
        self.cmb['state'] = "readonly" # Comboboxi sisu ei saa muuta
        self.cmb.grid(row=0, column=0, padx=3, pady=3, columnspan=2, sticky="ew")

        # Ujuvad vidinad (ring, ristkülik)
        self.lbl_circle, self.txt_circle = self.create_circle_widget()
        self.lbl_a, self.lbl_b, self.txt_a, self.txt_b = self.create_rectangle_widget()

        # Create button
        self.btn_submit = self.create_button()

        # Create result Text
        self.result = self.create_result()

        # Peidame ringi ja Ristküliku "asjad"
        self.forget_circle() # Unusta/Peida ring
        self.forget_rectangle() # Unusta/Peida ristkülik

        # "Kuula" comboboxi muutusi
        self.cmb.bind("<<ComboboxSelected>>", self.changed)


    def create_button(self):
        button = Button(self.frame, text="Näita", command=lambda: self.calculate())
        button['state'] = "disabled"
        button.grid(row=3, column=0, padx=3, pady=3, columnspan=2, sticky="ew")
        return button

    def create_result(self):
        result = Text(self.frame, height=5, width=25)
        result.grid(row=4, column=0, padx=3, pady=3, columnspan=2, sticky="ew")
        result["state"] = "disabled" # Kasti kirjutada ei saa
        return result

    def create_circle_widget(self):
        label = Label(self.frame, text="Raadius")
        label.grid(row=1, column=0, padx=3, pady=3, sticky="ew")

        text = Entry(self.frame, width=12)
        text.focus()
        text.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

        return label, text

    def create_rectangle_widget(self):
        label_a = Label(self.frame, text="Külg a")
        label_a.grid(row=1, column=0, padx=3, pady=3, sticky="ew")

        text_a = Entry(self.frame, width=12)
        text_a.focus()
        text_a.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

        label_b = Label(self.frame, text="Külg b")
        label_b.grid(row=2, column=0, padx=3, pady=3, sticky="ew")

        text_b = Entry(self.frame, width=12)
        text_b.grid(row=2, column=1, padx=3, pady=3, sticky="ew")


        return label_a, label_b, text_a, text_b

    def forget_circle(self):
        self.lbl_circle.grid_forget()
        self.txt_circle.grid_forget()
        self.btn_submit['state'] = "disabled" # Nuppu ei saa klikkida

    def forget_rectangle(self):
        self.lbl_a.grid_forget()
        self.lbl_b.grid_forget()
        self.txt_a.grid_forget()
        self.txt_b.grid_forget()
        self.btn_submit['state'] = "disabled"

    def changed(self, event=None):
        combo_index = self.cmb.current() # Mitmes valik comboboxist (0, 1, 2)
        if combo_index == 0:
            self.forget_circle()
            self.forget_rectangle()
            self.btn_submit['state'] = "disabled"
        elif combo_index == 1: #ring
            self.lbl_circle, self.txt_circle = self.create_circle_widget()
            self.forget_rectangle()
            self.btn_submit['state'] = "normal"
        elif combo_index == 2: #ristkülik
            self.lbl_a, self.lbl_b, self.txt_a, self.txt_b = self.create_rectangle_widget()
            self.forget_circle()
            self.btn_submit['state'] = "normal"

        self.clear_result() # Tulemuskasti sisu kustutamine

    def clear_result(self):
        self.result.config(state="normal") # Tulemuskasti sisu saab muuta
        self.result.delete("1.0", "end") # Tühenda tulemuskast
        self.result.config(state="disabled") # Tulemuskasti sisu EI SAA muuta

    def calculate(self):
        cmb_index = self.cmb.current()
        if cmb_index == 1: # Ring
            try:
                radius = float(self.txt_circle.get().strip())
                circle = Circle(radius) # Loo objekt ring
                self.clear_result() # Tühejenda vastuse kast
                self.result.config(state="normal") # Vastuse lisamiseks
                self.result.insert("1.0", str(circle)) # Täis vastus klassist Circle (
                self.result.config(state="disabled") # Et vastust ei saaks näppida
            except ValueError:
                messagebox.showerror("Viga", "Raadius peab olema number.")

            self.txt_circle.delete(0, "end") # Tühjenda raadiuse kast
            self.txt_circle.focus()
        elif cmb_index == 2: # Ristkülik
            try:
                width = float(self.txt_a.get().strip())
                height = float(self.txt_b.get().strip())
                rectangle = Rectangle(width, height)
                self.clear_result()
                self.result.config(state="normal")
                self.result.insert("1.0", str(rectangle))
                self.result.config(state="disabled")
            except ValueError:
                messagebox.showerror("Viga", "Küljed peavad olema numbrid.")

            self.txt_a.delete(0, "end")
            self.txt_a.focus()

            self.txt_b.delete(0, "end")
            self.txt_b.focus()