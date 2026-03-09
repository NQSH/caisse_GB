import tkinter as tk
from app.constants import BASE_CASH
from app.views.main_view import MainView
from app.views.result_window import ResultWindow
from app.services.cash_service import compute_total, compute_revenue, compute_daily_revenue


class App(tk.Tk):
    """Application principale."""

    def __init__(self):
        super().__init__()
        self.title("Caisse")

        # Vue principale
        self.view = MainView(self, self.update_totals)
        self.view.pack()

        # Bouton valider
        tk.Button(self.view, text="Valider", command=self.on_submit).pack(pady=5)

    def update_totals(self):
        total = compute_total(self.view.money_models)
        revenue = compute_revenue(total, BASE_CASH)
        self.view.total_var.set(f"{total:.2f}")
        self.view.revenue_var.set(f"{revenue:.2f}")

    def on_submit(self):
        total = float(self.view.revenue_var.get())
        expected = float(self.view.expected_var.get() or 0)
        difference = total - expected

        if difference == 0:
            message = "Votre caisse est juste !"
            color = "green"
        else:
            color = "red"
            if difference > 0:
                message = f"Vous avez {difference:.2f}€ en trop.\nMerci de prévenir un responsable."
            else:
                message = f"Il vous manque {abs(difference):.2f}€.\nMerci de prévenir un responsable."

        revenue_list = compute_daily_revenue(self.view.money_models, total)

        ResultWindow(self, message, color, revenue_list)