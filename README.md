# Mortgage Calculator with Desired Monthly Payment

A comprehensive Python-based mortgage calculator that helps you analyze the total cost of home ownership. Set your **desired monthly payment** and see exactly how it affects your payoff timeline, interest costs, and PMI removal!

## 🎯 What This Calculator Does

Instead of asking "how much extra do you want to pay?", this calculator asks:
> **"What monthly payment can you afford?"**

This is more intuitive because you budget in terms of total monthly payments. The calculator automatically validates your payment is sufficient, calculates how much extra goes toward principal, and shows you the complete payoff timeline.

## ✨ Key Features

- **Desired Monthly Payment** - Specify what you want to pay each month
- **Constant Payment Strategy** - Payment stays the same even after PMI removal (PMI savings go to principal!)
- **Automatic Validation** - Ensures your desired payment meets or exceeds the minimum required
- **Accurate Mortgage Calculations** - Principal, interest, property tax, PMI, home insurance, and HOA fees
- **Automatic PMI Removal** - Stops at 20% equity (80% LTV)
- **Payoff Timeline Projection** - Shows actual vs original payoff time and savings
- **Multiple Scenario Comparison** - YAML configuration for easy comparison
- **CSV Export** - Perfect for Excel/Google Sheets analysis
- **Interactive Mode** - Quick single calculations

## 📊 Real Example Results

**House**: $670,000 with 10% down ($603,000 loan)  
**Rate**: 6.33% for 30 years  
**Other Costs**: $982/month (tax, PMI, insurance, HOA)

| Monthly Payment | Time to Payoff | Time Saved | Total Interest | Total Cost | Savings vs Minimum |
|----------------|----------------|------------|----------------|------------|-------------------|
| $4,726 (min) | 29y 3m | - | $725,251 | $1,723,098 | - |
| $5,000 | 24y 4m | 5y 8m | $581,128 | $1,523,182 | **$199,916** |
| $5,500 | 18y 11m | 11y 1m | $434,305 | $1,315,324 | **$407,774** |
| $6,000 | 15y 8m | 14y 4m | $349,838 | $1,194,379 | **$528,719** |

### Key Insights:
- **$274/month extra** ($5,000 total) saves nearly **$200,000** and **5.7 years**
- **$1,274/month extra** ($6,000 total) saves over **$500,000** and **14+ years**
- PMI is removed faster with higher payments (5y 7m vs 7y 9m)
- **Payment stays constant** - when PMI is removed, that money goes to principal!

## Installation

Ensure you have Python 3.6+ installed. Install the required dependency:

```bash
pip install pyyaml
```

## 🚀 Quick Start

```bash
# Install dependency
pip install pyyaml

# Run with example scenarios
python3 mortgage_calculator.py --yaml

# View results
open mortgage_results.csv
```

## Usage

### Method 1: YAML Configuration (Recommended for Multiple Scenarios)

1. **Edit the YAML configuration file** (`mortgage_config.yaml`) with your scenarios:

