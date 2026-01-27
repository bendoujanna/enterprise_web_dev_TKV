# XML parser for mobile money SMS data
# This parses MTN Mobile Money SMS backup format

import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

def extract_transaction_info(body_text, date_str):
    # parse the SMS body to extract transaction details
    trans = {
        'id': None,
        'type': '',
        'amount': 0.0,
        'sender': '',
        'receiver': '',
        'timestamp': date_str,
        'status': 'completed'
    }
    
    # try to extract transaction ID
    txid_match = re.search(r'TxId[:\s]+(\d+)', body_text)
    if txid_match:
        trans['id'] = txid_match.group(1)
    
    # extract amount (look for patterns like "5000 RWF" or "5,000 RWF")
    amount_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*RWF', body_text)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        trans['amount'] = float(amount_str)
    
    # figure out transaction type from the message
    body_lower = body_text.lower()
    
    if 'received' in body_lower or 'from' in body_lower and 'to' not in body_lower:
        trans['type'] = 'RECEIVE'
        # extract sender name
        sender_match = re.search(r'from ([A-Za-z\s]+)', body_text, re.IGNORECASE)
        if sender_match:
            trans['sender'] = sender_match.group(1).strip()
        trans['receiver'] = 'You'
        
    elif 'payment' in body_lower and 'to' in body_lower:
        trans['type'] = 'SEND'
        trans['sender'] = 'You'
        # extract receiver name
        receiver_match = re.search(r'to ([A-Za-z\s]+\d+)', body_text, re.IGNORECASE)
        if receiver_match:
            trans['receiver'] = receiver_match.group(1).strip()
            
    elif 'transferred to' in body_lower:
        trans['type'] = 'SEND'
        trans['sender'] = 'You'
        # extract receiver name and number
        receiver_match = re.search(r'to ([A-Za-z\s]+)\s*\((\d+)\)', body_text, re.IGNORECASE)
        if receiver_match:
            trans['receiver'] = f"{receiver_match.group(1).strip()} ({receiver_match.group(2)})"
            
    elif 'deposit' in body_lower or 'cash deposit' in body_lower:
        trans['type'] = 'DEPOSIT'
        trans['sender'] = 'Bank/Agent'
        trans['receiver'] = 'You'
        
    elif 'airtime' in body_lower:
        trans['type'] = 'AIRTIME'
        trans['sender'] = 'You'
        trans['receiver'] = 'Airtime'
        
    elif 'withdrawal' in body_lower or 'withdraw' in body_lower:
        trans['type'] = 'WITHDRAW'
        trans['sender'] = 'You'
        trans['receiver'] = 'Agent'
        
    else:
        trans['type'] = 'OTHER'
        trans['sender'] = 'Unknown'
        trans['receiver'] = 'Unknown'
    
    return trans


def parse_xml_to_json(xml_file):
    # parse the MTN mobile money XML backup file
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        transactions = []
        counter = 1  # for generating IDs
        
        print("Parsing MTN Mobile Money SMS records...")
        
        # loop through all sms elements
        for sms in root.findall('sms'):
            # get the SMS body text
            body = sms.get('body', '')
            date_ms = sms.get('date', '0')
            readable_date = sms.get('readable_date', '')
            
            # skip empty bodies
            if not body or len(body) < 10:
                continue
            
            # convert timestamp
            try:
                timestamp_sec = int(date_ms) / 1000
                date_str = datetime.fromtimestamp(timestamp_sec).isoformat()
            except:
                date_str = readable_date
            
            # extract transaction info from the SMS body
            trans = extract_transaction_info(body, date_str)
            
            # assign ID if not found in body
            if not trans['id']:
                trans['id'] = str(counter)
            
            transactions.append(trans)
            counter += 1
        
        print(f"DEBUG: Parsed {len(transactions)} total transactions")
        return transactions
    
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except FileNotFoundError:
        print(f"File not found: {xml_file}")
        return []
    except Exception as e:
        print(f"Something went wrong: {e}")
        import traceback
        traceback.print_exc()
        return []


def save_to_json(trans_list, output_file):
    # save the transactions to a json file
    try:
        with open(output_file, 'w') as f:
            json.dump(trans_list, f, indent=2)
        print(f"Saved {len(trans_list)} transactions to {output_file}")
    except Exception as e:
        print(f"Error saving: {e}")


if __name__ == "__main__":
    # main execution starts here
    xml_file = "../dsa/modified_sms_v2.xml"
    output_file = "../api/transactions.json"
    
    print("Starting XML parsing...")
    transactions = parse_xml_to_json(xml_file)
    
    if len(transactions) > 0:
        save_to_json(transactions, output_file)
        # show first few transactions to verify
        print(f"\nFirst 5 transactions:")
        print(json.dumps(transactions[:5], indent=2))
        print(f"\nTransaction types found:")
        types = {}
        for t in transactions:
            ttype = t['type']
            types[ttype] = types.get(ttype, 0) + 1
        for ttype, count in types.items():
            print(f"  {ttype}: {count}")
    else:
        print("No transactions found or something went wrong")