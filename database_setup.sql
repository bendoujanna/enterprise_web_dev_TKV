-- ==================================================================
-- MoMo SMS Transaction Database 
-- ==================================================================

DROP DATABASE IF EXISTS momo_sms_db;
CREATE DATABASE momo_sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE momo_sms_db;

-- ==================================================================
-- TABLE 1: Users/Customers (matches ERD exactly)
-- ==================================================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    name VARCHAR(255) NOT NULL COMMENT 'Full name of account holder',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Mobile phone number',
    account_code VARCHAR(50) NOT NULL UNIQUE COMMENT 'MoMo account identifier',
    user_type ENUM('PERSON', 'MERCHANT', 'BANK', 'AGENT', 'SYSTEM') NOT NULL DEFAULT 'PERSON' COMMENT 'Account type',
    account_balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00 COMMENT 'Current account balance',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation date',
    CONSTRAINT chk_phone_format CHECK (phone_number LIKE '+%'),
    CONSTRAINT chk_balance_non_negative CHECK (account_balance >= 0)
) COMMENT='MoMo user accounts';

CREATE INDEX idx_phone_number ON users(phone_number);
CREATE INDEX idx_account_code ON users(account_code);
CREATE INDEX idx_user_type ON users(user_type);

-- ==================================================================
-- TABLE 2: Transaction_Categories (matches ERD exactly)
-- ==================================================================
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Category identifier',
    name VARCHAR(50) NOT NULL COMMENT 'Category display name',
    code VARCHAR(10) NOT NULL UNIQUE COMMENT 'Short category code',
    description VARCHAR(200) COMMENT 'Category description',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation date'
) COMMENT='Transaction type categories';

CREATE INDEX idx_category_code ON transaction_categories(code);

-- ==================================================================
-- TABLE 3: Transactions (matches ERD exactly)
-- ==================================================================
CREATE TABLE transactions (
    transaction_id VARCHAR(50) PRIMARY KEY COMMENT 'Unique transaction ID',
    category_id INT NOT NULL COMMENT 'Transaction type',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(3) NOT NULL DEFAULT 'RWF' COMMENT 'Currency code',
    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Transaction timestamp',
    fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT 'Transaction fee',
    balance_after DECIMAL(15, 2) COMMENT 'Balance after transaction',
    status ENUM('PENDING', 'COMPLETED', 'FAILED', 'REVERSED') NOT NULL DEFAULT 'PENDING' COMMENT 'Transaction status',
    reference_code VARCHAR(100) UNIQUE COMMENT 'External reference',
    description TEXT COMMENT 'Transaction notes',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',
    
    CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) 
        REFERENCES transaction_categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_fee_non_negative CHECK (fee >= 0)
) COMMENT='Main transaction records';

CREATE INDEX idx_category_id ON transactions(category_id);
CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_status ON transactions(status);
CREATE INDEX idx_currency ON transactions(currency);

