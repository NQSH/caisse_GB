import tkinter as tk


class MoneyWidget(tk.Frame):
    """Widget pour une coupure : valeur, quantité et total."""

    def __init__(self, master, money, on_change):
        super().__init__(master)

        self.money = money
        self.on_change = on_change

        self.quantity_var = tk.StringVar(value="0")
        self.total_var = tk.StringVar(value="0.00")

        self.quantity_var.trace_add("write", self.update_total)

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text=self.money.value, width=6).pack(side="left")

        tk.Button(self, text="-5", command=lambda: self.change_quantity(-5)).pack(side="left", padx=2)
        tk.Button(self, text="-1", command=lambda: self.change_quantity(-1)).pack(side="left", padx=2)

        self.entry = tk.Entry(
            self,
            textvariable=self.quantity_var,
            width=5,
            justify="center"
        )
        self.entry.pack(side="left", padx=5)

        tk.Button(self, text="+1", command=lambda: self.change_quantity(1)).pack(side="left", padx=2)
        tk.Button(self, text="+5", command=lambda: self.change_quantity(5)).pack(side="left", padx=2)

        tk.Label(self, textvariable=self.total_var, width=6).pack(side="left", padx=5)

    def change_quantity(self, delta):
        q = int(self.quantity_var.get() or 0)
        q = max(q + delta, 0)
        self.quantity_var.set(str(q))

    def update_total(self, *args):
        self.money.quantity = int(self.quantity_var.get() or 0)
        self.total_var.set(f"{self.money.total:.2f}")
        self.on_change()