#!/usr/bin/python3
"""
Enhanced Financial Term Matcher with Better Confidence Handling

This module provides an improved financial term matching system with better confidence
handling, partial match suggestions, and enhanced user experience.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FinancialTerm:
    """Data class representing a financial term."""
    name: str
    definition: str
    category: str
    aliases: List[str] = None
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []


@dataclass
class MatchResult:
    """Data class representing a match result."""
    term: FinancialTerm
    confidence: float
    match_type: str  # 'exact', 'partial', 'alias'


class FinancialTermMatcher:
    """Enhanced Financial Term Matcher with better confidence handling."""
    
    def __init__(self):
        self.terms = self._initialize_terms()
        self.confidence_thresholds = {
            'no_match': 0.3,
            'multiple_suggestions': 0.3,  # Changed from 0.6 to 0.3
            'single_suggestion': 0.6,     # Range 0.6 - 0.8
            'direct_match': 0.8           # > 0.8
        }
    
    def _initialize_terms(self) -> List[FinancialTerm]:
        """Initialize the financial terms database."""
        return [
            FinancialTerm(
                name="Annual Income",
                definition="The total amount of money earned by an individual or entity in a year, including salary, wages, bonuses, and other sources of income.",
                category="Income",
                aliases=["yearly income", "annual earnings", "yearly earnings"]
            ),
            FinancialTerm(
                name="Annual Percentage Rate",
                definition="The yearly interest rate charged for borrowing or earned through an investment, expressed as a percentage.",
                category="Interest",
                aliases=["APR", "annual rate", "yearly rate"]
            ),
            FinancialTerm(
                name="Annual Report",
                definition="A comprehensive report on a company's activities throughout the preceding year, including financial statements and management discussion.",
                category="Reporting",
                aliases=["yearly report", "annual statement"]
            ),
            FinancialTerm(
                name="Cash Flow",
                definition="The net amount of cash and cash-equivalents being transferred into and out of a business.",
                category="Financial Metrics",
                aliases=["cash movement", "money flow"]
            ),
            FinancialTerm(
                name="Return on Investment",
                definition="A performance measure used to evaluate the efficiency of an investment or compare the efficiency of several investments.",
                category="Investment",
                aliases=["ROI", "investment return", "return on capital"]
            ),
            FinancialTerm(
                name="Gross Domestic Product",
                definition="The total monetary or market value of all finished goods and services produced within a country's borders in a specific time period.",
                category="Economics",
                aliases=["GDP", "gross product", "national product"]
            ),
            FinancialTerm(
                name="Net Present Value",
                definition="The difference between the present value of cash inflows and the present value of cash outflows over a period of time.",
                category="Investment",
                aliases=["NPV", "present value", "discounted value"]
            ),
            FinancialTerm(
                name="Interest Rate",
                definition="The proportion of a loan that is charged as interest to the borrower, typically expressed as an annual percentage of the loan outstanding.",
                category="Interest",
                aliases=["rate", "borrowing rate", "lending rate"]
            )
        ]
    
    def _calculate_confidence(self, query: str, term: FinancialTerm) -> Tuple[float, str]:
        """
        Calculate confidence score for a term match.
        
        Returns:
            Tuple of (confidence_score, match_type)
        """
        query_lower = query.lower().strip()
        term_name_lower = term.name.lower()
        
        # Exact match
        if query_lower == term_name_lower:
            return 0.95, 'exact'
        
        # Check aliases for exact match
        for alias in term.aliases:
            if query_lower == alias.lower():
                return 0.90, 'alias'
        
        # Partial match in term name
        if query_lower in term_name_lower:
            # Higher confidence for longer partial matches
            match_ratio = len(query_lower) / len(term_name_lower)
            if match_ratio > 0.7:
                return 0.85, 'partial'
            elif match_ratio > 0.4:
                return 0.55, 'partial'
            else:
                return 0.45, 'partial'  # Increased from 0.35 to ensure it's above threshold
        
        # Partial match in aliases
        for alias in term.aliases:
            if query_lower in alias.lower():
                match_ratio = len(query_lower) / len(alias)
                if match_ratio > 0.7:
                    return 0.75, 'alias'
                elif match_ratio > 0.4:
                    return 0.50, 'alias'
                else:
                    return 0.40, 'alias'  # Increased from 0.30 to ensure it's above threshold
        
        # Check if term name contains query words
        query_words = query_lower.split()
        term_words = term_name_lower.split()
        
        if query_words and term_words:
            matching_words = sum(1 for word in query_words if any(word in term_word for term_word in term_words))
            if matching_words > 0:
                confidence = (matching_words / len(query_words)) * 0.7  # Increased multiplier
                return max(confidence, 0.35), 'partial'  # Ensure minimum confidence for matches
        
        # Check if any term words start with the query
        for term_word in term_words:
            if term_word.startswith(query_lower):
                return 0.45, 'partial'
        
        return 0.0, 'none'
    
    def search_terms(self, query: str) -> List[MatchResult]:
        """
        Search for financial terms based on the query.
        
        Args:
            query: The search query string
            
        Returns:
            List of MatchResult objects sorted by confidence
        """
        if not query or not query.strip():
            return []
        
        results = []
        
        for term in self.terms:
            confidence, match_type = self._calculate_confidence(query, term)
            if confidence > 0:
                results.append(MatchResult(term, confidence, match_type))
        
        # Sort by confidence descending
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        return results
    
    def get_response(self, query: str) -> Dict:
        """
        Get a structured response for the query with appropriate confidence handling.
        
        Args:
            query: The search query string
            
        Returns:
            Dictionary containing response type, message, and relevant data
        """
        # Clean the query by removing common prefixes
        clean_query = re.sub(r'^(what\s+is\s+|define\s+|explain\s+)', '', query, flags=re.IGNORECASE).strip()
        
        results = self.search_terms(clean_query)
        
        if not results:
            return {
                'type': 'no_match',
                'message': "There are no related terms present",
                'terms': [],
                'confidence': 0.0
            }
        
        best_match = results[0]
        
        # Direct match (> 0.8)
        if best_match.confidence > self.confidence_thresholds['direct_match']:
            return {
                'type': 'direct_match',
                'message': f"Direct match found for '{clean_query}'",
                'terms': [best_match.term],
                'confidence': best_match.confidence,
                'match_type': best_match.match_type
            }
        
        # Single suggestion with confirmation (0.6 - 0.8)
        elif best_match.confidence >= self.confidence_thresholds['single_suggestion']:
            return {
                'type': 'single_suggestion',
                'message': f"Found a related term for '{clean_query}'. Did you mean:",
                'terms': [best_match.term],
                'confidence': best_match.confidence,
                'match_type': best_match.match_type
            }
        
        # Multiple suggestions (0.3 - 0.6)
        elif best_match.confidence >= self.confidence_thresholds['multiple_suggestions']:
            # Get top 3 matches
            top_matches = [r.term for r in results[:3]]
            return {
                'type': 'multiple_suggestions',
                'message': f"Found multiple related terms for '{clean_query}':",
                'terms': top_matches,
                'confidence': best_match.confidence,
                'match_type': best_match.match_type
            }
        
        # No match (< 0.3)
        else:
            return {
                'type': 'no_match',
                'message': "There are no related terms present",
                'terms': [],
                'confidence': best_match.confidence if results else 0.0
            }


def main():
    """Main function for testing the financial term matcher."""
    matcher = FinancialTermMatcher()
    
    print("Financial Term Matcher - Enhanced Version")
    print("=" * 45)
    print("Type 'quit' to exit")
    print()
    
    while True:
        query = input("Enter your query (e.g., 'what is annual'): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not query:
            print("Please enter a valid query.\n")
            continue
        
        # Remove common prefixes like "what is", "define", etc.
        # clean_query = re.sub(r'^(what\s+is\s+|define\s+|explain\s+)', '', query, flags=re.IGNORECASE).strip()
        
        response = matcher.get_response(query)
        
        print(f"\nQuery: '{query}'")
        print(f"Confidence: {response.get('confidence', 0):.2f}")
        print(f"Response Type: {response['type']}")
        print("-" * 40)
        
        if response['type'] == 'no_match':
            print(response['message'])
        
        elif response['type'] == 'direct_match':
            term = response['terms'][0]
            print(f"✓ {term.name}")
            print(f"Category: {term.category}")
            print(f"Definition: {term.definition}")
            if term.aliases:
                print(f"Also known as: {', '.join(term.aliases)}")
        
        elif response['type'] == 'single_suggestion':
            print(response['message'])
            term = response['terms'][0]
            print(f"  → {term.name}")
            print(f"    Category: {term.category}")
            print(f"    Definition: {term.definition}")
        
        elif response['type'] == 'multiple_suggestions':
            print(response['message'])
            for i, term in enumerate(response['terms'], 1):
                print(f"  {i}. {term.name}")
                print(f"     Category: {term.category}")
            print("\nWhich one did you mean? (You can search for the specific term)")
        
        print()


if __name__ == "__main__":
    main()