-- ==================================================================
-- TABLE 4: Transaction_Parties (matches ERD - includes AGENT role)
-- ==================================================================
CREATE TABLE transaction_parties (
    party_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Party record ID',
    transaction_id VARCHAR(50) NOT NULL COMMENT 'Transaction reference',
    user_id INT NOT NULL COMMENT 'User reference',
    role ENUM('SENDER', 'RECEIVER', 'AGENT') NOT NULL COMMENT 'User role in transaction',
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Participation timestamp',
    
    CONSTRAINT fk_party_transaction FOREIGN KEY (transaction_id) 
        REFERENCES transactions(transaction_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_party_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uq_transaction_user_role UNIQUE (transaction_id, user_id, role)
) COMMENT='User-Transaction relationships (M:N)';

CREATE INDEX idx_party_transaction ON transaction_parties(transaction_id);
CREATE INDEX idx_party_user ON transaction_parties(user_id);
CREATE INDEX idx_party_role ON transaction_parties(role);

-- ==================================================================
-- TABLE 5: System_Logs (matches ERD exactly)
-- ==================================================================
CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Log entry ID',
    user_id INT NULL COMMENT 'User who triggered action',
    transaction_id VARCHAR(50) NULL COMMENT 'Related transaction',
    log_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Log timestamp',
    log_level VARCHAR(10) NOT NULL COMMENT 'Severity level',
    action VARCHAR(50) NOT NULL COMMENT 'Action performed',
    message TEXT NOT NULL COMMENT 'Detailed log message',
    
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) 
        REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) 
        REFERENCES transactions(transaction_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_log_level CHECK (log_level IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL'))
) COMMENT='System audit logs';

CREATE INDEX idx_log_date ON system_logs(log_date);
CREATE INDEX idx_log_level ON system_logs(log_level);
CREATE INDEX idx_log_user ON system_logs(user_id);
CREATE INDEX idx_log_transaction ON system_logs(transaction_id);

-- ==================================================================
-- SAMPLE DATA (5+ records per table)
-- ==================================================================

INSERT INTO transaction_categories (name, code, description) VALUES
('Money Transfer', 'XFER', 'Person-to-person money transfer'),
('Airtime Purchase', 'AIRTIME', 'Mobile phone airtime top-up'),
('Bill Payment', 'BILL', 'Utility and service bill payments'),
('Merchant Payment', 'MERCHANT', 'Payment to registered merchants'),
('Cash Withdrawal', 'WITHDRAW', 'Cash withdrawal from agent');

INSERT INTO users (name, phone_number, account_code, user_type, account_balance) VALUES
('Jean Damascene Nkusi', '+250788123456', 'ACC001', 'PERSON', 50000.00),
('Marie Claire Uwase', '+250788234567', 'ACC002', 'PERSON', 75000.00),
('Samuel Mugisha', '+250788345678', 'ACC003', 'PERSON', 120000.00),
('Kigali Electronics Ltd', '+250788456789', 'MER001', 'MERCHANT', 500000.00),
('MTN Rwanda', '+250788567890', 'SYS001', 'SYSTEM', 10000000.00);

INSERT INTO transactions (transaction_id, category_id, amount, currency, fee, balance_after, status, reference_code, description) VALUES
('TXN20260124001', 1, 10000.00, 'RWF', 100.00, 39900.00, 'COMPLETED', 'REF001', 'Money transfer to Marie'),
('TXN20260124002', 1, 15000.00, 'RWF', 150.00, 59850.00, 'COMPLETED', 'REF002', 'Rent payment'),
('TXN20260124003', 4, 25000.00, 'RWF', 0.00, 95000.00, 'COMPLETED', 'REF003', 'Shopping at electronics store'),
('TXN20260124004', 2, 5000.00, 'RWF', 0.00, 34900.00, 'COMPLETED', 'REF004', 'MTN airtime purchase'),
('TXN20260124005', 1, 8000.00, 'RWF', 80.00, 51770.00, 'PENDING', 'REF005', 'Loan repayment to Jean');

INSERT INTO transaction_parties (transaction_id, user_id, role) VALUES
('TXN20260124001', 1, 'SENDER'), ('TXN20260124001', 2, 'RECEIVER'),
('TXN20260124002', 2, 'SENDER'), ('TXN20260124002', 3, 'RECEIVER'),
('TXN20260124003', 3, 'SENDER'), ('TXN20260124003', 4, 'RECEIVER'),
('TXN20260124004', 1, 'SENDER'), ('TXN20260124004', 5, 'RECEIVER'),
('TXN20260124005', 2, 'SENDER'), ('TXN20260124005', 1, 'RECEIVER');

INSERT INTO system_logs (user_id, transaction_id, log_date, log_level, action, message) VALUES
(1, 'TXN20260124001', CURRENT_TIMESTAMP, 'INFO', 'TRANSACTION_CREATED', 'User initiated money transfer successfully'),
(2, 'TXN20260124002', CURRENT_TIMESTAMP, 'INFO', 'TRANSACTION_CREATED', 'User initiated money transfer successfully'),
(3, 'TXN20260124003', CURRENT_TIMESTAMP, 'INFO', 'TRANSACTION_CREATED', 'Merchant payment processed successfully'),
(NULL, NULL, CURRENT_TIMESTAMP, 'WARNING', 'SYSTEM_MAINTENANCE', 'Database backup initiated automatically'),
(1, 'TXN20260124004', CURRENT_TIMESTAMP, 'INFO', 'TRANSACTION_CREATED', 'Airtime purchase completed successfully');

-- ==================================================================
-- Ai was used for correction and optimization of this SQL code.
-- ==================================================================

