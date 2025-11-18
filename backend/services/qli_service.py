def calculate_qli(economy: float, health: float, climate: float, safety: float) -> float:
    qli = 0.35 * economy + 0.25 * health + 0.25 * climate + 0.15 * safety
    return round(qli, 3)
