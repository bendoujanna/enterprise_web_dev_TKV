# comparing different search methods for finding transactions
# need this for the DSA part of the assignment

import time
import json


def linear_search(transactions, transaction_id):
    # this is the slow way - just loop through everything
    for trans in transactions:
        if trans['id'] == transaction_id:
            return trans
    return None


def make_dict_from_transactions(transactions):
    # convert list to dictionary for faster lookups
    result = {}
    for trans in transactions:
        result[trans['id']] = trans
    return result


def dict_lookup(trans_dict, transaction_id):
    # this should be faster - direct dictionary access
    return trans_dict.get(transaction_id)


def compare_performance(transactions, test_ids):
    # comparing linear search vs dictionary lookup
    print(f"Testing with {len(test_ids)} searches...")
    
    results = {}