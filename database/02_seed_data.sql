USE ecommerce;

INSERT INTO categories (category_id, category_name, description) VALUES
  (1, 'Electronics', 'Phones, computers, and electronic accessories'),
  (2, 'Home and Kitchen', 'Appliances and household essentials'),
  (3, 'Fashion', 'Clothing and fashion accessories'),
  (4, 'Books', 'Printed books and learning material'),
  (5, 'Sports', 'Fitness and outdoor equipment')
ON DUPLICATE KEY UPDATE category_name = VALUES(category_name);

INSERT INTO customers
  (customer_id, first_name, last_name, email, phone, city, state, country, postal_code, created_at)
VALUES
  (1, 'Aarav', 'Sharma', 'aarav.sharma@example.com', '+91-9876500001', 'Mumbai', 'Maharashtra', 'India', '400001', '2025-01-05 09:20:00'),
  (2, 'Diya', 'Patel', 'diya.patel@example.com', '+91-9876500002', 'Ahmedabad', 'Gujarat', 'India', '380001', '2025-01-18 14:10:00'),
  (3, 'Arjun', 'Reddy', 'arjun.reddy@example.com', '+91-9876500003', 'Hyderabad', 'Telangana', 'India', '500001', '2025-02-02 11:45:00'),
  (4, 'Ananya', 'Singh', 'ananya.singh@example.com', '+91-9876500004', 'Lucknow', 'Uttar Pradesh', 'India', '226001', '2025-02-11 16:30:00'),
  (5, 'Kabir', 'Mehta', 'kabir.mehta@example.com', '+91-9876500005', 'Bengaluru', 'Karnataka', 'India', '560001', '2025-03-01 10:05:00'),
  (6, 'Meera', 'Nair', 'meera.nair@example.com', '+91-9876500006', 'Kochi', 'Kerala', 'India', '682001', '2025-03-16 13:40:00'),
  (7, 'Vihaan', 'Gupta', 'vihaan.gupta@example.com', '+91-9876500007', 'Delhi', 'Delhi', 'India', '110001', '2025-04-03 08:55:00'),
  (8, 'Isha', 'Joshi', 'isha.joshi@example.com', '+91-9876500008', 'Pune', 'Maharashtra', 'India', '411001', '2025-04-20 17:15:00')
ON DUPLICATE KEY UPDATE email = VALUES(email);

INSERT INTO products
  (product_id, category_id, sku, product_name, unit_price, stock_quantity, is_active, created_at)
VALUES
  (1, 1, 'ELEC-001', 'Wireless Headphones', 2499.00, 75, TRUE, '2025-01-01 08:00:00'),
  (2, 1, 'ELEC-002', 'Mechanical Keyboard', 3299.00, 42, TRUE, '2025-01-01 08:00:00'),
  (3, 1, 'ELEC-003', 'USB-C Hub', 1799.00, 110, TRUE, '2025-01-01 08:00:00'),
  (4, 2, 'HOME-001', 'Electric Kettle', 1499.00, 60, TRUE, '2025-01-01 08:00:00'),
  (5, 2, 'HOME-002', 'Cotton Bedsheet Set', 1299.00, 90, TRUE, '2025-01-01 08:00:00'),
  (6, 3, 'FASH-001', 'Classic Denim Jacket', 2799.00, 35, TRUE, '2025-01-01 08:00:00'),
  (7, 3, 'FASH-002', 'Running Shoes', 3499.00, 55, TRUE, '2025-01-01 08:00:00'),
  (8, 4, 'BOOK-001', 'Python Data Engineering', 899.00, 125, TRUE, '2025-01-01 08:00:00'),
  (9, 4, 'BOOK-002', 'Cloud Architecture Guide', 1099.00, 80, TRUE, '2025-01-01 08:00:00'),
  (10, 5, 'SPRT-001', 'Yoga Mat', 799.00, 100, TRUE, '2025-01-01 08:00:00'),
  (11, 5, 'SPRT-002', 'Adjustable Dumbbell Set', 4599.00, 25, TRUE, '2025-01-01 08:00:00'),
  (12, 2, 'HOME-003', 'Stainless Steel Cookware', 3999.00, 30, TRUE, '2025-01-01 08:00:00')
