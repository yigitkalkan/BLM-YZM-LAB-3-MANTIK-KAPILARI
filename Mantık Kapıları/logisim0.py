
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

class Calistir:
    def __init__(self):
        print("Çalıştır button clicked")

class Durdur:
    def __init__(self):
        print("Durdur button clicked")

class Reset:
    def __init__(self):
        print("Reset button clicked")

class CizgiCizme:
    def __init__(self):
        print("Çizgi çizme (kablo çekme)")

class BaglantiDugumu:
    def __init__(self):
        print("Bağlantı düğümü created")

class GirisKutusu:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect = None
        self.text = None
        self.create_giris_kutusu()

    def create_giris_kutusu(self):
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def start_drag(self, event):
        self.rect = self.canvas.create_rectangle(event.x, event.y, event.x + 50, event.y + 50, fill="white")
        self.text = self.canvas.create_text(event.x + 25, event.y + 25, text="0", fill="black")
        self.canvas.tag_bind(self.rect, "<Button-1>", self.toggle_value)
        self.canvas.tag_bind(self.text, "<Button-1>", self.toggle_value)

    def drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, event.x, event.y, event.x + 50, event.y + 50)
            self.canvas.coords(self.text, event.x + 25, event.y + 25)

    def drop(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def toggle_value(self, event):
        current_value = self.canvas.itemcget(self.text, "text")
        new_value = "1" if current_value == "0" else "0"
        self.canvas.itemconfig(self.text, text=new_value)

class CikisKutusu:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect = None
        self.text = None
        self.create_cikis_kutusu()

    def create_cikis_kutusu(self):
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def start_drag(self, event):
        self.rect = self.canvas.create_rectangle(event.x, event.y, event.x + 50, event.y + 50, fill="white")
        self.text = self.canvas.create_text(event.x + 25, event.y + 25, text="0", fill="black")
        self.canvas.tag_bind(self.rect, "<Button-1>", self.show_input_options)
        self.canvas.tag_bind(self.text, "<Button-1>", self.show_input_options)

    def drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, event.x, event.y, event.x + 50, event.y + 50)
            self.canvas.coords(self.text, event.x + 25, event.y + 25)

    def drop(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def show_input_options(self, event):
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="0", command=lambda: self.set_input_value("0"))
        menu.add_command(label="1", command=lambda: self.set_input_value("1"))
        for gate_name in Gate.gate_instances:
            menu.add_command(label=gate_name, command=lambda gate_name=gate_name: self.set_input_value(gate_name))
        menu.post(event.x_root, event.y_root)

    def set_input_value(self, value):
        self.canvas.itemconfig(self.text, text=value)

class Led:
    def __init__(self, canvas):
        self.canvas = canvas
        self.led = None
        self.text = None
        self.create_led()

    def create_led(self):
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)

    def start_drag(self, event):
        self.led = self.canvas.create_oval(event.x, event.y, event.x + 50, event.y + 50, fill="gray")
        self.text = self.canvas.create_text(event.x + 25, event.y + 25, text="0", fill="black")
        self.canvas.tag_bind(self.led, "<Button-1>", self.show_input_options)
        self.canvas.tag_bind(self.text, "<Button-1>", self.show_input_options)

    def drag(self, event):
        if self.led:
            self.canvas.coords(self.led, event.x, event.y, event.x + 50, event.y + 50)
            self.canvas.coords(self.text, event.x + 25, event.y + 25)

    def drop(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def show_input_options(self, event):
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="0", command=lambda: self.set_input_value("0"))
        menu.add_command(label="1", command=lambda: self.set_input_value("1"))
        for gate_name in Gate.gate_instances:
            menu.add_command(label=gate_name, command=lambda gate_name=gate_name: self.set_input_value(gate_name))
        menu.post(event.x_root, event.y_root)

    def set_input_value(self, value):
        self.canvas.itemconfig(self.text, text=value)
        if value == "0":
            self.canvas.itemconfig(self.led, fill="gray")
        elif value == "1":
            self.canvas.itemconfig(self.led, fill="red")
        elif value in Gate.gate_instances:
            gate_output = Gate.gate_instances[value].output_value
            self.canvas.itemconfig(self.led, fill="red" if gate_output == 1 else "gray")
            self.canvas.itemconfig(self.text, text=value)

root = tk.Tk()
root.title("Logisim: main")                         
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)

