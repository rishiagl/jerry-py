DROP TABLE customer;
CREATE TABLE IF NOT EXISTS customer(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   phone_no TEXT NOT NULL UNIQUE,
   name TEXT NOT NULL,
   address TEXT NOT NULL
);
INSERT INTO customer(phone_no, name, address) VALUES ('7970460076', 'Rishi Agarwal', 'Hume Pipe Nirmal Nagar, Jamshedpur');
INSERT INTO customer(phone_no, name, address) VALUES ('9334638328', 'Rajesh Agarwal', 'Hume Pipe Nirmal Nagar, Jamshedpur');
INSERT INTO customer(phone_no, name, address) VALUES ('8789738298', 'Akash Kumar', 'Hume Pipe Nirmal Nagar, Jamshedpur');

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

DROP TABLE invoice;
CREATE TABLE IF NOT EXISTS invoice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_created TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customer(id) ON DELETE RESTRICT
);
INSERT INTO invoice(date_created, customer_name, customer_id) VALUES('2023-09-16', 'RIshi Agarwal', 1);

DROP TABLE invoice_item_list;
CREATE TABLE IF NOT EXISTS invoice_item_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    rate INTEGER NOT NULL,
    UNIQUE(invoice_id, product_id)
    FOREIGN KEY(invoice_id) REFERENCES invoice(id) ON DELETE RESTRICT,
    FOREIGN KEY(product_id) REFERENCES product(id) ON DELETE RESTRICT
);
INSERT INTO invoice_item_list(invoice_id, product_id, qty, rate) VALUES(1, 1, 2, 5000);

DROP TABLE company;
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    legal_name TEXT NOT NULL,
    address TEXT NOT NULL,
    gstn  TEXT NOT NULL UNIQUE,
    phone_no TEXT NOT NULL,
    email TEXT NOT NULL,
    website TEXT NOT NULL,
    owner_email TEXT NOT NULL
);
INSERT INTO company(name, legal_name, address, gstn, phone_no, email, website, owner_email) VALUES('My Choice Electronics', 'My Choice', 'Sakchi, Jamshedpur, Jharkhand, India - 831001', '20AEYPA0067P1ZB', '9334638328', 'mychoice_jamshedpur@rediffmail.com', 'www.mychoiceelectronics.com', 'mychoiceeletronics01@gmail.com');
INSERT INTO company(name, legal_name, address, gstn, phone_no, email, website, owner_email) VALUES('Synergy Limited', 'Synergy Limited', 'Bistupur, Jamshedpur, Jharkhand, India - 831001', '20AHDVA0067P1ZB', '7979888545', 'synergylimited@gmail.com', 'www.synergylimited.com', 'rishi58235@gmail.com');

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


DROP TABLE trasaction_table;
CREATE TABLE IF NOT EXISTS transaction_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    prefix TEXT NOT NULL,
    last_inserted_id INTEGER,
    UNIQUE(name, company_name),
    FOREIGN KEY(company_name) REFERENCES company(name) ON DELETE RESTRICT
);

INSERT INTO transaction_table(name, company_name, prefix, last_inserted_id) VALUES('My Choice', 'invoice', 'inv', '0');
INSERT INTO transaction_table(name, company_name, prefix, last_inserted_id) VALUES('Synergy Limited', 'invoice', 'inv', '0');