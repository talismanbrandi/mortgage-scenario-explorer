import yaml
import csv
from datetime import datetime

def calculate_mortgage(house_price, down_payment_percent, interest_rate, loan_term_years, 
                     monthly_property_tax, monthly_pmi, monthly_home_insurance, monthly_hoa):
    """
    Calculate the total cost of home ownership with a mortgage.
    PMI is automatically removed once the loan balance reaches 80% of the home value (20% equity).
    
    Args:
        house_price (float): Total price of the house
        down_payment_percent (float): Down payment as a percentage (e.g., 20 for 20%)
        interest_rate (float): Annual interest rate (e.g., 3.5 for 3.5%)
        loan_term_years (int): Loan term in years
        monthly_property_tax (float): Monthly property tax
        monthly_pmi (float): Monthly PMI (Private Mortgage Insurance)
        monthly_home_insurance (float): Monthly home insurance
        monthly_hoa (float): Monthly HOA fees
        
    Returns:
        dict: Dictionary containing payment details
    """
    # Convert percentage to decimal
    down_payment = house_price * (down_payment_percent / 100)
    loan_amount = house_price - down_payment
    
    # Monthly interest rate and total number of payments
    monthly_interest_rate = (interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    
    # Calculate monthly principal + interest using the mortgage formula
    if monthly_interest_rate > 0:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / \
                         ((1 + monthly_interest_rate) ** total_payments - 1)
    else:
        monthly_payment = loan_amount / total_payments
    
    # Calculate when PMI will be removed (when LTV reaches 80%)
    # Track the loan balance month by month
    remaining_balance = loan_amount
    total_pmi_paid = 0
    pmi_removal_month = None
    ltv_threshold = house_price * 0.80  # 80% LTV = 20% equity
    
    for month in range(1, total_payments + 1):
        # Check if PMI should still be paid
        if remaining_balance > ltv_threshold and monthly_pmi > 0:
            total_pmi_paid += monthly_pmi
        elif pmi_removal_month is None and remaining_balance <= ltv_threshold:
            pmi_removal_month = month
        
        # Calculate interest and principal for this month
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
    
    # Calculate total monthly payment (initial, with PMI if applicable)
    initial_total_monthly = (monthly_payment + monthly_property_tax + 
                            monthly_pmi + monthly_home_insurance + monthly_hoa)
    
    # Calculate total monthly payment after PMI is removed
    total_monthly_without_pmi = (monthly_payment + monthly_property_tax + 
                                monthly_home_insurance + monthly_hoa)
    
    # Calculate total interest paid
    total_interest = (monthly_payment * total_payments) - loan_amount
    
    # Calculate total cost: down payment + all principal & interest + all other fees + PMI (only while active)
    total_other_fees = (monthly_property_tax + monthly_home_insurance + monthly_hoa) * total_payments
    total_cost = down_payment + (monthly_payment * total_payments) + total_other_fees + total_pmi_paid
    
    return {
        'monthly_principal_interest': round(monthly_payment, 2),
        'initial_total_monthly_payment': round(initial_total_monthly, 2),
        'total_monthly_without_pmi': round(total_monthly_without_pmi, 2),
        'total_interest_paid': round(total_interest, 2),
        'total_pmi_paid': round(total_pmi_paid, 2),
        'pmi_removal_month': pmi_removal_month,
        'total_cost_of_ownership': round(total_cost, 2),
        'down_payment': round(down_payment, 2)
    }

def get_user_input():
    """Get user input for mortgage calculation."""
    print("=== Mortgage Calculator ===")
    house_price = float(input("Enter the total price of the house: "))
    down_payment_percent = float(input("Enter the down payment percentage (e.g., 20 for 20%): "))
    interest_rate = float(input("Enter the annual interest rate (e.g., 3.5 for 3.5%): "))
    loan_term_years = int(input("Enter the loan term in years: "))
    monthly_property_tax = float(input("Enter the monthly property tax: "))
    monthly_pmi = float(input("Enter the monthly PMI (0 if none): "))
    monthly_home_insurance = float(input("Enter the monthly home insurance: "))
    monthly_hoa = float(input("Enter the monthly HOA fees (0 if none): "))
    
    return {
        'house_price': house_price,
        'down_payment_percent': down_payment_percent,
        'interest_rate': interest_rate,
        'loan_term_years': loan_term_years,
        'monthly_property_tax': monthly_property_tax,
        'monthly_pmi': monthly_pmi,
        'monthly_home_insurance': monthly_home_insurance,
        'monthly_hoa': monthly_hoa
    }

def display_results(results):
    """Display the calculation results in a user-friendly format."""
    print("\n=== Mortgage Calculation Results ===")
    print(f"Down Payment: ${results['down_payment']:,.2f}")
    print(f"\nMonthly Principal + Interest: ${results['monthly_principal_interest']:,.2f}")
    print(f"Initial Total Monthly Payment (with PMI): ${results['initial_total_monthly_payment']:,.2f}")
    
    if results['pmi_removal_month']:
        years = results['pmi_removal_month'] // 12
        months = results['pmi_removal_month'] % 12
        print(f"\n*** PMI will be removed after {years} years and {months} months ***")
        print(f"Total Monthly Payment (after PMI removal): ${results['total_monthly_without_pmi']:,.2f}")
        print(f"Total PMI Paid: ${results['total_pmi_paid']:,.2f}")
    else:
        print(f"\nTotal Monthly Payment: ${results['total_monthly_without_pmi']:,.2f}")
        print("(No PMI required - you have 20% or more equity)")
    
    print(f"\nTotal Interest Paid: ${results['total_interest_paid']:,.2f}")
    print(f"Total Cost of Ownership: ${results['total_cost_of_ownership']:,.2f}")

def load_scenarios_from_yaml(yaml_file):
    """Load mortgage scenarios from a YAML configuration file."""
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['scenarios']

def write_results_to_csv(all_results, output_file):
    """Write mortgage calculation results to a CSV file."""
    fieldnames = [
        'Scenario Name',
        'House Price',
        'Down Payment %',
        'Down Payment $',
        'Loan Amount',
        'Interest Rate %',
        'Loan Term (Years)',
        'Monthly Property Tax',
        'Monthly PMI',
        'Monthly Home Insurance',
        'Monthly HOA',
        'Monthly Principal + Interest',
        'Initial Total Monthly Payment',
        'Monthly Payment After PMI Removal',
        'PMI Removal Month',
        'PMI Removal Time',
        'Total PMI Paid',
        'Total Interest Paid',
        'Total Cost of Ownership'
    ]
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in all_results:
            writer.writerow(result)
    
    print(f"\nResults written to {output_file}")

def process_yaml_scenarios(yaml_file='mortgage_config.yaml', output_csv='mortgage_results.csv'):
    """Process all scenarios from YAML file and write results to CSV."""
    try:
        # Load scenarios from YAML
        scenarios = load_scenarios_from_yaml(yaml_file)
        print(f"Loaded {len(scenarios)} scenarios from {yaml_file}")
        
        all_results = []
        
        # Process each scenario
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'='*60}")
            print(f"Processing: {scenario.get('name', f'Scenario {i}')}")
            print(f"{'='*60}")
            
            # Calculate mortgage for this scenario
            results = calculate_mortgage(
                house_price=scenario['house_price'],
                down_payment_percent=scenario['down_payment_percent'],
                interest_rate=scenario['interest_rate'],
                loan_term_years=scenario['loan_term_years'],
                monthly_property_tax=scenario['monthly_property_tax'],
                monthly_pmi=scenario['monthly_pmi'],
                monthly_home_insurance=scenario['monthly_home_insurance'],
                monthly_hoa=scenario['monthly_hoa']
            )
            
            # Display results to console
            display_results(results)
            
            # Calculate loan amount
            loan_amount = scenario['house_price'] - results['down_payment']
            
            # Format PMI removal time
            pmi_removal_time = ''
            if results['pmi_removal_month']:
                years = results['pmi_removal_month'] // 12
                months = results['pmi_removal_month'] % 12
                pmi_removal_time = f"{years}y {months}m"
            else:
                pmi_removal_time = 'N/A (20%+ equity)'
            
            # Prepare CSV row
            csv_row = {
                'Scenario Name': scenario.get('name', f'Scenario {i}'),
                'House Price': f"${scenario['house_price']:,.2f}",
                'Down Payment %': f"{scenario['down_payment_percent']}%",
                'Down Payment $': f"${results['down_payment']:,.2f}",
                'Loan Amount': f"${loan_amount:,.2f}",
                'Interest Rate %': f"{scenario['interest_rate']}%",
                'Loan Term (Years)': scenario['loan_term_years'],
                'Monthly Property Tax': f"${scenario['monthly_property_tax']:,.2f}",
                'Monthly PMI': f"${scenario['monthly_pmi']:,.2f}",
                'Monthly Home Insurance': f"${scenario['monthly_home_insurance']:,.2f}",
                'Monthly HOA': f"${scenario['monthly_hoa']:,.2f}",
                'Monthly Principal + Interest': f"${results['monthly_principal_interest']:,.2f}",
                'Initial Total Monthly Payment': f"${results['initial_total_monthly_payment']:,.2f}",
                'Monthly Payment After PMI Removal': f"${results['total_monthly_without_pmi']:,.2f}",
                'PMI Removal Month': results['pmi_removal_month'] if results['pmi_removal_month'] else 'N/A',
                'PMI Removal Time': pmi_removal_time,
                'Total PMI Paid': f"${results['total_pmi_paid']:,.2f}",
                'Total Interest Paid': f"${results['total_interest_paid']:,.2f}",
                'Total Cost of Ownership': f"${results['total_cost_of_ownership']:,.2f}"
            }
            
            all_results.append(csv_row)
        
        # Write all results to CSV
        write_results_to_csv(all_results, output_csv)
        
        print(f"\n{'='*60}")
        print(f"Successfully processed {len(scenarios)} scenarios!")
        print(f"{'='*60}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {yaml_file}")
        print("Please ensure the YAML configuration file exists.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import sys
    
    # Check if user wants to use YAML mode or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--yaml':
        # YAML mode: read from config file and output to CSV
        yaml_file = sys.argv[2] if len(sys.argv) > 2 else 'mortgage_config.yaml'
        output_csv = sys.argv[3] if len(sys.argv) > 3 else 'mortgage_results.csv'
        process_yaml_scenarios(yaml_file, output_csv)
    else:
        # Interactive mode: get user input
        try:
            inputs = get_user_input()
            results = calculate_mortgage(**inputs)
            display_results(results)
        except ValueError as e:
            print(f"Error: Please enter valid numbers. {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
