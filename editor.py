import tkinter as tk
from tkinter import ttk, colorchooser
from planet import Planet

class Controller:
    def __init__(self, master, simulation):
        self.master = master
        self.simulation = simulation
        self.selected_planet = None
        self.simulation_running = True

        self.master.title("Solar System Controller")
        self.master.geometry("300x400")

        self.create_widgets()
        self.update_planets_list_periodically()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.master)

        self.list_tab = ttk.Frame(self.tab_control)
        self.add_tab = ttk.Frame(self.tab_control)
        self.edit_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.list_tab, text='Planets List')
        self.tab_control.add(self.add_tab, text='Add Planet')
        self.tab_control.add(self.edit_tab, text='Edit Planet')

        self.tab_control.pack(expand=1, fill='both')

        self.create_list_widgets()
        self.create_add_widgets()
        self.create_edit_widgets()

        self.tab_control.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def create_list_widgets(self):
        list_frame = ttk.Frame(self.list_tab)
        list_frame.pack(pady=10, fill='both', expand=True)

        self.planets_listbox = tk.Listbox(list_frame)
        self.planets_listbox.pack(fill='both', expand=True)
        self.planets_listbox.bind('<<ListboxSelect>>', self.on_planet_select)

        self.update_planets_list()

    def create_add_widgets(self):
        add_frame = ttk.Frame(self.add_tab)
        add_frame.pack(pady=10)

        self.name_label = ttk.Label(add_frame, text="Name")
        self.name_label.pack()
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.pack()

        self.mass_label = ttk.Label(add_frame, text="Mass (kg)")
        self.mass_label.pack()
        self.mass_entry = ttk.Entry(add_frame)
        self.mass_entry.pack()

        self.radius_label = ttk.Label(add_frame, text="Radius (pixels)")
        self.radius_label.pack()
        self.radius_entry = ttk.Entry(add_frame)
        self.radius_entry.pack()

        self.velocity_label = ttk.Label(add_frame, text="Velocity (m/s)")
        self.velocity_label.pack()
        self.velocity_entry = ttk.Entry(add_frame)
        self.velocity_entry.pack()

        self.distance_label = ttk.Label(add_frame, text="Distance to Sun (AU)")
        self.distance_label.pack()
        self.distance_entry = ttk.Entry(add_frame)
        self.distance_entry.pack()

        self.color_label = ttk.Label(add_frame, text="Color")
        self.color_label.pack()
        self.color_button = tk.Button(add_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack()
        self.color = (255, 255, 255)

        self.add_planet_button = ttk.Button(add_frame, text="Add Planet", command=self.add_planet)
        self.add_planet_button.pack()

    def create_edit_widgets(self):
        edit_frame = ttk.Frame(self.edit_tab)
        edit_frame.pack(pady=10)

        self.edit_name_label = ttk.Label(edit_frame, text="Name")
        self.edit_name_label.pack()
        self.edit_name_entry = ttk.Entry(edit_frame)
        self.edit_name_entry.pack()

        self.edit_mass_label = ttk.Label(edit_frame, text="Mass (kg)")
        self.edit_mass_label.pack()
        self.edit_mass_entry = ttk.Entry(edit_frame)
        self.edit_mass_entry.pack()

        self.edit_radius_label = ttk.Label(edit_frame, text="Radius (pixels)")
        self.edit_radius_label.pack()
        self.edit_radius_entry = ttk.Entry(edit_frame)
        self.edit_radius_entry.pack()

        self.edit_velocity_label = ttk.Label(edit_frame, text="Velocity (m/s)")
        self.edit_velocity_label.pack()
        self.edit_velocity_entry = ttk.Entry(edit_frame)
        self.edit_velocity_entry.pack()

        self.edit_color_label = ttk.Label(edit_frame, text="Color")
        self.edit_color_label.pack()
        self.edit_color_button = tk.Button(edit_frame, text="Choose Color", command=self.choose_edit_color)
        self.edit_color_button.pack()

        self.remove_planet_button = tk.Button(edit_frame, text="Remove Planet", command=self.remove_planet)
        self.remove_planet_button.pack()

        self.update_planet_button = ttk.Button(edit_frame, text="Update Planet", command=self.update_planet)
        self.update_planet_button.pack()

    def update_planets_list(self):
        self.planets_listbox.delete(0, tk.END)
        for planet in self.simulation.planets:
            planet_info = f"{planet.name}: Mass={planet.mass:.2e}, Radius={planet.radius}, Vel={planet.y_vel:.2f}"
            self.planets_listbox.insert(tk.END, planet_info)

    def update_planets_list_periodically(self):
        self.update_planets_list()
        self.master.after(1000, self.update_planets_list_periodically)

    def on_planet_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_planet = self.simulation.planets[index]
            self.populate_edit_fields(self.selected_planet)
            self.simulation_running = False
            self.tab_control.select(self.edit_tab)

    def on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == 'Edit Planet':
            self.simulation_running = False
        else:
            self.simulation_running = True

    def populate_edit_fields(self, planet):
        self.edit_name_entry.delete(0, tk.END)
        self.edit_name_entry.insert(0, planet.name)
        self.edit_mass_entry.delete(0, tk.END)
        self.edit_mass_entry.insert(0, str(planet.mass))
        self.edit_radius_entry.delete(0, tk.END)
        self.edit_radius_entry.insert(0, str(planet.radius))
        self.edit_velocity_entry.delete(0, tk.END)
        self.edit_velocity_entry.insert(0, str(planet.y_vel))
        self.edit_color_button.configure(bg=self.rgb_to_hex(planet.color))

    def add_planet(self):
        name = self.name_entry.get()
        mass = float(self.mass_entry.get())
        radius = int(self.radius_entry.get())
        velocity = float(self.velocity_entry.get())
        distance = float(self.distance_entry.get())

        x = -distance * Planet.AU
        y = 0

        new_planet = Planet(x, y, radius, self.color, mass, name)
        new_planet.y_vel = velocity
        self.simulation.planets.append(new_planet)

        self.update_planets_list()

    def update_planet(self):
        if self.selected_planet:
            new_name = self.edit_name_entry.get()
            new_mass = float(self.edit_mass_entry.get())
            new_radius = int(self.edit_radius_entry.get())
            new_velocity = float(self.edit_velocity_entry.get())

            self.selected_planet.name = new_name
            self.selected_planet.mass = new_mass
            self.selected_planet.radius = new_radius
            self.selected_planet.y_vel = new_velocity

            self.update_planets_list()
            self.tab_control.select(self.list_tab)
            self.simulation_running = True

    def remove_planet(self):
        if self.selected_planet:
            self.simulation.planets.remove(self.selected_planet)
            self.selected_planet = None
            self.update_planets_list()
            self.tab_control.select(self.list_tab)
            self.simulation_running = True

    def choose_color(self):
        self.color = colorchooser.askcolor()[0]

    def choose_edit_color(self):
        color = colorchooser.askcolor()[0]
        if color:
            self.selected_planet.color = color
            self.edit_color_button.configure(bg=self.rgb_to_hex(color))

    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))