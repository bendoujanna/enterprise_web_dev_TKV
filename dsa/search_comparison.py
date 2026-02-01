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
     
    # test linear search first
    linear_times = []
    print("Running linear search tests...")
    for test_id in test_ids:
        start = time.perf_counter()
        result = linear_search(transactions, test_id)
        end = time.perf_counter()
        linear_times.append(end - start)
    
    avg_linear = sum(linear_times) / len(linear_times)
    print(f"Linear search avg time: {avg_linear}")
    
    # now test dictionary lookup
    print("Creating dictionary...")
    dict_start = time.perf_counter()
    trans_dict = make_dict_from_transactions(transactions)
    dict_creation = time.perf_counter() - dict_start
    print(f"Dictionary creation took: {dict_creation}")
    
    dict_times = []
    print("Running dictionary lookup tests...")
    for test_id in test_ids:
        start = time.perf_counter()
        result = dict_lookup(trans_dict, test_id)
        end = time.perf_counter()
        dict_times.append(end - start)
    