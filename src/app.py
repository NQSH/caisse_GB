import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caisse")
        
        self.moneyList = []
        self.total = tk.StringVar(value="0")
        self.revenue = tk.StringVar(value="0")
        self.exceptedRevenue = tk.StringVar(value="0")

        self.vcmd = (self.register(self.validate), "%P")
        
        #Header
        header = tk.Frame(self)
        header.pack(expand=True, fill="x")
        tk.Label(header, text="Montant", width="10").pack(side="left", expand=True)
        tk.Label(header, text="Quantité", width="10").pack(side="left", expand=True)
        tk.Label(header, text="Total", width="10").pack(side="left", expand=True)
        
        #AmountWidgetList
        for money in [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]:
            widget = MoneyWidget(self, money, self.update_total)
            widget.pack(expand=True, fill="x", pady=5)
            self.moneyList.append(widget)

        #Footer
        totalFrame = tk.Frame(self)
        totalFrame.pack(fill="x", pady=5, padx=10)
        tk.Label(totalFrame, text="Total en caisse").pack(side="left")
        tk.Label(totalFrame, textvariable=self.total).pack(side="right")

        baseCashFrame = tk.Frame(self)
        baseCashFrame.pack(fill="x", pady=5, padx=10)
        tk.Label(baseCashFrame, text="Fond de caisse").pack(side="left")
        tk.Label(baseCashFrame, text=150).pack(side="right")

        revenueFrame = tk.Frame(self)
        revenueFrame.pack(fill="x", pady=5, padx=10)
        tk.Label(revenueFrame, text="Recette réélle").pack(side="left")
        tk.Label(revenueFrame, textvariable=self.revenue).pack(side="right")

        exceptedRevenueFrame = tk.Frame(self)
        exceptedRevenueFrame.pack(fill="x", pady=5, padx=10)
        tk.Label(exceptedRevenueFrame, text="Recette sur feuille de caisse").pack(side="left")
        tk.Entry(
            exceptedRevenueFrame,
            textvariable=self.exceptedRevenue,
            justify="right",
            width=6,
            validate="key",
            validatecommand=self.vcmd
        ).pack(side="right")

        tk.Button(self, text="Valider", command=self.on_submit).pack(ipadx=10, pady=5)

        self.update_idletasks()
        self.minsize(300, self.winfo_reqheight())
        
    def update_total(self):
        total = sum([float(money.total.get() or 0) for money in self.moneyList])
        self.total.set(f"{total:.2f}")
        self.revenue.set(f"{total - 150:.2f}")

    def on_submit(self):
        difference = float(self.revenue.get() or 0) - float(self.exceptedRevenue.get() or 0)

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

        moneyHeaderFrame = tk.Frame(window)
        moneyHeaderFrame.pack(fill="x", pady=10, padx=20)
        tk.Label(moneyHeaderFrame, text="Montant", justify="center").pack(side="left", expand=True, fill="x")
        tk.Label(moneyHeaderFrame, text="Quantité", justify="center").pack(side="left", expand=True, fill="x")

        computedDailyRevenue = self.compute_daily_revenue()
        
        for money in computedDailyRevenue:
            moneyFrame = tk.Frame(window)
            moneyFrame.pack(fill="x", pady=5, padx=20)
            tk.Label(moneyFrame, text=f"{money[0]}", justify="center", width=5).pack(side="left", expand=True, fill="x")
            tk.Label(moneyFrame, text=f"{money[1]}", justify="center", width=5).pack(side="left", expand=True, fill="x")

        tk.Label(window, text="").pack()
        
        window.update_idletasks()
        window.minsize(300, window.winfo_reqheight())
        
    def validate(self, P):
        if P == "":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def compute_daily_revenue(self):

        revenue = []

        total_cash = float(self.total.get() or 0)
        amount_to_remove = total_cash - 150

        for money in sorted(self.moneyList, key=lambda x: x.value, reverse=True):

            if amount_to_remove <= 0:
                break

            max_possible = min(int(money.quantity.get() or 0), int(amount_to_remove // money.value))

            if max_possible > 0:
                revenue.append((money.value, max_possible))
                amount_to_remove -= max_possible * money.value

        return revenue
            
class MoneyWidget(tk.Frame):
    def __init__(self, parent, money, updateMainTotal):
        super().__init__(parent)
        
        self.value = money
        self.quantity = tk.StringVar(value="0")
        self.total = tk.StringVar(value="0.00")
        self.vcmd = (self.register(self.validate), "%P")
        
        self.update_main_total = updateMainTotal

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
        self.quantityEntry = tk.Entry(
            self,
            textvariable=self.quantity,
            validate="key",
            validatecommand=self.vcmd,
            width=5,
            justify="center"
        )
        self.quantityEntry.pack(side="left", padx=10)
        self.quantityEntry.bind("<FocusOut>", self.on_focus_out)

        #Increment buttons
        tk.Button(self, text="+1", command=lambda: self.increment()
            ).pack(side="left", padx=2)
        tk.Button(self, text="+5", command=lambda: self.increment(5)
            ).pack(side="left", padx=2)

        #Total label
        self.totalLabel = tk.Label(self, textvariable=self.total, width=5)
        self.totalLabel.pack(side="left", expand=True, fill="x")

    def validate(self, P):
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
        total = self.value * float(self.quantity.get() or 0)
        self.total.set(f"{total:.2f}")

def main():
    root = App()
    root.mainloop()

if __name__ == "__main__":
    main()

