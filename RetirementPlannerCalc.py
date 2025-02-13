#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv

# Function to read rates from the CSV file
def read_rates(filename):
    rates = {'stocks': [], 'bonds': []}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rates['stocks'].append(float(row['S&P 500 '].strip('%')) / 100)
            rates['bonds'].append(float(row['US T. Bond (10-year)'].strip('%')) / 100)
    return rates

# Function to calculate yearly balance
def calculate_balance(balance, rate, contribution):
    return round(balance * (1 + rate) + contribution, 2)

# Main function
def retirement_calculator():
    # Read bond and stock rates from the CSV file
    rates = read_rates('BondsAndStocksAnnualReturn.csv')

    # Get user input
    current_age = int(input("How old are you? "))
    retirement_age = int(input("At what age do you want to retire? "))
    years_until_retirement = retirement_age - current_age

    # Initialize balances
    balances = {
        'mattress': round(float(input("Enter money stored under your mattress: ")), 2),
        'savings': round(float(input("Enter money in bank savings: ")), 2),
        'bonds': round(float(input("Enter money in bonds: ")), 2),
        'stocks': round(float(input("Enter money in stocks: ")), 2)
    }

    # Initialize CSV file
    with open('retirement_balances.csv', 'w', newline='') as csvfile:
        fieldnames = ['Year', 'Mattress', 'Savings', 'Bonds', 'Stocks', 'Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for year in range(years_until_retirement):
            print(f"\nYear {year + 1} of {years_until_retirement}")
            contributions = {'mattress': 0, 'savings': 0, 'bonds': 0, 'stocks': 0}

            # Ask the user which accounts they want to deposit into
            for account in contributions:
                deposit = input(f"Do you want to add money to {account} this year? (yes/no): ").strip().lower()
                if deposit == 'yes':
                    contributions[account] = round(float(input(f"How much do you want to add to {account} this year? ")), 2)

            # Apply contributions and calculate new balances
            balances['mattress'] = round(balances['mattress'] + contributions['mattress'], 2)
            balances['savings'] = calculate_balance(balances['savings'], 0.02, contributions['savings'])
            balances['bonds'] = calculate_balance(balances['bonds'], rates['bonds'][year], contributions['bonds'])
            balances['stocks'] = calculate_balance(balances['stocks'], rates['stocks'][year], contributions['stocks'])

            total_balance = round(sum(balances.values()), 2)
            writer.writerow({
                'Year': year + 1,
                'Mattress': balances['mattress'],
                'Savings': balances['savings'],
                'Bonds': balances['bonds'],
                'Stocks': balances['stocks'],
                'Total': total_balance
            })

            print(f"Current balances: {balances}")
            print(f"Total balance: {total_balance}")

    # Adjust for inflation
    inflation_rate = 0.02
    adjusted_total = round(total_balance / ((1 + inflation_rate) ** years_until_retirement), 2)

    print(f"\nFinal balances at retirement: {balances}")
    print(f"Total retirement savings: {total_balance}")
    print(f"Inflation-adjusted balance: {adjusted_total}")

# Run the calculator
retirement_calculator()


# In[ ]:




