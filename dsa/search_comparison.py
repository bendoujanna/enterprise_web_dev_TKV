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
    
    avg_dict = sum(dict_times) / len(dict_times)
    print(f"Dict lookup avg time: {avg_dict}")
    
    # calculate how much faster
    speedup = avg_linear / avg_dict
    
    results = {
        'linear_search': {
            'avg_time': avg_linear,
            'total_time': sum(linear_times),
            'min_time': min(linear_times),
            'max_time': max(linear_times)
        },
        'dictionary_lookup': {
            'avg_time': avg_dict,
            'total_time': sum(dict_times),
            'min_time': min(dict_times),
            'max_time': max(dict_times),
            'dict_creation_time': dict_creation
        },
        'speedup': speedup,
        'test_count': len(test_ids)
    }
    
    return results


def run_comparison():
    # main function to run everything
    print("Loading transactions from JSON file...")
    try:
        with open('../data/transactions.json', 'r') as f:
            transactions = json.load(f)
    except FileNotFoundError:
        print("ERROR: transactions.json not found!")
        print("You need to run xml_parser.py first")
        return
    
    print(f"Loaded {len(transactions)} transactions")
    print("")
    
    # create test IDs (need at least 20 for the assignment)
    test_ids = []
    for i in range(1, 21):  # testing IDs 1-20
        test_ids.append(str(i))
    
    print("="*60)
    print("PERFORMANCE COMPARISON: LINEAR SEARCH vs DICTIONARY LOOKUP")
    print("="*60)
    print("")
    
    # run the comparison
    results = compare_performance(transactions, test_ids)
    
    print("")
    print("="*60)
    print("RESULTS")
    print("="*60)
    print("")
    print("1. LINEAR SEARCH (O(n) - checks each item)")
    print(f"   Average time: {results['linear_search']['avg_time']:.9f} seconds")
    print(f"   Total time:   {results['linear_search']['total_time']:.9f} seconds")
    print(f"   Fastest:      {results['linear_search']['min_time']:.9f} seconds")
    print(f"   Slowest:      {results['linear_search']['max_time']:.9f} seconds")
    print("")
    
    print("2. DICTIONARY LOOKUP (O(1) - direct access)")
    print(f"   Dict creation: {results['dictionary_lookup']['dict_creation_time']:.9f} seconds")
    print(f"   Average time:  {results['dictionary_lookup']['avg_time']:.9f} seconds")
    print(f"   Total time:    {results['dictionary_lookup']['total_time']:.9f} seconds")
    print(f"   Fastest:       {results['dictionary_lookup']['min_time']:.9f} seconds")
    print(f"   Slowest:       {results['dictionary_lookup']['max_time']:.9f} seconds")
    print("")
    
    print(f"SPEEDUP: Dictionary is {results['speedup']:.2f}x faster!")
    print("")
    
    print("="*60)
    print("WHY IS DICTIONARY FASTER?")
    print("="*60)
    print("""
Linear search has to check each transaction one by one until it finds
the right ID. With 20 transactions, it might need to check all 20.

Dictionary lookup uses a hash table which can jump directly to the 
right transaction using the ID as a key. It doesn't matter if there
are 20 or 20,000 transactions - it's always fast.

Time Complexity:
- Linear Search: O(n) - gets slower as data grows
- Dictionary: O(1) - stays the same speed no matter what

For bigger datasets this difference becomes huge. With 1000 transactions,
linear search would be ~50x slower while dictionary stays the same.

Other efficient data structures:
- Binary Search Tree: O(log n) if data is sorted
- Hash tables (what Python dicts use): O(1) average case
- Tries: Good for string prefix matching
    """)
    
    # save results to file
    print("Saving results to file...")
    with open('../dsa/performance_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to dsa/performance_results.json")


if __name__ == "__main__":
    run_comparison()