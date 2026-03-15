import tkinter as tk
from app.services.window_service import lock_window_size

class ResultWindow(tk.Toplevel):
    """Fenêtre de résultat avec message et répartition de billets."""

    def __init__(self, master, message, color, revenue_list):
        super().__init__(master)
        self.title("Résultat")

        tk.Label(self, text=message, fg=color).pack(pady=10)

        tk.Label(self, text="Espèces à mettre dans la pochette :").pack()

        # Entêtes
        header = tk.Frame(self)
        header.pack(fill="x", pady=5, padx=20)
        tk.Label(header, text="Montant").pack(side="left", expand=True)
        tk.Label(header, text="Quantité").pack(side="left", expand=True)

        # Liste des billets
        for value, quantity in revenue_list:
            frame = tk.Frame(self)
            frame.pack(fill="x", pady=2, padx=20)
            tk.Label(frame, text=value).pack(side="left", expand=True)
            tk.Label(frame, text=quantity).pack(side="left", expand=True)

        lock_window_size(self)