```yaml
scenarios:
  - name: "Minimum Payment Scenario"
    house_price: 500000
    down_payment_percent: 10
    interest_rate: 6.5
    loan_term_years: 30
    monthly_property_tax: 400
    monthly_pmi: 250
    monthly_home_insurance: 150
    monthly_hoa: 100
    # Omit desired_monthly_payment to use minimum
  
  - name: "$5000/month Payment Scenario"
    house_price: 500000
    down_payment_percent: 10
    interest_rate: 6.5
    loan_term_years: 30
    monthly_property_tax: 400
    monthly_pmi: 250
    monthly_home_insurance: 150
    monthly_hoa: 100
    desired_monthly_payment: 5000  # Your target monthly payment
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
- **Minimum P&I payment** (what you must pay at minimum)
- **Minimum total monthly payment** (including all costs)
- **Desired monthly payment** (your target payment)
- **Extra toward principal** (how much extra goes to principal)
- Validation message (confirms payment is above minimum)
- Initial total monthly payment (with PMI)
- PMI removal timeline
- Monthly payment after PMI removal
- Total PMI paid
- **Loan payoff timeline** (original term vs actual payoff time)
- **Time saved** with your payment strategy
- Total interest paid
- Total cost of ownership

### CSV Output (YAML mode)
The CSV file includes all input parameters and calculated results for easy comparison:
- Scenario details (name, house price, down payment, interest rate, loan term)
- Minimum P&I and total payments
- Desired monthly payment amount
- Extra toward principal
- Monthly payment breakdown
- PMI removal information
- **Original loan term vs actual payoff time**
- **Months and years saved**
- Total costs

## How PMI Removal Works

PMI (Private Mortgage Insurance) is automatically calculated to stop once you reach 20% equity in your home:
- The calculator tracks your loan balance month by month
- When the loan balance drops to 80% of the home's value, PMI payments stop
- The total cost calculation only includes PMI for the months it's actually required
- If you put down 20% or more initially, no PMI is charged

## 🎓 How It Works

### 1. Calculate Minimum Payment
```
Minimum P&I = Standard mortgage formula
Minimum Total = P&I + Tax + PMI + Insurance + HOA
```

### 2. Validate Desired Payment
```
If desired_payment < minimum_total:
    ERROR: Payment too low!