class Gate:
    id_counter = 1
    gate_instances = {}

    def __init__(self, canvas, image_path, gate_type):
        self.canvas = canvas
        self.image_path = image_path
        self.gate_type = gate_type
        self.gate_name = f"{self.gate_type}{Gate.id_counter}"
        Gate.id_counter += 1
        Gate.gate_instances[self.gate_name] = self
        self.output_value = 0
        self.input_values = [0, 0]
        self.load_image()

    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((150, 150), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.image_id = None
            self.input_text_ids = []
            self.output_text_id = None
            self.label_id = None
            self._dragging = False
        except FileNotFoundError:
            messagebox.showerror("Image not found", f"Image file '{self.image_path}' not found.")

    def start_drag(self, event):
        self._dragging = True
        self.image_id = self.canvas.create_image(event.x, event.y, image=self.tk_image, anchor=tk.CENTER)
        self.create_io_boxes(event.x, event.y)
        self.create_label(event.x, event.y)
        self.canvas.tag_bind(self.image_id, "<Button-3>", self.show_context_menu)

    def drag(self, event):
        if self._dragging and self.image_id:
            self.canvas.coords(self.image_id, event.x, event.y)
            self.update_io_boxes(event.x, event.y)
            self.update_label(event.x, event.y)

    def drop(self, event):
        self._dragging = False
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def show_context_menu(self, event):
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Boyutlandır", command=lambda: self.resize(event))
        context_menu.add_command(label="İsim Değiştir", command=lambda: self.rename_gate(event))
        context_menu.post(event.x_root, event.y_root)

    def resize(self, event):
        new_size = simpledialog.askinteger("Boyutlandır", "Yeni boyutu girin (piksel cinsinden):")
        if new_size:
            self.image = self.image.resize((new_size, new_size), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)

    def rename_gate(self, event):
        new_name = simpledialog.askstring("İsim Değiştir", "Yeni ismi girin:")
        if new_name:
            del Gate.gate_instances[self.gate_name]
            self.gate_name = new_name
            Gate.gate_instances[self.gate_name] = self
            self.canvas.itemconfig(self.label_id, text=self.gate_name)
            self.update_output_value()

    def create_io_boxes(self, x, y):
        self.input_text_ids = [
            self.canvas.create_text(x - 30, y - 25, text="0", fill="black"),
            self.canvas.create_text(x - 30, y + 25, text="0", fill="black")
        ]
        self.output_text_id = self.canvas.create_text(x + 30, y, text="0", fill="black")
        for text_id in self.input_text_ids:
            self.canvas.tag_bind(text_id, "<Button-1>", lambda event, text_id=text_id: self.show_input_options(event, text_id))

    def update_io_boxes(self, x, y):
        self.canvas.coords(self.input_text_ids[0], x - 30, y - 25)
        self.canvas.coords(self.input_text_ids[1], x - 30, y + 25)
        self.canvas.coords(self.output_text_id, x + 30, y)

    def show_input_options(self, event, text_id):
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="0", command=lambda: self.set_input_value(text_id, "0"))
        menu.add_command(label="1", command=lambda: self.set_input_value(text_id, "1"))
        for gate_name in Gate.gate_instances:
            menu.add_command(label=gate_name, command=lambda gate_name=gate_name: self.set_input_value(text_id, gate_name))
        menu.post(event.x_root, event.y_root)

    def set_input_value(self, text_id, value):
        self.canvas.itemconfig(text_id, text=value)
        self.update_output_value()

    def update_output_value(self):
        input_values = []
        for text_id in self.input_text_ids:
            input_text = self.canvas.itemcget(text_id, "text")
            if input_text in Gate.gate_instances:
                input_values.append(Gate.gate_instances[input_text].output_value)
            else:
                input_values.append(int(input_text))
        output_value = self.calculate_output(input_values)
        self.output_value = output_value
        self.canvas.itemconfig(self.output_text_id, text=str(output_value))
        self.update_linked_gates()

    def update_linked_gates(self):
        for gate in Gate.gate_instances.values():
            for i, input_text_id in enumerate(gate.input_text_ids):
                input_text = self.canvas.itemcget(input_text_id, "text")
                if input_text == self.gate_name:
                    gate.input_values[i] = self.output_value
                    gate.update_output_value()

    def create_label(self, x, y):
        self.label_id = self.canvas.create_text(x, y - 80, text=self.gate_name, fill="black", font=("Helvetica", 10, "bold"))

    def update_label(self, x, y):
        self.canvas.coords(self.label_id, x, y - 80)

    def calculate_output(self, input_values):
        return 0  # Default implementation, should be overridden by specific gate classes

