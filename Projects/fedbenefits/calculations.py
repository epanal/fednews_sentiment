def calculate_lump_sum_payment(hourly_rate, leave_balance):
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance * 8  # Convert leave days to hours

def calculate_pension(high_3_salary, years_of_service, multiplier=0.01):
    """Calculate basic federal pension (FERS)."""
    return high_3_salary * years_of_service * multiplier