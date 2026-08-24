"""
Schema validation utilities for ChurnGuard AI data uploads.
Validates CSV and JSON files against strict database and business schemas before loading into SQLite.
"""

from typing import Dict, List, Any, Tuple, Union
import pandas as pd
import numpy as np


class SchemaValidator:
    """Validator class for verifying uploaded datasets against expected schemas."""

    REQUIRED_CUSTOMER_COLUMNS = ['company_name', 'arr', 'renewal_date']
    RECOMMENDED_CUSTOMER_COLUMNS = ['customer_id', 'industry', 'contract_type', 'csm_name']
    
    REQUIRED_TICKET_FIELDS = ['ticket_id', 'subject', 'priority', 'status']
    RECOMMENDED_TICKET_FIELDS = ['customer_id', 'sentiment', 'created_date']
    
    REQUIRED_INTERACTION_COLUMNS = ['customer_id', 'interaction_type', 'timestamp']
    RECOMMENDED_INTERACTION_COLUMNS = ['interaction_id', 'description']

    VALID_PRIORITIES = {'Low', 'Medium', 'High', 'Critical'}
    VALID_STATUSES = {'Open', 'In Progress', 'Awaiting Response', 'Resolved', 'Closed'}
    VALID_SENTIMENTS = {'Positive', 'Neutral', 'Negative'}
    VALID_INTERACTION_TYPES = {
        'Login', 'Feature Usage', 'Support Call', 'QBR', 'Email Sent', 
        'Email', 'Call', 'Meeting', 'Training', 'Executive Review'
    }

    @classmethod
    def validate_customers(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates customer DataFrame against required schema and data types.
        
        Returns:
            Dict with:
                - is_valid (bool): True if all required checks pass
                - errors (List[str]): List of blocking issues
                - warnings (List[str]): List of non-blocking issues
                - missing_required (List[str]): Missing required columns
                - missing_recommended (List[str]): Missing recommended columns
                - row_count (int): Total rows
                - valid_row_count (int): Rows passing data type checks
        """
        errors = []
        warnings = []
        
        if not isinstance(df, pd.DataFrame):
            return {
                'is_valid': False,
                'errors': ['Uploaded data is not a valid tabular DataFrame.'],
                'warnings': [],
                'missing_required': cls.REQUIRED_CUSTOMER_COLUMNS,
                'missing_recommended': cls.RECOMMENDED_CUSTOMER_COLUMNS,
                'row_count': 0,
                'valid_row_count': 0
            }
            
        if df.empty:
            return {
                'is_valid': False,
                'errors': ['The uploaded customer file is empty (0 rows).'],
                'warnings': [],
                'missing_required': [],
                'missing_recommended': [],
                'row_count': 0,
                'valid_row_count': 0
            }

        cols = set(df.columns)
        missing_required = [col for col in cls.REQUIRED_CUSTOMER_COLUMNS if col not in cols]
        missing_recommended = [col for col in cls.RECOMMENDED_CUSTOMER_COLUMNS if col not in cols]

        if missing_required:
            errors.append(f"Missing required column(s): {', '.join(missing_required)}")

        if missing_recommended:
            warnings.append(f"Missing recommended column(s): {', '.join(missing_recommended)} (default values will be assigned)")

        # Data type and value validations if required columns exist
        valid_rows = len(df)
        if 'company_name' in df.columns:
            null_names = df['company_name'].isna().sum()
            if null_names > 0:
                errors.append(f"Found {null_names} customer record(s) with blank/null company_name.")

        if 'arr' in df.columns:
            # Check numeric conversion
            non_numeric_arr = pd.to_numeric(df['arr'], errors='coerce')
            invalid_arr_count = non_numeric_arr.isna().sum()
            if invalid_arr_count > 0:
                errors.append(f"Column 'arr' contains {invalid_arr_count} non-numeric or invalid value(s).")
            else:
                negative_arr = (non_numeric_arr < 0).sum()
                if negative_arr > 0:
                    warnings.append(f"Found {negative_arr} customer(s) with negative ARR.")

        if 'renewal_date' in df.columns:
            parsed_dates = pd.to_datetime(df['renewal_date'], errors='coerce')
            invalid_dates = parsed_dates.isna().sum()
            if invalid_dates > 0:
                warnings.append(f"Found {invalid_dates} unparseable renewal_date value(s) (format should be YYYY-MM-DD).")

        if 'sentiment' in df.columns:
            invalid_sentiments = ~df['sentiment'].fillna('Neutral').isin(cls.VALID_SENTIMENTS)
            invalid_sent_count = invalid_sentiments.sum()
            if invalid_sent_count > 0:
                warnings.append(f"Found {invalid_sent_count} row(s) with non-standard sentiment values. Expected: Positive, Neutral, Negative.")

        is_valid = len(errors) == 0
        return {
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'missing_required': missing_required,
            'missing_recommended': missing_recommended,
            'row_count': len(df),
            'valid_row_count': valid_rows if is_valid else 0
        }

    @classmethod
    def validate_tickets(cls, data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Dict[str, Any]:
        """
        Validates support ticket data (JSON list of dicts or DataFrame) against schema.
        """
        errors = []
        warnings = []
        
        if isinstance(data, list):
            if not data:
                return {
                    'is_valid': False,
                    'errors': ['The uploaded tickets JSON file is empty.'],
                    'warnings': [],
                    'missing_required': cls.REQUIRED_TICKET_FIELDS,
                    'missing_recommended': cls.RECOMMENDED_TICKET_FIELDS,
                    'row_count': 0,
                    'valid_row_count': 0
                }
            df = pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            df = data
            if df.empty:
                return {
                    'is_valid': False,
                    'errors': ['The uploaded tickets file is empty.'],
                    'warnings': [],
                    'missing_required': cls.REQUIRED_TICKET_FIELDS,
                    'missing_recommended': cls.RECOMMENDED_TICKET_FIELDS,
                    'row_count': 0,
                    'valid_row_count': 0
                }
        else:
            return {
                'is_valid': False,
                'errors': ['Invalid format: Tickets must be a JSON array of objects or CSV table.'],
                'warnings': [],
                'missing_required': cls.REQUIRED_TICKET_FIELDS,
                'missing_recommended': cls.RECOMMENDED_TICKET_FIELDS,
                'row_count': 0,
                'valid_row_count': 0
            }

        cols = set(df.columns)
        missing_required = [col for col in cls.REQUIRED_TICKET_FIELDS if col not in cols]
        missing_recommended = [col for col in cls.RECOMMENDED_TICKET_FIELDS if col not in cols]

        if missing_required:
            errors.append(f"Missing required field(s): {', '.join(missing_required)}")

        if missing_recommended:
            warnings.append(f"Missing recommended field(s): {', '.join(missing_recommended)}")

        if 'priority' in df.columns:
            invalid_priorities = ~df['priority'].isin(cls.VALID_PRIORITIES)
            invalid_count = invalid_priorities.sum()
            if invalid_count > 0:
                warnings.append(f"Found {invalid_count} ticket(s) with non-standard priority values. Expected: {', '.join(cls.VALID_PRIORITIES)}.")

        if 'status' in df.columns:
            invalid_statuses = ~df['status'].isin(cls.VALID_STATUSES)
            invalid_count = invalid_statuses.sum()
            if invalid_count > 0:
                warnings.append(f"Found {invalid_count} ticket(s) with non-standard status values. Expected: {', '.join(cls.VALID_STATUSES)}.")

        is_valid = len(errors) == 0
        return {
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'missing_required': missing_required,
            'missing_recommended': missing_recommended,
            'row_count': len(df),
            'valid_row_count': len(df) if is_valid else 0
        }

    @classmethod
    def validate_interactions(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates interactions DataFrame against schema and data types.
        """
        errors = []
        warnings = []
        
        if not isinstance(df, pd.DataFrame):
            return {
                'is_valid': False,
                'errors': ['Uploaded interactions data is not a valid DataFrame.'],
                'warnings': [],
                'missing_required': cls.REQUIRED_INTERACTION_COLUMNS,
                'missing_recommended': cls.RECOMMENDED_INTERACTION_COLUMNS,
                'row_count': 0,
                'valid_row_count': 0
            }
            
        if df.empty:
            return {
                'is_valid': False,
                'errors': ['The uploaded interactions file is empty (0 rows).'],
                'warnings': [],
                'missing_required': [],
                'missing_recommended': [],
                'row_count': 0,
                'valid_row_count': 0
            }

        cols = set(df.columns)
        missing_required = [col for col in cls.REQUIRED_INTERACTION_COLUMNS if col not in cols]
        missing_recommended = [col for col in cls.RECOMMENDED_INTERACTION_COLUMNS if col not in cols]

        if missing_required:
            errors.append(f"Missing required column(s): {', '.join(missing_required)}")

        if missing_recommended:
            warnings.append(f"Missing recommended column(s): {', '.join(missing_recommended)}")

        if 'timestamp' in df.columns:
            parsed_timestamps = pd.to_datetime(df['timestamp'], errors='coerce')
            invalid_timestamps = parsed_timestamps.isna().sum()
            if invalid_timestamps > 0:
                warnings.append(f"Found {invalid_timestamps} unparseable timestamp value(s).")

        is_valid = len(errors) == 0
        return {
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'missing_required': missing_required,
            'missing_recommended': missing_recommended,
            'row_count': len(df),
            'valid_row_count': len(df) if is_valid else 0
        }


def validate_customers_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Helper wrapper for customer schema validation."""
    return SchemaValidator.validate_customers(df)


def validate_tickets_schema(data: Union[List[Dict[str, Any]], pd.DataFrame]) -> Dict[str, Any]:
    """Helper wrapper for ticket schema validation."""
    return SchemaValidator.validate_tickets(data)


def validate_interactions_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Helper wrapper for interaction schema validation."""
    return SchemaValidator.validate_interactions(df)
