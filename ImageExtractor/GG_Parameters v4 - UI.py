import tkinter as tk
from tkinter import Checkbutton, IntVar, Listbox, END
import json

# Assuming PARAMETERS_PATH is defined (for loading/saving script configs)
PARAMETERS_PATH = 'ImageExtractor\\parameters.json'

def load_parameters():
    try:
        with open(PARAMETERS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_parameters(parameters):
    with open(PARAMETERS_PATH, 'w') as f:
        json.dump(parameters, f, indent=4)

def main():
    parameters = load_parameters()
    script_configs = parameters.get('scripts', {})

    root = tk.Tk()
    root.title("Geospatial Processing Configuration")

    # Coordinate Entry Section
    tk.Label(root, text="Coordinates (lat, lon):").pack(padx=10, pady=5)
    coords_entry = tk.Entry(root)
    coords_entry.pack(padx=10, pady=5)

    def on_submit():
        coords = coords_entry.get()
        if coords:
            try:
                lat, lon = map(float, coords.split(','))
                parameters["center_lat"] = lat
                parameters["center_lon"] = lon
                save_parameters(parameters)
                print("Parameters updated and saved.")
                root.destroy()  # Close the tkinter window
            except ValueError:
                print("Invalid coordinates format.")
        else:
            print("Please enter both coordinates and a location name.")

    submit_btn = tk.Button(root, text="Submit", command=on_submit)
    submit_btn.pack(padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
