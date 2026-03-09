def compute_total(money_list):
    return sum(m.total for m in money_list)


def compute_revenue(total_cash, base_cash):
    return total_cash - base_cash


def compute_daily_revenue(money_list, amount_to_remove):
    """Renvoie la répartition des billets pour atteindre le montant à retirer."""
    result = []

    for money in sorted(money_list, key=lambda x: x.value, reverse=True):
        if amount_to_remove <= 0:
            break

        max_possible = min(money.quantity, int(amount_to_remove // money.value))

        if max_possible > 0:
            result.append((money.value, max_possible))
            amount_to_remove -= max_possible * money.value

    return result