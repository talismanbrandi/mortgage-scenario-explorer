import yaml
import csv
from datetime import datetime

def calculate_mortgage(house_price, down_payment_percent, interest_rate, loan_term_years, 
                     monthly_property_tax, monthly_pmi, monthly_home_insurance, monthly_hoa, 
                     desired_monthly_payment=None):
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
        desired_monthly_payment (float): Total desired monthly payment including all costs (optional)
        
    Returns:
        dict: Dictionary containing payment details
    """
    # Convert percentage to decimal
    down_payment = house_price * (down_payment_percent / 100)
    loan_amount = house_price - down_payment
    
    # PMI is not required if down payment is 20% or more
    # Override monthly_pmi to 0 if down payment >= 20%
    if down_payment_percent >= 20:
        monthly_pmi = 0
    
    # Monthly interest rate and total number of payments
    monthly_interest_rate = (interest_rate / 100) / 12
    total_payments = loan_term_years * 12
    
    # Calculate minimum monthly principal + interest using the mortgage formula
    if monthly_interest_rate > 0:
        min_principal_interest = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / \
                         ((1 + monthly_interest_rate) ** total_payments - 1)
    else:
        min_principal_interest = loan_amount / total_payments
    
    # Calculate minimum total monthly payment (with all costs)
    min_total_payment = min_principal_interest + monthly_property_tax + monthly_pmi + monthly_home_insurance + monthly_hoa
    
    # Determine actual payment to use
    if desired_monthly_payment is not None:
        if desired_monthly_payment < min_total_payment:
            raise ValueError(f"Desired monthly payment (${desired_monthly_payment:,.2f}) is less than minimum required payment (${min_total_payment:,.2f})")
        actual_total_payment = desired_monthly_payment
        extra_toward_principal = desired_monthly_payment - min_total_payment
    else:
        actual_total_payment = min_total_payment
        extra_toward_principal = 0
    
    # Track the loan balance month by month
    remaining_balance = loan_amount
    total_pmi_paid = 0
    total_interest_paid = 0
    total_principal_paid = 0
    pmi_removal_month = None
    actual_payoff_month = 0
    ltv_threshold = house_price * 0.80  # 80% LTV = 20% equity
    
    month = 0
    max_months = total_payments * 3  # Safety limit
    
    while remaining_balance > 0.01 and month < max_months:  # Small threshold for rounding
        month += 1
        
        # Calculate interest for this month
        interest_payment = remaining_balance * monthly_interest_rate
        total_interest_paid += interest_payment
        
        # Calculate how much goes to principal this month
        # Start with minimum P&I payment
        principal_from_min_payment = min_principal_interest - interest_payment
        
        # Add extra payment (if any) - all goes to principal
        # But account for PMI removal
        current_pmi = monthly_pmi if remaining_balance > ltv_threshold else 0
        current_other_costs = monthly_property_tax + current_pmi + monthly_home_insurance + monthly_hoa
        
        # Total available for principal = desired payment - interest - other costs
        total_principal_payment = actual_total_payment - interest_payment - current_other_costs
        
        # Don't overpay on the last payment
        if total_principal_payment > remaining_balance:
            total_principal_payment = remaining_balance
        
        total_principal_paid += total_principal_payment
        remaining_balance -= total_principal_payment
        
        # Track PMI payments
        if remaining_balance > ltv_threshold and monthly_pmi > 0:
            total_pmi_paid += monthly_pmi
        elif pmi_removal_month is None and remaining_balance <= ltv_threshold:
            pmi_removal_month = month
        
        # Check if loan is paid off
        if remaining_balance <= 0.01:
            actual_payoff_month = month
            break
    
    # Calculate extra principal after PMI removal
    # When PMI is removed, the same total payment continues, but PMI amount now goes to principal
    extra_principal_after_pmi_removal = extra_toward_principal + monthly_pmi if pmi_removal_month else extra_toward_principal
    
    # Calculate total cost: down payment + all interest + all other fees + PMI (only while active)
    total_other_fees = (monthly_property_tax + monthly_home_insurance + monthly_hoa) * actual_payoff_month
    total_cost = down_payment + loan_amount + total_interest_paid + total_other_fees + total_pmi_paid
    
    # Calculate time saved
    original_months = loan_term_years * 12
    months_saved = original_months - actual_payoff_month
    
    return {
        'min_principal_interest': round(min_principal_interest, 2),
        'min_total_monthly_payment': round(min_total_payment, 2),
        'desired_monthly_payment': round(actual_total_payment, 2) if desired_monthly_payment else None,
        'extra_toward_principal': round(extra_toward_principal, 2),
        'extra_principal_after_pmi_removal': round(extra_principal_after_pmi_removal, 2),
        'monthly_payment_amount': round(actual_total_payment, 2),  # Stays constant
        'total_interest_paid': round(total_interest_paid, 2),
        'total_pmi_paid': round(total_pmi_paid, 2),
        'pmi_removal_month': pmi_removal_month,
        'actual_payoff_month': actual_payoff_month,
        'original_term_months': original_months,
        'months_saved': months_saved,
        'total_cost_of_ownership': round(total_cost, 2),
        'down_payment': round(down_payment, 2),
        'down_payment_percent': down_payment_percent,
        'is_paying_extra': desired_monthly_payment is not None and desired_monthly_payment > min_total_payment,
        'pmi_amount': round(monthly_pmi, 2)
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
    
    desired_payment_input = input("Enter desired total monthly payment (press Enter to use minimum): ").strip()
    desired_monthly_payment = float(desired_payment_input) if desired_payment_input else None
    
    return {
        'house_price': house_price,
        'down_payment_percent': down_payment_percent,
        'interest_rate': interest_rate,
        'loan_term_years': loan_term_years,
        'monthly_property_tax': monthly_property_tax,
        'monthly_pmi': monthly_pmi,
        'monthly_home_insurance': monthly_home_insurance,
        'monthly_hoa': monthly_hoa,
        'desired_monthly_payment': desired_monthly_payment
    }

def display_results(results):
    """Display the calculation results in a user-friendly format."""
    print("\n=== Mortgage Calculation Results ===")
    print(f"Down Payment: ${results['down_payment']:,.2f}")
    
    print(f"\n*** Monthly Payment Breakdown ***")
    print(f"Minimum P&I Payment: ${results['min_principal_interest']:,.2f}")
    print(f"Minimum Total Monthly Payment: ${results['min_total_monthly_payment']:,.2f}")
    
    if results['desired_monthly_payment']:
        print(f"\nDesired Monthly Payment: ${results['desired_monthly_payment']:,.2f} (constant throughout loan)")
        if results['is_paying_extra']:
            print(f"Extra Toward Principal (initially): ${results['extra_toward_principal']:,.2f}")
            print("✓ Payment is ABOVE minimum - loan will pay off early!")
        else:
            print("✓ Payment equals minimum - standard payoff schedule")
    else:
        print("\nUsing Minimum Payment (no extra principal)")
    
    # Check if down payment is 20% or more
    if results['down_payment_percent'] >= 20:
        print(f"\n*** No PMI Required ***")
        print("(Down payment is 20% or more)")
    elif results['pmi_removal_month']:
        years = results['pmi_removal_month'] // 12
        months = results['pmi_removal_month'] % 12
        print(f"\n*** PMI Removal Impact ***")
        print(f"PMI will be removed after {years} years and {months} months")
        print(f"PMI Amount: ${results['pmi_amount']:,.2f}/month")
        print(f"Total PMI Paid: ${results['total_pmi_paid']:,.2f}")
        print(f"\n💡 After PMI removal:")
        print(f"   Monthly payment stays: ${results['monthly_payment_amount']:,.2f}")
        print(f"   Extra to principal becomes: ${results['extra_principal_after_pmi_removal']:,.2f}")
        print(f"   (PMI savings of ${results['pmi_amount']:,.2f} now goes to principal!)")
    else:
        print(f"\n*** No PMI Required ***")
        print("(You have 20% or more equity from the start)")
    
    # Display payoff timeline
    payoff_years = results['actual_payoff_month'] // 12
    payoff_months = results['actual_payoff_month'] % 12
    print(f"\n*** Loan Payoff Timeline ***")
    print(f"Original Loan Term: {results['original_term_months'] // 12} years ({results['original_term_months']} months)")
    print(f"Actual Payoff Time: {payoff_years} years and {payoff_months} months ({results['actual_payoff_month']} months)")
    
    if results['months_saved'] > 0:
        saved_years = results['months_saved'] // 12
        saved_months = results['months_saved'] % 12
        print(f"⭐ Time Saved: {saved_years} years and {saved_months} months ({results['months_saved']} months)")
    
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
        'Min P&I Payment',
        'Min Total Payment',
        'Desired Monthly Payment (Constant)',
        'Extra Toward Principal (Initial)',
        'Extra Toward Principal (After PMI Removal)',
        'PMI Removal Month',
        'PMI Removal Time',
        'Total PMI Paid',
        'Original Term (Months)',
        'Actual Payoff (Months)',
        'Actual Payoff Time',
        'Time Saved (Months)',
        'Time Saved',
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
            # Support both old 'extra_monthly_payment' and new 'desired_monthly_payment' format
            desired_payment = scenario.get('desired_monthly_payment')
            if desired_payment is None and 'extra_monthly_payment' in scenario:
                # Legacy support: convert extra_monthly_payment to desired_monthly_payment
                # First calculate minimum payment
                temp_results = calculate_mortgage(
                    house_price=scenario['house_price'],
                    down_payment_percent=scenario['down_payment_percent'],
                    interest_rate=scenario['interest_rate'],
                    loan_term_years=scenario['loan_term_years'],
                    monthly_property_tax=scenario['monthly_property_tax'],
                    monthly_pmi=scenario['monthly_pmi'],
                    monthly_home_insurance=scenario['monthly_home_insurance'],
                    monthly_hoa=scenario['monthly_hoa'],
                    desired_monthly_payment=None
                )
                extra = scenario.get('extra_monthly_payment', 0)
                if extra > 0:
                    desired_payment = temp_results['min_total_monthly_payment'] + extra
            
            results = calculate_mortgage(
                house_price=scenario['house_price'],
                down_payment_percent=scenario['down_payment_percent'],
                interest_rate=scenario['interest_rate'],
                loan_term_years=scenario['loan_term_years'],
                monthly_property_tax=scenario['monthly_property_tax'],
                monthly_pmi=scenario['monthly_pmi'],
                monthly_home_insurance=scenario['monthly_home_insurance'],
                monthly_hoa=scenario['monthly_hoa'],
                desired_monthly_payment=desired_payment
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
            
            # Format actual payoff time
            payoff_years = results['actual_payoff_month'] // 12
            payoff_months = results['actual_payoff_month'] % 12
            actual_payoff_time = f"{payoff_years}y {payoff_months}m"
            
            # Format time saved
            time_saved_str = ''
            if results['months_saved'] > 0:
                saved_years = results['months_saved'] // 12
                saved_months = results['months_saved'] % 12
                time_saved_str = f"{saved_years}y {saved_months}m"
            else:
                time_saved_str = 'None'
            
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
                'Min P&I Payment': f"${results['min_principal_interest']:,.2f}",
                'Min Total Payment': f"${results['min_total_monthly_payment']:,.2f}",
                'Desired Monthly Payment (Constant)': f"${results['desired_monthly_payment']:,.2f}" if results['desired_monthly_payment'] else 'N/A',
                'Extra Toward Principal (Initial)': f"${results['extra_toward_principal']:,.2f}",
                'Extra Toward Principal (After PMI Removal)': f"${results['extra_principal_after_pmi_removal']:,.2f}",
                'PMI Removal Month': results['pmi_removal_month'] if results['pmi_removal_month'] else 'N/A',
                'PMI Removal Time': pmi_removal_time,
                'Total PMI Paid': f"${results['total_pmi_paid']:,.2f}",
                'Original Term (Months)': results['original_term_months'],
                'Actual Payoff (Months)': results['actual_payoff_month'],
                'Actual Payoff Time': actual_payoff_time,
                'Time Saved (Months)': results['months_saved'],
                'Time Saved': time_saved_str,
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
