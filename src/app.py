import tkinter as tk


class App(tk.Tk):

    MONEY_LIST = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

    def __init__(self):

        super().__init__()

        self.title("Caisse")
        
        self.money_widget_list = []
        self.total_cash = tk.StringVar(value="0")
        self.revenue = tk.StringVar(value="0")

        self.excepted_revenue = tk.StringVar(value="0")
        self.excepted_revenue_vcmd = (self.register(self.validate_excepted_revenue_entry), "%P")
        
        #Header
        header_frame = tk.Frame(self)
        header_frame.pack(expand=True, fill="x")

        tk.Label(header_frame, text="Montant", width="10").pack(side="left", expand=True)
        tk.Label(header_frame, text="Quantité", width="10").pack(side="left", expand=True)
        tk.Label(header_frame, text="Total", width="10").pack(side="left", expand=True)
        
        #MoneyWidgetList
        for money in self.MONEY_LIST:
            widget = MoneyWidget(self, money, self.update_total)
            widget.pack(expand=True, fill="x", pady=5)
            self.money_widget_list.append(widget)

        #Footer
        total_frame = tk.Frame(self)
        total_frame.pack(fill="x", pady=5, padx=10)

        tk.Label(total_frame, text="Total en caisse").pack(side="left")
        tk.Label(total_frame, textvariable=self.total_cash).pack(side="right")

        base_cash_frame = tk.Frame(self)
        base_cash_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(base_cash_frame, text="Fond de caisse").pack(side="left")
        tk.Label(base_cash_frame, text=150).pack(side="right")

        revenue_frame = tk.Frame(self)
        revenue_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(revenue_frame, text="Recette réélle").pack(side="left")
        tk.Label(revenue_frame, textvariable=self.revenue).pack(side="right")

        excepted_revenue_frame = tk.Frame(self)
        excepted_revenue_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(excepted_revenue_frame, text="Recette sur feuille de caisse").pack(side="left")
        tk.Entry(
            excepted_revenue_frame,
            textvariable=self.excepted_revenue,
            justify="right",
            width=6,
            validate="key",
            validatecommand=self.excepted_revenue_vcmd
        ).pack(side="right")

        tk.Button(self, text="Valider", command=self.on_submit).pack(ipadx=10, pady=5)

        self.update_idletasks()
        self.minsize(300, self.winfo_reqheight())
        
    def update_total(self):
        total_cash = sum([float(money.total_cash.get() or 0) for money in self.money_widget_list])
        self.total_cash.set(f"{total_cash:.2f}")
        self.revenue.set(f"{total_cash - 150:.2f}")

    def on_submit(self):
        difference = float(self.revenue.get() or 0) - float(self.excepted_revenue.get() or 0)

        message = ""
        color = ""

        if difference == 0:
            message = "Votre caisse est juste !"
            color = "green"
        else:
            if difference > 0:
                message = f"Vous avez {difference}€ en trop."
            else:
                message = f"Il vous manque {abs(difference)}€."
            color = "red"
            message += "\nMerci de prévenir un responsable."
                
        window = tk.Toplevel(self)
        window.title("Résultat")
        
        tk.Label(window, text=message, fg=color).pack(pady=10)

        tk.Label(window, text="Espèce à mettre dans la pochette recette :").pack()

        money_header_frame = tk.Frame(window)
        money_header_frame.pack(fill="x", pady=10, padx=20)
        tk.Label(money_header_frame, text="Montant", justify="center").pack(side="left", expand=True, fill="x")
        tk.Label(money_header_frame, text="Quantité", justify="center").pack(side="left", expand=True, fill="x")

        computed_daily_revenue = self.compute_daily_revenue()
        
        for money in computed_daily_revenue:
            money_frame = tk.Frame(window)
            money_frame.pack(fill="x", pady=5, padx=20)
            tk.Label(money_frame, text=f"{money[0]}", justify="center", width=5).pack(side="left", expand=True, fill="x")
            tk.Label(money_frame, text=f"{money[1]}", justify="center", width=5).pack(side="left", expand=True, fill="x")

        tk.Label(window, text="").pack()
        
        # Set the minimum size of the window to its current size to prevent resizing smaller than the content
        window.update_idletasks()
        window.minsize(300, window.winfo_reqheight())
        
    def validate_excepted_revenue_entry(self, P):
        if P == "":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def compute_daily_revenue(self):

        revenue = []

        total_cash = float(self.total_cash.get() or 0)
        amount_to_remove = total_cash - 150

        for money in sorted(self.money_widget_list, key=lambda x: x.value, reverse=True):

            if amount_to_remove <= 0:
                break

            max_possible = min(int(money.quantity.get() or 0), int(amount_to_remove // money.value))

            if max_possible > 0:
                revenue.append((money.value, max_possible))
                amount_to_remove -= max_possible * money.value

        return revenue
            
class MoneyWidget(tk.Frame):

    def __init__(self, master, money, update_main_total):
        super().__init__(master)
        
        self.value = money
        self.quantity = tk.StringVar(value="0")
        self.total_cash = tk.StringVar(value="0.00")
        self.quantity_entry_vcmd = (self.register(self.validate_quantity_entry), "%P")
        
        self.update_main_total = update_main_total

        self.quantity.trace_add("write", self.on_change)

        #Amount label
        tk.Label(self, text=self.value, width=5
            ).pack(side="left", expand=True, fill="x")

        #Decrement buttons
        tk.Button(self, text="-5", command=lambda: self.decrement(5)
            ).pack(side="left", padx=2)
        tk.Button(self, text="-1", command=lambda: self.decrement()
            ).pack(side="left", padx=2)

        #Quantity entry
        self.quantity_entry = tk.Entry(
            self,
            textvariable=self.quantity,
            validate="key",
            validatecommand=self.quantity_entry_vcmd,
            width=5,
            justify="center"
        )
        self.quantity_entry.pack(side="left", padx=10)
        self.quantity_entry.bind("<FocusOut>", self.on_focus_out)

        #Increment buttons
        tk.Button(self, text="+1", command=lambda: self.increment()
            ).pack(side="left", padx=2)
        tk.Button(self, text="+5", command=lambda: self.increment(5)
            ).pack(side="left", padx=2)

        #Total label
        self.total_label = tk.Label(self, textvariable=self.total_cash, width=5)
        self.total_label.pack(side="left", expand=True, fill="x")

    def validate_quantity_entry(self, P):
        return (P.isdigit() or P == "") and int(P or 0) < 1000

    def on_change(self, *args):
        self.update_total()

    def on_focus_out(self, event):
        if self.quantity.get() == "":
            self.quantity.set("0")
        
    def increment(self, value=1):
        quantity = int(self.quantity.get() or 0)
        if quantity + value >= 1000:
            return
        self.quantity.set(quantity + value)
        self.update_total()
        self.update_main_total()
        
    def decrement(self, value=1):
        quantity = int(self.quantity.get() or 0)
        if quantity - value < 0:
            return
        self.quantity.set(quantity - value)
        self.update_total()
        self.update_main_total()

    def update_total(self):
        total_cash = self.value * float(self.quantity.get() or 0)
        self.total_cash.set(f"{total_cash:.2f}")

def main():
    root = App()
    root.mainloop()

if __name__ == "__main__":
    main()