# Specific gate classes inheriting from Gate
class NotGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "notegate.png", "NOT")

    def calculate_output(self, input_values):
        return 1 if input_values[0] == 0 else 0

class AndGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "andgate.png", "AND")

    def calculate_output(self, input_values):
        return 1 if input_values[0] == 1 and input_values[1] == 1 else 0

class OrGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "orgate.png", "OR")

    def calculate_output(self, input_values):
        return 1 if input_values[0] == 1 or input_values[1] == 1 else 0

class NandGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "nandgate.png", "NAND")

    def calculate_output(self, input_values):
        return 0 if input_values[0] == 1 and input_values[1] == 1 else 1

class NorGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "norgate.png", "NOR")

    def calculate_output(self, input_values):
        return 0 if input_values[0] == 1 or input_values[1] == 1 else 1

class XorGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "xorgate.png", "XOR")

    def calculate_output(self, input_values):
        return 1 if input_values[0] != input_values[1] else 0

class XnorGate(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "xnorgate.png", "XNOR")

    def calculate_output(self, input_values):
        return 1 if input_values[0] == input_values[1] else 0

class Buffer(Gate):
    def __init__(self, canvas):
        super().__init__(canvas, "buffergate.png", "BUF")

    def calculate_output(self, input_values):
        return input_values[0]

def create_gate_instance(cls):
    def wrapper():
        gate_instance = cls(canvas)
        canvas.bind("<ButtonPress-1>", gate_instance.start_drag)
        canvas.bind("<B1-Motion>", gate_instance.drag)
        canvas.bind("<ButtonRelease-1>", gate_instance.drop)
    return wrapper

def create_instance(cls):
    def wrapper():
        if isinstance(cls, type) and issubclass(cls, Gate):
            create_gate_instance(cls)()
        else:
            instance = cls(canvas)
    return wrapper

def enable_move_mode():
    canvas.bind("<ButtonPress-1>", start_move)
    canvas.bind("<B1-Motion>", move)
    canvas.bind("<ButtonRelease-1>", drop_move)

def disable_move_mode():
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def start_move(event):
    global selected_item
    selected_item = canvas.find_closest(event.x, event.y)[0]
    if canvas.type(selected_item) not in ["image", "text"]:
        selected_item = None

def move(event):
    if selected_item:
        canvas.coords(selected_item, event.x, event.y)

def drop_move(event):
    global selected_item
    selected_item = None

groups = {
    "Kontrol Tuşları": [("Çalıştır", Calistir), ("Durdur", Durdur), ("Reset", Reset)],
    "Mantık Kapıları": [("Not Gate", NotGate), ("Buffer", Buffer), ("And Gate", AndGate), ("Or Gate", OrGate),
                        ("Nand Gate", NandGate), ("Nor Gate", NorGate), ("Xor Gate", XorGate), ("Xnor Gate", XnorGate)],
    "Bağlantı Elemanları": [("Çizgi çizme (kablo çekme)", CizgiCizme), ("Bağlantı düğümü", BaglantiDugumu)],
    "Giriş Çıkış Elemanları": [("Giriş Kutusu", GirisKutusu), ("Çıkış Kutusu", CikisKutusu), ("Led", Led)],
    "Diğer": [("Taşı", enable_move_mode), ("Taşımayı Durdur", disable_move_mode)]
}

for group, buttons in groups.items():
    label = tk.Label(toolbar, text=group, anchor="w")
    label.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
    for button_text, cls in buttons:
        btn = tk.Button(toolbar, text=button_text, command=create_instance(cls) if callable(cls) else cls)
        btn.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

toolbar.pack(side=tk.LEFT, fill=tk.Y)

canvas = tk.Canvas(root, bg="white")
canvas.pack(expand=True, fill=tk.BOTH)

def draw_grid():
    canvas.delete('grid_line')
    for i in range(0, canvas.winfo_width(), 20):
        canvas.create_line([(i, 0), (i, canvas.winfo_height())], tag='grid_line', fill="gray")
    for i in range(0, canvas.winfo_height(), 20):
        canvas.create_line([(0, i), (canvas.winfo_width(), i)], tag='grid_line', fill="gray")

canvas.bind('<Configure>', lambda event: draw_grid())

selected_item = None

root.mainloop()
