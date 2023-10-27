DROP TABLE company;
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    legal_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    pincode TEXT NOT NULL,
    gstn  TEXT NOT NULL UNIQUE,
    phone_no TEXT NOT NULL,
    email TEXT NOT NULL,
    website TEXT,
    bank_name TEXT NOT NULL,
    account_no TEXT NOT NULL,
    ifsc_code TEXT NOT NULL,
    upi_id TEXT NOT NULL,
    owner_email TEXT NOT NULL
);
INSERT INTO company(name, legal_name, address, city, state, pincode, gstn, phone_no, email, website, bank_name, account_no, ifsc_code, upi_id, owner_email) VALUES('My Choice Electronics', 'My Choice', 'Block-A, Sakchi', 'Jamshedpur', 'Jharkhand', '831001', '20AEYPA0067P1ZB', '9334638328', 'mychoice_jamshedpur@rediffmail.com', 'www.mychoiceelectronics.com', 'HDFC BANK', '74964976596957', 'HDFC108983', 'upiid@okhdfc', 'mychoiceeletronics01@gmail.com');
INSERT INTO company(name, legal_name, address, city, state, pincode, gstn, phone_no, email, website, bank_name, account_no, ifsc_code, upi_id, owner_email) VALUES('Synergy Limited', 'Synergy Limited', 'Bistupur', 'Jamshedpur', 'Jharkhand', '831001', '20AHDVA0067P1ZB', '7979888545', 'synergylimited@gmail.com', 'www.synergylimited.com', 'HDFC BANK', '74964976596957', 'HDFC108983', 'upiid@okhdfc', 'rishi58235@gmail.com');

DROP TABLE company_users;
CREATE TABLE IF NOT EXISTS company_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    user_email TEXT NOT NULL,
    FOREIGN KEY(company_id) REFERENCES company(id) ON DELETE RESTRICT,
    FOREIGN KEY(company_name) REFERENCES company(name) ON DELETE RESTRICT
);
INSERT INTO company_users(company_id, company_name, user_email) VALUES(1, 'My Choice', 'mychoiceelectronics01@gmail.com');
INSERT INTO company_users(company_id, company_name, user_email) VALUES(2, 'Synergy Limited', 'rishi58235@gmail.com');

DROP TABLE customer;
CREATE TABLE IF NOT EXISTS customer(
   phone_no TEXT PRIMARY KEY,
   name TEXT NOT NULL,
   address TEXT NOT NULL,
   state TEXT NOT NULL,
   pincode TEXT
);
INSERT INTO customer(phone_no, name, address, state, pincode) VALUES ('7970460076', 'Rishi Agarwal', 'Hume Pipe Nirmal Nagar, Jamshedpur', 'Jharkhand', '831001');
INSERT INTO customer(phone_no, name, address, state, pincode) VALUES ('9334638328', 'Rajesh Agarwal', 'Hume Pipe Nirmal Nagar, Jamshedpur', 'Jharkhand', '831009');
INSERT INTO customer(phone_no, name, address, state, pincode) VALUES     ('8789738298', 'Akash Kumar', 'Hume Pipe Nirmal Nagar, Jamshedpur', 'west bengal', '821001');

DROP TABLE product;
CREATE TABLE IF NOT EXISTS product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    hsn TEXT NOT NULL,
    tax_rate INTEGER NOT NULL
);
INSERT INTO product(name, hsn, tax_rate) VALUES ('Bajaj Air Cooler', '84796000', 18);
INSERT INTO product(name, hsn, tax_rate) VALUES ('Voltas Air Conditioner', '8415', 28);
INSERT INTO product(name, hsn, tax_rate) VALUES ('Samsung Refridgerator', '82344523', 18);

DROP TABLE transaction_metadata;
CREATE TABLE IF NOT EXISTS transaction_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    company_name TEXT NOT NULL,
    prefix TEXT NOT NULL,
    last_inserted_id INTEGER,
    UNIQUE(type, company_name),
    FOREIGN KEY(company_name) REFERENCES company(name) ON DELETE RESTRICT
);

INSERT INTO transaction_metadata(type, company_name, prefix, last_inserted_id) VALUES('invoice', 'My Choice', 'inv', '1');
INSERT INTO transaction_metadata(type, company_name, prefix, last_inserted_id) VALUES('invoice', 'Synergy Limited', 'inv', '0');

DROP TABLE invoice;
CREATE TABLE IF NOT EXISTS invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT NOt NULL,
    company_name TEXT NOT NULL,
    date_created TEXT NOT NULL,
    customer_phone_no INTEGER NOT NULL,
    taxable_value INTEGER NOT NULL,
    cgst INTEGER NOT NULL,
    sgst INTEGER NOT NULL,
    igst INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    amount_paid INTEGER NOT NULL,
    finance_name TEXT,
    finance_duration_in_months INTEGER,
    dp INTEGER,
    emi INTEGER,
    narration TEXT,
    is_cancelled INTEGER NOT NULL,
    UNIQUE(company_name, invoice_no),
    FOREIGN KEY(customer_phone_no) REFERENCES customer(phone_no) ON DELETE RESTRICT
);
INSERT INTO invoice(invoice_no, company_name, date_created, customer_phone_no, taxable_value, cgst, sgst, igst, amount, amount_paid, finance_name, finance_duration_in_months, dp, emi, narration, is_cancelled) VALUES('INV1', 'My Choice', '2023-09-16', '7970460076', 10000, 900, 900, 0, 11800, 10000, 'Bajaj Finance', 2800, 1000, 10, 'New Narration', 0);

DROP TABLE invoice_product;
CREATE TABLE IF NOT EXISTS invoice_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    invoice_no TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    description TEXT,
    qty INTEGER NOT NULL,
    rate INTEGER NOT NULL,
    UNIQUE(company_name, invoice_no, product_id)
    FOREIGN KEY(invoice_no) REFERENCES invoice(id) ON DELETE RESTRICT,
    FOREIGN KEY(product_id) REFERENCES product(id) ON DELETE RESTRICT
);
INSERT INTO invoice_product(company_name, invoice_no, product_id, description, qty, rate) VALUES('My Choice', 'INV1', 1, 'a des', 2, 5000);