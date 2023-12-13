import tkinter as tk
from tkinter import ttk
import pandas as pd
import tkinter.scrolledtext as st
def amortization_schedule_table(principal, annual_interest_rate, tenure_years):
    """
    Generate an amortization schedule in a tabular format.

    Parameters:
    principal (float): The total amount of the loan.
    annual_interest_rate (float): The annual interest rate as a percentage.
    tenure_years (int): The tenure of the loan in years.

    Returns:
    DataFrame: Amortization schedule in a table format.
    """

    #convert
    principal=int(principal)
    annual_interest_rate=float(annual_interest_rate)
    tenure_years=int(tenure_years)

    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / (12 * 100)

    # Total number of payments
    total_payments = tenure_years * 12

    # Calculate EMI
    emi = principal * monthly_interest_rate * ((1 + monthly_interest_rate)**total_payments) / (((1 + monthly_interest_rate)**total_payments) - 1)

    data = []
    remaining_principal = principal

    for month in range(1, total_payments + 1):
        interest_payment = remaining_principal * monthly_interest_rate
        principal_payment = emi - interest_payment
        remaining_principal -= principal_payment

        # Break the loop if remaining principal is less than or equal to zero
        if remaining_principal <= 0:
            break

        data.append({
            'Month': month,
            'EMI (INR)': round(emi, 2),
            'Interest (INR)': round(interest_payment, 2),
            'Principal (INR)': round(principal_payment, 2),
            'Remaining Principal (INR)': round(remaining_principal, 2)
        })

    return pd.DataFrame(data)


#principal = input("Enter the Principle")  
#annual_interest_rate = input("Enter the interest rate")
#tenure_years = input("Enter the tenure in years")
#schedule_table = amortization_schedule_table(principal, annual_interest_rate, tenure_years)
#print(schedule_table)

def calculate():
    principal = principal_var.get()
    interest_rate = interest_rate_var.get()
    tenure = tenure_var.get()

    if not principal or not interest_rate or not tenure:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Please fill all the fields correctly.")
        return

    try:
        schedule = amortization_schedule_table(principal, interest_rate, tenure)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, schedule.to_string(index=False))
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, str(e))

# Set up the main application window
root = tk.Tk()
root.title("EMI Calculator")

# Create and grid the widgets
principal_label = ttk.Label(root, text="Principal (INR):")
principal_label.grid(row=0, column=0, padx=10, pady=10)

principal_var = tk.StringVar()
principal_entry = ttk.Entry(root, textvariable=principal_var)
principal_entry.grid(row=0, column=1, padx=10, pady=10)

interest_rate_label = ttk.Label(root, text="Annual Interest Rate (%):")
interest_rate_label.grid(row=1, column=0, padx=10, pady=10)

interest_rate_var = tk.StringVar()
interest_rate_entry = ttk.Entry(root, textvariable=interest_rate_var)
interest_rate_entry.grid(row=1, column=1, padx=10, pady=10)

tenure_label = ttk.Label(root, text="Tenure (Years):")
tenure_label.grid(row=2, column=0, padx=10, pady=10)

tenure_var = tk.StringVar()
tenure_entry = ttk.Entry(root, textvariable=tenure_var)
tenure_entry.grid(row=2, column=1, padx=10, pady=10)

calculate_button = ttk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# ScrolledText widget for result
result_text = st.ScrolledText(root, wrap=tk.WORD, height=10)
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Start the GUI event loop
root.mainloop()
