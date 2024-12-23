import tkinter as tk
from tkinter import messagebox
import requests

def get_exchange_rates(base_currency='USD'):
    url = f'https://api.frankfurter.dev/v1/latest?base={base_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"API error: {e}")
        return None

def fetch_exchange_rate(from_currency, to_currency):
    data = get_exchange_rates(from_currency)
    if data:
        if "rates" in data and to_currency in data["rates"]:
            return data["rates"][to_currency]
        else:
            messagebox.showerror("Error", "Could not fetch exchange rate.")
            return None
    return None

def convert_currency():
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount!")
        return
    
    rate = fetch_exchange_rate(from_currency, to_currency)
    
    if rate:
        converted_amount = amount * rate
        result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    else:
        result_label.config(text="Unable to fetch exchange rate.")

root = tk.Tk()
root.title("Currency Converter")
root.geometry("300x320")

currency_list = ["EUR", "USD", "TRY"]  # Currencies available for selection

# Source currency dropdown menu
from_currency_var = tk.StringVar(value=currency_list[1])  # Default is USD
tk.Label(root, text="Source Currency:").pack(pady=5)
from_currency_menu = tk.OptionMenu(root, from_currency_var, *currency_list)
from_currency_menu.pack(pady=5)

# Target currency dropdown menu
to_currency_var = tk.StringVar(value=currency_list[2])  # Default is TRY
tk.Label(root, text="Target Currency:").pack(pady=5)
to_currency_menu = tk.OptionMenu(root, to_currency_var, *currency_list)
to_currency_menu.pack(pady=5)

# Entry for amount
tk.Label(root, text="Amount:").pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.pack(pady=15)

result_label = tk.Label(root, text="", font=("Open Sans", 12))
result_label.pack(pady=10)

root.mainloop()