ON DUPLICATE KEY UPDATE sku = VALUES(sku);

INSERT INTO orders
  (order_id, customer_id, order_date, status, shipping_address, total_amount)
VALUES
  (1, 1, '2025-05-02 10:15:00', 'delivered', 'Fort, Mumbai, Maharashtra 400001', 4298.00),
  (2, 2, '2025-05-05 18:20:00', 'delivered', 'Navrangpura, Ahmedabad, Gujarat 380009', 2799.00),
  (3, 3, '2025-05-11 12:05:00', 'shipped', 'Banjara Hills, Hyderabad, Telangana 500034', 4998.00),
  (4, 4, '2025-05-18 09:40:00', 'processing', 'Hazratganj, Lucknow, Uttar Pradesh 226001', 2198.00),
  (5, 5, '2025-06-01 15:35:00', 'delivered', 'Indiranagar, Bengaluru, Karnataka 560038', 4599.00),
  (6, 6, '2025-06-09 11:25:00', 'cancelled', 'Marine Drive, Kochi, Kerala 682031', 3499.00),
  (7, 7, '2025-06-17 20:10:00', 'pending', 'Connaught Place, Delhi 110001', 7398.00),
  (8, 8, '2025-06-25 13:50:00', 'shipped', 'Shivajinagar, Pune, Maharashtra 411005', 4098.00),
  (9, 1, '2025-07-03 08:30:00', 'delivered', 'Fort, Mumbai, Maharashtra 400001', 1698.00),
  (10, 3, '2025-07-12 16:45:00', 'processing', 'Banjara Hills, Hyderabad, Telangana 500034', 3999.00)
ON DUPLICATE KEY UPDATE status = VALUES(status);

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
  (1, 1, 1, 1, 2499.00), (2, 1, 3, 1, 1799.00),
  (3, 2, 6, 1, 2799.00),
  (4, 3, 2, 1, 3299.00), (5, 3, 4, 1, 1499.00), (6, 3, 8, 1, 200.00),
  (7, 4, 9, 2, 1099.00),
  (8, 5, 11, 1, 4599.00),
  (9, 6, 7, 1, 3499.00),
  (10, 7, 2, 1, 3299.00), (11, 7, 12, 1, 3999.00), (12, 7, 10, 1, 100.00),
  (13, 8, 5, 1, 1299.00), (14, 8, 6, 1, 2799.00),
  (15, 9, 8, 1, 899.00), (16, 9, 10, 1, 799.00),
  (17, 10, 12, 1, 3999.00)
ON DUPLICATE KEY UPDATE quantity = VALUES(quantity);

INSERT INTO payments
  (payment_id, order_id, payment_date, payment_method, amount, payment_status, transaction_reference)
VALUES
  (1, 1, '2025-05-02 10:17:00', 'credit_card', 4298.00, 'completed', 'TXN-20250502-001'),
  (2, 2, '2025-05-05 18:22:00', 'upi', 2799.00, 'completed', 'TXN-20250505-002'),
  (3, 3, '2025-05-11 12:07:00', 'debit_card', 4998.00, 'completed', 'TXN-20250511-003'),
  (4, 4, '2025-05-18 09:42:00', 'net_banking', 2198.00, 'completed', 'TXN-20250518-004'),
  (5, 5, '2025-06-01 15:37:00', 'upi', 4599.00, 'completed', 'TXN-20250601-005'),
  (6, 6, '2025-06-09 11:27:00', 'credit_card', 3499.00, 'refunded', 'TXN-20250609-006'),
  (7, 7, '2025-06-17 20:10:00', 'cash_on_delivery', 7398.00, 'pending', 'TXN-20250617-007'),
  (8, 8, '2025-06-25 13:52:00', 'upi', 4098.00, 'completed', 'TXN-20250625-008'),
  (9, 9, '2025-07-03 08:32:00', 'debit_card', 1698.00, 'completed', 'TXN-20250703-009'),
  (10, 10, '2025-07-12 16:47:00', 'credit_card', 3999.00, 'completed', 'TXN-20250712-010')
ON DUPLICATE KEY UPDATE payment_status = VALUES(payment_status);
