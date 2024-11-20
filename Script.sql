-- 1. Customers Table
CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT
);

-- 2. Products Table
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL,
    stock_quantity INTEGER NOT NULL,
    supplier_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES Categories (category_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
);

-- 3. Categories Table
CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 4. Orders Table
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Pending',
    employee_id INTEGER,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
    FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
);

-- 5. OrderItems Table (Many-to-Many between Orders and Products)
CREATE TABLE OrderItems (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (product_id) REFERENCES Products (product_id)
);

-- 6. Employees Table
CREATE TABLE Employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT,
    hire_date DATE,
    salary REAL
);

-- 7. Suppliers Table
CREATE TABLE Suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    contact_name TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    country TEXT
);

-- 8. Payments Table
CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount REAL NOT NULL,
    payment_method TEXT,
    FOREIGN KEY (order_id) REFERENCES Orders (order_id)
);

-- Insert Sample Data into Categories
INSERT INTO Categories (category_name, description) VALUES
('Electronics', 'Electronic gadgets and devices'),
('Clothing', 'Apparel for men, women, and children'),
('Furniture', 'Home and office furniture'),
('Groceries', 'Everyday food items and essentials');

-- Insert Sample Data into Suppliers
INSERT INTO Suppliers (supplier_name, contact_name, phone, address, city, country) VALUES
('Tech Supplies Inc.', 'Alice Johnson', '123-456-7890', '123 Tech Lane', 'New York', 'USA'),
('Fashion World', 'Bob Smith', '987-654-3210', '45 Fashion St.', 'Los Angeles', 'USA');

-- Insert Sample Data into Products
INSERT INTO Products (product_name, category_id, price, stock_quantity, supplier_id) VALUES
('Smartphone', 1, 699.99, 50, 1),
('Laptop', 1, 1299.99, 30, 1),
('T-Shirt', 2, 19.99, 100, 2),
('Dining Table', 3, 499.99, 10, NULL),
('Milk', 4, 2.99, 200, NULL);

-- Insert Sample Data into Customers
INSERT INTO Customers (first_name, last_name, email, phone, address, city, country) VALUES
('John', 'Doe', 'john.doe@example.com', '555-1234', '123 Elm St.', 'New York', 'USA'),
('Jane', 'Smith', 'jane.smith@example.com', '555-5678', '456 Oak St.', 'Los Angeles', 'USA');

-- Insert Sample Data into Employees
INSERT INTO Employees (first_name, last_name, position, hire_date, salary) VALUES
('Alice', 'Brown', 'Manager', '2022-01-15', 60000),
('Bob', 'Davis', 'Salesperson', '2023-03-10', 40000);

-- Insert Sample Data into Orders
INSERT INTO Orders (customer_id, order_date, status, employee_id, total_amount) VALUES
(1, '2024-10-01 10:30:00', 'Completed', 2, 719.98),
(2, '2024-10-05 15:00:00', 'Pending', 1, 19.99);

-- Insert Sample Data into OrderItems
INSERT INTO OrderItems (order_id, product_id, quantity, price_per_unit) VALUES
(1, 1, 1, 699.99),
(1, 3, 1, 19.99),
(2, 3, 1, 19.99);

-- Insert Sample Data into Payments
INSERT INTO Payments (order_id, payment_date, amount, payment_method) VALUES
(1, '2024-10-01 10:35:00', 719.98, 'Credit Card');

-- Verify Customers
SELECT * FROM Customers;
