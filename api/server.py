# REST API for mobile money SMS transactions
# Using plain Python http.server as required

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
from urllib.parse import urlparse
import os

# global storage for transactions
all_transactions = []
trans_dict = {}  # for faster lookups

# login credentials for basic auth
USERS = {
    'admin': 'password123',
    'user': 'userpass'
}


class TransactionAPI(BaseHTTPRequestHandler):
    
    def _set_headers(self, status=200):
        # set response headers
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def check_auth(self):
        # check if user has valid credentials
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            print("No auth header found")
            return False
        
        try:
            # parse the auth header
            parts = auth_header.split(' ')
            if len(parts) != 2 or parts[0] != 'Basic':
                return False
            
            # decode the base64 credentials
            decoded = base64.b64decode(parts[1]).decode('utf-8')
            username, password = decoded.split(':')
            
            # check if credentials are valid
            if username in USERS and USERS[username] == password:
                print(f"Auth successful for user: {username}")
                return True
            else:
                print("Invalid credentials")
                return False
            
        except Exception as e:
            print(f"Auth error: {e}")
            return False
    
    def send_error_response(self, status, error_msg):
        # send error response as JSON
        self._set_headers(status)
        response = {
            'success': False,
            'error': error_msg
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_json_response(self, data, status=200):
        # send success response
        self._set_headers(status)
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def get_request_body(self):
        # read and parse JSON body
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        return json.loads(body.decode('utf-8'))
    
    def do_OPTIONS(self):
        # handle preflight requests
        self._set_headers(204)
    
    def do_GET(self):
        # handle GET requests
        global all_transactions, trans_dict
        
        # check authentication first
        if not self.check_auth():
            self.send_error_response(401, 'Unauthorized - Invalid or missing credentials')
            return
        
        path = urlparse(self.path).path
        print(f"GET request for: {path}")
        
        # list all transactions
        if path == '/transactions':
            response = {
                'success': True,
                'count': len(all_transactions),
                'data': all_transactions
            }
            self.send_json_response(response)
            return
        
        # get specific transaction by id
        if path.startswith('/transactions/'):
            trans_id = path.split('/')[-1]
            print(f"Looking for transaction: {trans_id}")
            
            # use dictionary for fast lookup
            transaction = trans_dict.get(trans_id)
            
            if transaction:
                response = {
                    'success': True,
                    'data': transaction
                }
                self.send_json_response(response)
            else:
                self.send_error_response(404, f'Transaction {trans_id} not found')
            return
        
        # unknown endpoint
        self.send_error_response(404, 'Endpoint not found')
    
    def do_POST(self):
        # handle POST requests (create new transaction)
        global all_transactions, trans_dict
        
        if not self.check_auth():
            self.send_error_response(401, 'Unauthorized')
            return
        
        path = urlparse(self.path).path
        
        if path == '/transactions':
            try:
                # get new transaction data from request
                new_trans = self.get_request_body()
                
                # validate required fields
                required = ['type', 'amount', 'sender', 'receiver']
                missing = []
                for field in required:
                    if field not in new_trans:
                        missing.append(field)
                
                if len(missing) > 0:
                    self.send_error_response(400, f'Missing fields: {", ".join(missing)}')
                    return
                
                # generate new ID
                if len(all_transactions) > 0:
                    max_id = max([int(t['id']) for t in all_transactions])
                    new_id = str(max_id + 1)
                else:
                    new_id = '1'
                
                new_trans['id'] = new_id
                
                # add timestamp if not provided
                if 'timestamp' not in new_trans:
                    from datetime import datetime
                    new_trans['timestamp'] = datetime.now().isoformat()
                
                # add status if not provided
                if 'status' not in new_trans:
                    new_trans['status'] = 'pending'
                
                # add to storage
                all_transactions.append(new_trans)
                trans_dict[new_id] = new_trans
                
                print(f"Created new transaction with ID: {new_id}")
                
                response = {
                    'success': True,
                    'message': 'Transaction created',
                    'data': new_trans
                }
                self.send_json_response(response, 201)
                
            except json.JSONDecodeError:
                self.send_error_response(400, 'Invalid JSON')
            except Exception as e:
                print(f"Error creating transaction: {e}")
                self.send_error_response(500, str(e))
            return
        
        self.send_error_response(404, 'Endpoint not found')
    
    def do_PUT(self):
        # handle PUT requests (update existing transaction)
        global all_transactions, trans_dict
        
        if not self.check_auth():
            self.send_error_response(401, 'Unauthorized')
            return
        
        path = urlparse(self.path).path
        
        if path.startswith('/transactions/'):
            trans_id = path.split('/')[-1]
            
            try:
                update_data = self.get_request_body()
                
                # find the transaction
                transaction = trans_dict.get(trans_id)
                
                if not transaction:
                    self.send_error_response(404, f'Transaction {trans_id} not found')
                    return
                
                # update fields (don't allow ID changes)
                for key in update_data:
                    if key != 'id':
                        transaction[key] = update_data[key]
                
                print(f"Updated transaction {trans_id}")
                
                response = {
                    'success': True,
                    'message': 'Transaction updated',
                    'data': transaction
                }
                self.send_json_response(response)
                
            except json.JSONDecodeError:
                self.send_error_response(400, 'Invalid JSON')
            except Exception as e:
                print(f"Error updating: {e}")
                self.send_error_response(500, str(e))
            return
        
        self.send_error_response(404, 'Endpoint not found')
    
    def do_DELETE(self):
        # handle DELETE requests
        global all_transactions, trans_dict
        
        if not self.check_auth():
            self.send_error_response(401, 'Unauthorized')
            return
        
        path = urlparse(self.path).path
        
        if path.startswith('/transactions/'):
            trans_id = path.split('/')[-1]
            
            # check if transaction exists
            transaction = trans_dict.get(trans_id)
            
            if not transaction:
                self.send_error_response(404, f'Transaction {trans_id} not found')
                return
            
            # remove from both storage locations
            all_transactions = [t for t in all_transactions if t['id'] != trans_id]
            del trans_dict[trans_id]
            
            print(f"Deleted transaction {trans_id}")
            
            response = {
                'success': True,
                'message': f'Transaction {trans_id} deleted',
                'deleted': transaction
            }
            self.send_json_response(response)
            return
        
        self.send_error_response(404, 'Endpoint not found')


def load_data():
    # load transactions from JSON file
    global all_transactions, trans_dict
    
    try:
        with open('../data/transactions.json', 'r') as f:
            all_transactions = json.load(f)
            
        # create dictionary for fast lookups
        trans_dict = {}
        for trans in all_transactions:
            trans_dict[trans['id']] = trans
            
        print(f"Loaded {len(all_transactions)} transactions from file")
    except FileNotFoundError:
        print("WARNING: transactions.json not found")
        print("Run xml_parser.py first to generate the data")
        all_transactions = []
        trans_dict = {}


def start_server(port=8000):
    # start the API server
    load_data()
    
    server_addr = ('', port)
    httpd = HTTPServer(server_addr, TransactionAPI)
    
    print("\n" + "="*60)
    print("Mobile Money SMS Transaction API Server")
    print("="*60)
    print(f"\nServer running on http://localhost:{port}")
    print(f"Loaded {len(all_transactions)} transactions")
    print("\nAvailable endpoints:")
    print("  GET    /transactions       - List all")
    print("  GET    /transactions/{{id}}  - Get one")
    print("  POST   /transactions       - Create new")
    print("  PUT    /transactions/{{id}}  - Update")
    print("  DELETE /transactions/{{id}}  - Delete")
    print("\nTest credentials:")
    print("  admin:password123")
    print("  user:userpass")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")


if __name__ == "__main__":
    start_server()
