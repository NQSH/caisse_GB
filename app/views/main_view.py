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
        total_frame = self.create_footer_line("Total en caisse")
        tk.Label(total_frame, textvariable=self.total_var).pack(side="right")

        # Fond de caisse
        base_frame = self.create_footer_line("Fond de caisse")
        tk.Label(base_frame, text=BASE_CASH).pack(side="right")

        # Recette réelle
        revenue_frame = self.create_footer_line("Recette réelle")
        tk.Label(revenue_frame, textvariable=self.revenue_var).pack(side="right")

        # Recette attendue (entrée)
        expected_frame = self.create_footer_line("Recette sur feuille de caisse")
        tk.Entry(expected_frame, textvariable=self.expected_var, width=6, justify="right").pack(side="right")

    def create_footer_line(self, label_text):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=5, padx=10)
        tk.Label(frame, text=label_text).pack(side="left")
        return frame