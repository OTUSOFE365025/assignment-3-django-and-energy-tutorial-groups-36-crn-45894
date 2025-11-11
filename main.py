############################################################################
## Django ORM Standalone Python Template
############################################################################
""" Here we'll import the parts of Django we need. It's recommended to leave
these settings as is, and skip to START OF APPLICATION section below """

# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# setup django environment
import django
django.setup()

# Import your models for use in your script
from db.models import *

############################################################################
## START OF APPLICATION
############################################################################

# Simple Tkinter Cash Register GUI Application
import tkinter as tk
import random
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

RUNNING_SUBTOTAL = 0.0

# Clean up the database by deleting all items
Item.objects.all().delete()

def on_button_click_add_item_random():
    global RUNNING_SUBTOTAL
    # Get a random item from the database
    items = list(Item.objects.all())
    if not items:
        messagebox.showwarning("No Items", "No items available in the database.")
        text_area.see(tk.END)
        return

    item = random.choice(items)
    text_area.insert(tk.END, f"{item}\n")
    text_area.see(tk.END)

    RUNNING_SUBTOTAL += item.get_price()
    subtotal_text.set(f"${RUNNING_SUBTOTAL:.2f}")

# Button click event handler
def on_button_click_add_item():
    global RUNNING_SUBTOTAL
    upc = upc_entry.get().strip()
    
    if not upc or upc.isalpha():
        messagebox.showwarning("Input Error", "Please enter a UPC code.")
        text_area.see(tk.END)
        return
    
    try:
        # Try to get the item by UPC code
        item = Item.objects.get(upc_code=upc)
        text_area.insert(tk.END, f"{item}\n")
        text_area.see(tk.END)

        RUNNING_SUBTOTAL += item.get_price()
        subtotal_text.set(f"${RUNNING_SUBTOTAL:.2f}")

        # Clear the input box for the next item
        upc_entry.delete(0, tk.END)

    except Item.DoesNotExist:
        messagebox.showwarning("Item Not Found", f"No item found with UPC '{upc}'.")
        text_area.see(tk.END)
        upc_entry.delete(0, tk.END)

# Function to load items from a file
def load_items_into_database_from_file(filename):
    """
    Reads product data from a file and returns a list of Item objects.

    :param filename: The path to the text file (e.g., 'products_file.txt').
    """
    try:
        # Open the file for reading ('r')
        with open(filename, 'r') as file:
            # Skip the header line
            file.readline()

            # Process the remaining lines in the file
            for line in file:
                # Remove leading/trailing whitespace and split the line by spaces
                parts = line.strip().split()

                if len(parts) == 3:
                    # Unpack the parts
                    upc_code_file = parts[0]
                    name_file = parts[1]
                    # Remove the '$' sign and convert the price to a float
                    price_file = float(parts[2].replace('$', ''))
                    
                    # Create an Item object and add it to the database
                    Item.objects.create(upc_code=upc_code_file, name=name_file, price=price_file)
                else:
                    print(f"Skipping malformed line: {line.strip()}")

    # Handle file not found error and other exceptions
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print('Available products:')
    for i in Item.objects.all():
        print(i.upc_code, i.name, i.price)

############################################################################
## START OF GUI APPLICATION
############################################################################

# Load items from the products file
load_items_into_database_from_file('products_file.txt')

# Create the main window
root = tk.Tk()
root.title("Cash Register App")
root.geometry("500x500")

# Create a frame for input and button
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

# UPC input entry
upc_label = tk.Label(input_frame, text="Enter UPC Code:", font=("Times New Roman", 10))
upc_label.grid(row=0, column=0, padx=(0, 5))

upc_entry = tk.Entry(input_frame, font=("Times New Roman", 10))
upc_entry.grid(row=0, column=1, padx=(0, 10))

# Add scan item button
add_item_button = tk.Button(
    input_frame, text="Scan Item",
    command=lambda: on_button_click_add_item()
)
add_item_button.grid(row=0, column=2)

# Add random item button
add_random_item_button = tk.Button(
    input_frame, text="Add Random Item",
    command=lambda: on_button_click_add_item_random()
)
add_random_item_button.grid(row=0, column=3, padx=(10, 0))

# Create a scrolled text area for displaying items
text_area = ScrolledText(
    root, wrap=tk.WORD, width=54, height=22, font=("Times New Roman", 10))

text_area.pack(padx=10, pady=10)

# Create a button to simulate scanning an item
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

subtotal_label = tk.Label(button_frame, text="Subtotal:", font=("Times New Roman", 10))
subtotal_label.grid(row=0, column=0, padx=(0, 5))

subtotal_text = tk.StringVar(value="$0.00")
subtotal_count = tk.Label(button_frame, textvariable=subtotal_text, font=("Times New Roman", 10))
subtotal_count.grid(row=0, column=1, padx=(0, 20))

# Start the GUI event loop
root.mainloop()