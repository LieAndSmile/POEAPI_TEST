import tkinter as tk
import requests

def fetch_currency_data(league='Ancestor'):
    try:
        url = 'https://poe.ninja/api/data/currencyoverview'
        params = {
            'league': league,
            'type': 'Currency'
        }
        print("Fetching data for league:", league)
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        print("Data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_currency_data(data):
    desired_currencies = ['Chaos Orb', 'Divine Orb', 'Exalted Orb']
    currency_info = {}

    for item in data['lines']:
        currency_name = item['currencyTypeName']
        if currency_name in desired_currencies:
            chaos_value = item['chaosEquivalent']
            currency_info[currency_name] = chaos_value

    print("Parsed data:", currency_info)
    return currency_info

class CurrencyOverlay(tk.Tk):
    def __init__(self):
        super().__init__()
        print("Initializing CurrencyOverlay...")
        self.title("PoE Currency Overlay")
        self.attributes('-topmost', True)
        self.overrideredirect(True)  # Removes window decorations
        self.configure(bg='black')
        self.attributes('-alpha', 1.0)  # Fully opaque for visibility
        self.geometry('300x150+100+100')  # Set window size and position
        self.currency_labels = {}
        self.create_widgets()
        self.update_data()
        self._offsetx = 0
        self._offsety = 0
        self.bind_events()
        self.bind('<Escape>', self.close_app)  # Allows closing with 'Esc' key
        self.lift()  # Bring window to front
        self.after_idle(self.attributes, '-topmost', True)

    def create_widgets(self):
        currencies = ['Chaos Orb', 'Divine Orb', 'Exalted Orb']
        for currency in currencies:
            label = tk.Label(self, text='', fg='white', bg='black', font=('Arial', 14))
            label.pack(anchor='w', padx=5, pady=2)
            self.currency_labels[currency] = label
        # Optional: Add a close button
        close_button = tk.Button(self, text='Close', command=self.destroy)
        close_button.pack(pady=5)

    def update_data(self):
        data = fetch_currency_data()
        if data:
            currency_info = parse_currency_data(data)
            self.update_labels(currency_info)
        else:
            self.display_error()
        self.after(300000, self.update_data)  # Refresh every 5 minutes

    def update_labels(self, currency_info):
        for currency, label in self.currency_labels.items():
            value = currency_info.get(currency, None)
            if value is not None:
                if currency == 'Chaos Orb':
                    display_text = f'{currency}: 1.00 Chaos Orb'
                else:
                    display_text = f'{currency}: {value:.2f} Chaos Orbs'
            else:
                display_text = f'{currency}: Data Unavailable'
            label.config(text=display_text)

    def display_error(self):
        for label in self.currency_labels.values():
            label.config(text='Error fetching data')

    def bind_events(self):
        self.bind('<ButtonPress-1>', self.start_move)
        self.bind('<B1-Motion>', self.do_move)

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def do_move(self, event):
        x = event.x_root - self._offsetx
        y = event.y_root - self._offsety
        self.geometry(f'+{x}+{y}')

    def close_app(self, event=None):
        self.destroy()

if __name__ == '__main__':
    try:
        app = CurrencyOverlay()
        app.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
