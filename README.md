# Mortgage Calculator

A comprehensive Python-based mortgage calculator that helps you analyze the total cost of home ownership, including automatic PMI removal when you reach 20% equity.

## Features

- **Accurate mortgage calculations** with principal, interest, property tax, PMI, home insurance, and HOA fees
- **Automatic PMI removal** when loan-to-value ratio reaches 80% (20% equity)
- **Multiple scenario comparison** using YAML configuration files
- **CSV export** for easy analysis in spreadsheet applications
- **Interactive mode** for quick single calculations

## Installation

Ensure you have Python 3.6+ installed. Install the required dependency:

```bash
pip install pyyaml
```

## Usage

### Method 1: YAML Configuration (Recommended for Multiple Scenarios)

1. **Edit the YAML configuration file** (`mortgage_config.yaml`) with your scenarios:

```yaml
scenarios:
  - name: "My First Scenario"
    house_price: 500000
    down_payment_percent: 10
    interest_rate: 6.5
    loan_term_years: 30
    monthly_property_tax: 400
    monthly_pmi: 250
    monthly_home_insurance: 150
    monthly_hoa: 100
```

2. **Run the calculator**:

```bash
python mortgage_calculator.py --yaml
```

Or specify custom file paths:

```bash
python mortgage_calculator.py --yaml my_config.yaml my_results.csv
```

3. **View results** in the generated CSV file (`mortgage_results.csv`)

### Method 2: Interactive Mode

Run the calculator without arguments for interactive input:

```bash
python mortgage_calculator.py
```

Follow the prompts to enter your mortgage details.

## Output

### Console Output
- Down payment amount
- Monthly principal + interest payment
- Initial total monthly payment (with PMI)
- PMI removal timeline
- Monthly payment after PMI removal
- Total PMI paid
- Total interest paid
- Total cost of ownership

### CSV Output (YAML mode)
The CSV file includes all input parameters and calculated results for easy comparison:
- Scenario details (name, house price, down payment, interest rate, loan term)
- Monthly payment breakdown
- PMI removal information
- Total costs

## How PMI Removal Works

PMI (Private Mortgage Insurance) is automatically calculated to stop once you reach 20% equity in your home:
- The calculator tracks your loan balance month by month
- When the loan balance drops to 80% of the home's value, PMI payments stop
- The total cost calculation only includes PMI for the months it's actually required
- If you put down 20% or more initially, no PMI is charged

## Example Scenarios

The included `mortgage_config.yaml` file contains 4 example scenarios:
1. **10% Down** - Shows PMI costs with minimal down payment
2. **20% Down** - No PMI required
3. **15 Year Loan** - Shorter term with higher monthly payments but less interest
4. **Lower Price** - More affordable home option

## Tips

- Compare multiple scenarios to find the best option for your situation
- Consider the trade-off between down payment size and PMI costs
- Look at total cost of ownership, not just monthly payments
- Use the CSV output to create charts and visualizations in Excel or Google Sheets

## Files

- `mortgage_calculator.py` - Main calculator script
- `mortgage_config.yaml` - Configuration file for scenarios
- `mortgage_results.csv` - Generated results (after running with --yaml)
- `README.md` - This file
