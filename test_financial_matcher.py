#!/usr/bin/python3
"""
Test suite for the Enhanced Financial Term Matcher
"""

import unittest
from financial_term_matcher import FinancialTermMatcher, FinancialTerm, MatchResult


class TestFinancialTermMatcher(unittest.TestCase):
    """Test cases for the Financial Term Matcher."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.matcher = FinancialTermMatcher()
    
    def test_exact_match_high_confidence(self):
        """Test exact matches should have high confidence (>0.8)."""
        response = self.matcher.get_response("Annual Income")
        
        self.assertEqual(response['type'], 'direct_match')
        self.assertGreater(response['confidence'], 0.8)
        self.assertEqual(len(response['terms']), 1)
        self.assertEqual(response['terms'][0].name, "Annual Income")
    
    def test_alias_exact_match(self):
        """Test exact alias matches should have high confidence."""
        response = self.matcher.get_response("APR")
        
        self.assertEqual(response['type'], 'direct_match')
        self.assertGreater(response['confidence'], 0.8)
        self.assertEqual(response['terms'][0].name, "Annual Percentage Rate")
    
    def test_partial_match_multiple_suggestions(self):
        """Test partial matches should show multiple suggestions."""
        response = self.matcher.get_response("annual")
        
        # Should be either multiple_suggestions or single_suggestion
        self.assertIn(response['type'], ['multiple_suggestions', 'single_suggestion'])
        self.assertGreaterEqual(response['confidence'], 0.3)
        self.assertGreater(len(response['terms']), 0)
        
        # Check that "Annual Income" is in the suggestions
        term_names = [term.name for term in response['terms']]
        self.assertIn("Annual Income", term_names)
    
    def test_case_insensitive_matching(self):
        """Test that matching is case insensitive."""
        response_lower = self.matcher.get_response("annual income")
        response_upper = self.matcher.get_response("ANNUAL INCOME")
        response_mixed = self.matcher.get_response("Annual Income")
        
        # All should return the same result
        self.assertEqual(response_lower['type'], 'direct_match')
        self.assertEqual(response_upper['type'], 'direct_match')
        self.assertEqual(response_mixed['type'], 'direct_match')
        
        # All should have similar confidence
        self.assertAlmostEqual(response_lower['confidence'], response_upper['confidence'], places=2)
        self.assertAlmostEqual(response_lower['confidence'], response_mixed['confidence'], places=2)
    
    def test_no_match_low_confidence(self):
        """Test queries with no matches should return no_match."""
        response = self.matcher.get_response("xyz random nonexistent term")
        
        self.assertEqual(response['type'], 'no_match')
        self.assertLess(response['confidence'], 0.3)
        self.assertEqual(len(response['terms']), 0)
        self.assertEqual(response['message'], "There are no related terms present")
    
    def test_empty_query(self):
        """Test empty or whitespace queries."""
        response_empty = self.matcher.get_response("")
        response_whitespace = self.matcher.get_response("   ")
        
        self.assertEqual(response_empty['type'], 'no_match')
        self.assertEqual(response_whitespace['type'], 'no_match')
        self.assertEqual(len(response_empty['terms']), 0)
        self.assertEqual(len(response_whitespace['terms']), 0)
    
    def test_confidence_thresholds(self):
        """Test that confidence thresholds work correctly."""
        # Test different query types and their expected confidence ranges
        test_cases = [
            ("Annual Income", 'direct_match', 0.8, 1.0),  # Exact match
            ("APR", 'direct_match', 0.8, 1.0),  # Alias exact match
            ("annual", 'multiple_suggestions', 0.3, 0.8),  # Partial match
            ("xyz123", 'no_match', 0.0, 0.3),  # No match
        ]
        
        for query, expected_type, min_conf, max_conf in test_cases:
            with self.subTest(query=query):
                response = self.matcher.get_response(query)
                self.assertEqual(response['type'], expected_type, 
                               f"Query '{query}' expected {expected_type}, got {response['type']}")
                self.assertGreaterEqual(response['confidence'], min_conf,
                                      f"Query '{query}' confidence too low: {response['confidence']}")
                self.assertLessEqual(response['confidence'], max_conf,
                                   f"Query '{query}' confidence too high: {response['confidence']}")
    
    def test_query_preprocessing(self):
        """Test that common query prefixes are handled correctly."""
        # These should all match "Annual Income"
        queries = [
            "Annual Income",
            "what is Annual Income",
            "define Annual Income",
            "explain Annual Income"
        ]
        
        for query in queries:
            with self.subTest(query=query):
                response = self.matcher.get_response(query)
                self.assertEqual(response['type'], 'direct_match')
                self.assertEqual(response['terms'][0].name, "Annual Income")
    
    def test_search_terms_functionality(self):
        """Test the search_terms method directly."""
        results = self.matcher.search_terms("Annual Income")
        
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], MatchResult)
        self.assertEqual(results[0].term.name, "Annual Income")
        self.assertGreater(results[0].confidence, 0.8)
        
        # Results should be sorted by confidence (descending)
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(results[i].confidence, results[i + 1].confidence)
    
    def test_financial_term_structure(self):
        """Test that financial terms have the expected structure."""
        for term in self.matcher.terms:
            self.assertIsInstance(term, FinancialTerm)
            self.assertIsInstance(term.name, str)
            self.assertIsInstance(term.definition, str)
            self.assertIsInstance(term.category, str)
            self.assertIsInstance(term.aliases, list)
            
            # All should have non-empty name and definition
            self.assertTrue(term.name.strip())
            self.assertTrue(term.definition.strip())
            self.assertTrue(term.category.strip())
    
    def test_abbreviation_matching(self):
        """Test that abbreviations work correctly."""
        test_cases = [
            ("ROI", "Return on Investment"),
            ("GDP", "Gross Domestic Product"),
            ("NPV", "Net Present Value"),
            ("APR", "Annual Percentage Rate")
        ]
        
        for abbrev, full_name in test_cases:
            with self.subTest(abbrev=abbrev):
                response = self.matcher.get_response(abbrev)
                self.assertEqual(response['type'], 'direct_match')
                self.assertEqual(response['terms'][0].name, full_name)
    
    def test_partial_word_matching(self):
        """Test partial word matching scenarios."""
        # "cash" should match "Cash Flow"
        response = self.matcher.get_response("cash")
        self.assertGreaterEqual(response['confidence'], 0.3)
        
        if response['confidence'] >= 0.3:
            term_names = [term.name for term in response['terms']]
            self.assertIn("Cash Flow", term_names)
    
    def test_multiple_word_queries(self):
        """Test queries with multiple words."""
        response = self.matcher.get_response("return investment")
        
        # Should find "Return on Investment"
        self.assertGreaterEqual(response['confidence'], 0.3)
        if response['confidence'] >= 0.3:
            term_names = [term.name for term in response['terms']]
            self.assertIn("Return on Investment", term_names)


class TestMatchResultAndFinancialTerm(unittest.TestCase):
    """Test the data classes used by the matcher."""
    
    def test_financial_term_creation(self):
        """Test FinancialTerm creation and defaults."""
        term = FinancialTerm(
            name="Test Term",
            definition="Test definition",
            category="Test Category"
        )
        
        self.assertEqual(term.name, "Test Term")
        self.assertEqual(term.definition, "Test definition")
        self.assertEqual(term.category, "Test Category")
        self.assertEqual(term.aliases, [])  # Should default to empty list
    
    def test_financial_term_with_aliases(self):
        """Test FinancialTerm with aliases."""
        aliases = ["alias1", "alias2"]
        term = FinancialTerm(
            name="Test Term",
            definition="Test definition",
            category="Test Category",
            aliases=aliases
        )
        
        self.assertEqual(term.aliases, aliases)
    
    def test_match_result_creation(self):
        """Test MatchResult creation."""
        term = FinancialTerm("Test", "Definition", "Category")
        result = MatchResult(term, 0.85, "exact")
        
        self.assertEqual(result.term, term)
        self.assertEqual(result.confidence, 0.85)
        self.assertEqual(result.match_type, "exact")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)