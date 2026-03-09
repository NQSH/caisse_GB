import tkinter as tk
from app.models.money import Money
from app.constants import MONEY_LIST, BASE_CASH
from app.widgets.money_widget import MoneyWidget


class MainView(tk.Frame):
    """Vue principale avec toutes les coupures et footer."""

    def __init__(self, master, on_change):
        super().__init__(master)

        self.money_models = [Money(v) for v in MONEY_LIST]
        self.widgets = []

        # Variables pour le footer
        self.total_var = tk.StringVar(value="0")
        self.revenue_var = tk.StringVar(value="0")
        self.expected_var = tk.StringVar(value="0")

        self.build_money_widgets(on_change)
        self.build_footer()

    def build_money_widgets(self, on_change):
        header = tk.Frame(self)
        header.pack(fill="x", pady=5)
        tk.Label(header, text="Montant", width=10).pack(side="left", expand=True)
        tk.Label(header, text="Quantité", width=10).pack(side="left", expand=True)
        tk.Label(header, text="Total", width=10).pack(side="left", expand=True)

        for money in self.money_models:
            widget = MoneyWidget(self, money, on_change)
            widget.pack(fill="x", pady=2)
            self.widgets.append(widget)

    def build_footer(self):
        # Total en caisse
        total_frame = tk.Frame(self)
        total_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(total_frame, text="Total en caisse").pack(side="left")
        tk.Label(total_frame, textvariable=self.total_var).pack(side="right")

        # Fond de caisse
        base_frame = tk.Frame(self)
        base_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(base_frame, text="Fond de caisse").pack(side="left")
        tk.Label(base_frame, text=BASE_CASH).pack(side="right")

        # Recette réelle
        revenue_frame = tk.Frame(self)
        revenue_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(revenue_frame, text="Recette réelle").pack(side="left")
        tk.Label(revenue_frame, textvariable=self.revenue_var).pack(side="right")

        # Recette attendue (entrée)
        expected_frame = tk.Frame(self)
        expected_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(expected_frame, text="Recette sur feuille").pack(side="left")
        self.expected_entry = tk.Entry(expected_frame, textvariable=self.expected_var, width=6, justify="right")
        self.expected_entry.pack(side="right")