```

### 3. Calculate Extra Principal
```
Extra = Desired Payment - Minimum Total
```

### 4. Month-by-Month Simulation
For each month:
- Calculate interest on remaining balance
- Apply desired payment
- Extra amount goes directly to principal
- Track when PMI can be removed (80% LTV)
- Continue until loan is paid off

### 5. Calculate Savings
```
Time Saved = Original Term - Actual Payoff Time
Interest Saved = Original Interest - Actual Interest
```

## 💡 Constant Payment Strategy

### How It Works
This calculator implements a **constant monthly payment** strategy. When PMI is removed, your monthly payment **stays the same**, but the PMI amount now goes directly toward **extra principal reduction**.

### Example: $5,000/month Payment

#### Phase 1: With PMI (Months 1-67)
```
Monthly Payment:        $5,000.00 (constant)
├─ P&I Payment:         $3,744.21
├─ Property Tax:          $325.00
├─ PMI:                    $65.00  ← Goes away at month 67
├─ Home Insurance:         $60.00
├─ HOA:                   $532.00
└─ Extra to Principal:    $273.79
```

#### Phase 2: After PMI Removal (Months 68-292)
```
Monthly Payment:        $5,000.00 (SAME!)
├─ P&I Payment:         $3,744.21
├─ Property Tax:          $325.00
├─ PMI:                     $0.00  ← Removed!
├─ Home Insurance:         $60.00
├─ HOA:                   $532.00
└─ Extra to Principal:    $338.79  ← Increased by $65!
```

**Key Point:** The $65 that was going to PMI now goes to principal, accelerating your payoff even more!

### Benefits of Constant Payment

1. **Predictable Budgeting** - Your monthly payment never changes
2. **Automatic Acceleration** - PMI savings automatically go to principal
3. **Faster PMI Removal** - Extra principal payments build equity faster
4. **Maximum Savings** - Combines extra payments + PMI reinvestment

### Real Savings Example

**$5,000/month vs Minimum Payment:**

| Metric | Minimum | $5,000/month | Savings |
|--------|---------|--------------|---------|
| Monthly Payment | $4,726 | $5,000 | -$274/month |
| PMI Removed At | 7y 9m | 5y 7m | 2y 2m sooner |
| Total PMI Paid | $5,980 | $4,290 | **$1,690** |
| Payoff Time | 29y 3m | 24y 4m | **5y 8m** |
| Total Interest | $725,251 | $581,128 | **$144,123** |
| Total Cost | $1,723,098 | $1,523,182 | **$199,916** |

**By paying just $274 more per month, you save nearly $200,000!**

## 📈 Output Details

### Console Output
For each scenario, you'll see:
- ✅ Minimum payment required (validation)
- ✅ Your desired payment (constant throughout loan)
- ✅ How much extra goes to principal (initially and after PMI removal)
- ✅ When PMI will be removed
- ✅ Actual payoff time
- ✅ Time and money saved
- ✅ Total interest and total cost

### CSV Export
A spreadsheet with all scenarios including:
- All input parameters
- Minimum vs desired payments
- Monthly payment breakdown
- PMI removal timeline
- Extra principal (initial and after PMI removal)
- Payoff timeline comparison
- Total costs and savings

Perfect for:
- Creating charts in Excel/Google Sheets
- Comparing multiple scenarios side-by-side
- Sharing with financial advisors
- Making informed decisions

## 💡 Pro Tips

### Finding Your Sweet Spot
1. Start with minimum payment scenario
2. Try increments of $250-500 above minimum
3. Look at the "Time Saved" and "Interest Saved" columns
4. Find the payment that balances your budget with savings goals

### Maximizing Savings
- **Every dollar extra** goes directly to principal (after minimum costs)
- **Front-loading** extra payments saves the most interest
- **Consistency** is key - maintain the same payment throughout
- **PMI removal** happens faster, creating additional savings
- **Constant payment** after PMI removal maximizes benefit

### Budget Planning
- Use the minimum payment as your baseline
- Add extra only if you can sustain it long-term
- Consider keeping some buffer for emergencies
- Remember: you can always pay more, but can't pay less than minimum
- The calculator will warn you if your desired payment is below the minimum

## 🔒 Built-in Safeguards

1. **Payment Validation** - Ensures you can't set a payment below the minimum
2. **PMI Auto-Removal** - Automatically stops PMI at 20% equity
3. **Accurate Interest Calculation** - Month-by-month tracking for precision
4. **Overpayment Prevention** - Won't charge you more than the remaining balance
5. **Safety Limits** - Prevents infinite loops with maximum iteration checks

## 🎯 Use Cases

### Home Buyers
- Compare different payment strategies before buying
- Understand true cost of homeownership
- Plan budget with different scenarios

### Current Homeowners
- See impact of increasing monthly payment
- Calculate when you can remove PMI
- Plan for early payoff

### Financial Advisors
- Show clients multiple scenarios
- Demonstrate power of extra payments
- Export data for presentations

### Real Estate Professionals
- Help buyers understand affordability
- Show long-term cost implications
- Compare different loan structures

## 🚨 Important Notes

1. **Property Tax & Insurance**: May increase over time (calculator uses fixed values)
2. **PMI Rates**: Verify your actual PMI rate with lender
3. **Interest Rates**: Use your actual rate, not advertised rates
4. **HOA Fees**: Can change annually
5. **Prepayment Penalties**: Some loans have them (check your terms)
6. **Constant Payment**: Default behavior - payment stays same after PMI removal

## 🔄 Backward Compatibility

Old YAML files using `extra_monthly_payment` still work:
```yaml
# Old format (still supported)
extra_monthly_payment: 300

# Automatically converted to:
# desired_monthly_payment = minimum + 300
```

## 📁 Project Files

- **mortgage_calculator.py** - Main calculator script
- **mortgage_config.yaml** - Scenario configuration
- **mortgage_results.csv** - Generated output
- **README.md** - This comprehensive guide
- **requirements.txt** - Python dependencies

## 📞 Getting Help

If you encounter issues:
1. Check that desired payment ≥ minimum payment
2. Verify all YAML fields are filled correctly
3. Ensure PyYAML is installed: `pip install pyyaml`
4. Review error messages - they're descriptive

## Quick Reference Commands

```bash
# Run with default config
python3 mortgage_calculator.py --yaml

# Run with custom config
python3 mortgage_calculator.py --yaml my_config.yaml my_output.csv

# Interactive mode
python3 mortgage_calculator.py

# Install dependencies
pip install -r requirements.txt
```

---

**Built with Python 3.6+**  
**Dependencies**: PyYAML  
**License**: Use freely for personal or commercial purposes

**The power of consistent extra payments can save you hundreds of thousands of dollars!**
