def decide_trade(current_price, last_price, grid_step):
    """
    Initial strategy to decide whether to trade based on grid step.
    Fiyat farkı grid_step'ten büyükse trade yapılır.
    """
    if abs((current_price - last_price) / last_price) > grid_step:
        return True
    return False