# Enhanced Financial Term Matcher

This repository now includes an enhanced financial term matcher with better confidence handling and improved user experience.

## Features

### 1. Enhanced Confidence Logic
- **< 0.3**: No related terms found
- **0.3 - 0.6**: Multiple suggestions (if partial match)
- **0.6 - 0.8**: Single suggestion with confirmation
- **> 0.8**: Direct match (only for exact or very close matches)

### 2. Improved Terminal Interface
- Better formatting and user experience
- Show multiple suggestions when available
- Handle case variations explicitly
- Add confidence score display for debugging

### 3. Query Preprocessing
- Automatically removes common prefixes like "what is", "define", "explain"
- Case-insensitive matching
- Support for abbreviations and aliases

### 4. Financial Terms Database
The system includes 8 comprehensive financial terms:
- Annual Income
- Annual Percentage Rate (APR)
- Annual Report
- Cash Flow
- Return on Investment (ROI)
- Gross Domestic Product (GDP)
- Net Present Value (NPV)
- Interest Rate

## Usage

### Running the Financial Term Matcher
```bash
python3 financial_term_matcher.py
```

### Example Interactions

#### Partial Match (Multiple Suggestions):
```
Query: "what is annual"
Response: Found multiple related terms for 'annual':
1. Annual Income
   Category: Income
2. Annual Report
   Category: Reporting
3. Annual Percentage Rate
   Category: Interest

Which one did you mean?
```

#### Exact Match:
```
Query: "Annual Income"
Response: ✓ Annual Income
Category: Income
Definition: The total amount of money earned by an individual or entity in a year, including salary, wages, bonuses, and other sources of income.
Also known as: yearly income, annual earnings, yearly earnings
```

#### Abbreviation Match:
```
Query: "ROI"
Response: ✓ Return on Investment
Category: Investment
Definition: A performance measure used to evaluate the efficiency of an investment or compare the efficiency of several investments.
Also known as: ROI, investment return, return on capital
```

#### No Match:
```
Query: "xyz random"
Response: "There are no related terms present"
```

## Testing

### Run Financial Term Matcher Tests
```bash
python3 test_financial_matcher.py
```

### Run Original Calculator Tests
```bash
python3 test.py
```

Both test suites pass with 100% success rate.

## Architecture

The system is built using:
- **FinancialTermMatcher**: Main class handling search logic and confidence scoring
- **FinancialTerm**: Data class for term definitions and metadata
- **MatchResult**: Data class for search results with confidence scores
- Comprehensive test suite with 16 test cases covering all functionality

## Integration

The financial term matcher is implemented as a standalone module that doesn't interfere with the existing calculator functionality. Both systems can be used independently.