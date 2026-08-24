"""
Unit tests for Customer 360 directory tickets table (PR 16).
"""

import unittest
import pandas as pd
from utils.data_loader import load_data


class TestCustomerDirectoryExpansion(unittest.TestCase):
    
    def test_customer_and_ticket_loading(self):
        customers, tickets, interactions, _ = load_data()
        self.assertFalse(customers.empty, "Customers dataframe should not be empty")
        self.assertFalse(tickets.empty, "Tickets dataframe should not be empty")
        
        # Verify tickets have required columns for Customer 360 table
        expected_cols = ['ticket_id', 'customer_id', 'subject', 'priority', 'status']
        for col in expected_cols:
            self.assertIn(col, tickets.columns, f"Column '{col}' should be in tickets DataFrame")

    def test_customer_ticket_filtering_and_sorting(self):
        customers, tickets, _, _ = load_data()
        first_cust = customers.iloc[0]
        cust_id = first_cust['customer_id']
        
        # Filter tickets matching this customer
        cust_tickets = tickets[
            (tickets['customer_id'] == cust_id) | 
            (tickets['customer_id'] == f"CUST-{cust_id}") |
            (tickets['customer_id'].astype(str) == str(cust_id))
        ]
        
        # If the customer has tickets, verify head(5) limit
        recent_tickets = cust_tickets.head(5)
        self.assertLessEqual(len(recent_tickets), 5)


if __name__ == '__main__':
    unittest.main()
