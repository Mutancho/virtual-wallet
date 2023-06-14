# If you decide to use this test data you need to ensure that the registration of the users is manually done in stripe and chatengine and update the stripe ids stripe provides into the database

INSERT INTO `e-wallet`.users (username, password, is_admin, is_blocked, two_factor_method, anti_money_laundry_checked, email_verified, stripe_id, title, first_name, last_name, gender, dob, address, email, phone_number, identity_document) VALUES
('SamWinchester', 'Sammy10?', 1, 0, 'email', 1, 1, 'stripe_123', 'Mr', 'Sam', 'Winchester', 'male', '1983-05-02', 'Lawrence, Kansas', 'sammy@example.com', '0888123456', 'photo'),
('DeanWinchester', 'Deans10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Dean', 'Winchester', 'male', '1979-01-24', 'Lawrence, Kansas', 'impala67@example.com', '0889123456', 'photo'),
('StefanSalvatore', 'Stefan10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Stefan', 'Salvatore', 'male', '1989-11-01', 'Mystic Falls, Virginia', 'stefan@example.com', '0889234567', 'photo'),
('DamonSalvatore', 'Damon10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Damon', 'Salvatore', 'male', '1969-06-18', 'Mystic Falls, Virginia', 'damon@example.com', '0888890123', 'photo'),
('ElijahMikaelson', 'Elijah10?', 1, 0, 'email', 1, 1, 'stripe_123', 'Mr', 'Elijah', 'Mikaelson', 'male', '1933-04-27', 'Mystic Falls, Virginia', 'elijah@example.com', '0888901234', 'photo'),
('BarryAllen', 'Barry10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Barry', 'Allen', 'male', '1989-03-14', 'Central City', 'theflash@example.com', '0888012345', 'photo'),
('ScottMcCall', 'Scott10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Scott', 'McCall', 'male', '1994-09-16', 'Beacon Hills', 'scott@example.com', '0888678901', 'photo'),
('JangUk', 'Naksu10?', 0, 0, 'email', 1, 1, 'stripe_456', 'Mr', 'Uk', 'Jang', 'male', '1998-04-27', 'Kingdom of Daeho', 'kingstar@example.com', '0888456789', 'photo');

INSERT INTO `e-wallet`.contacts (user_id, contact_id) VALUES
(11, 12),(12, 11),(11, 13),(11, 14),(11, 15),(11, 16),(11, 17),
(11, 18),(12, 13),(12, 14),(12, 15),(12, 16),(12, 17),(12, 18),
(13, 14),(13, 15),(13, 16),(13, 17),(13, 18),(14, 15),(14, 16),
(14, 17),(14, 18),(15, 16),(15, 17),(15, 18),(16, 17),(16, 18),
(17, 18);

INSERT INTO `e-wallet`.wallets (name, balance, type, is_active, default_wallet, creator_id, currency_id) VALUES
('Personal (Sam)', 1000.00, 'personal', 1, 1, 11, 1),
('Joint Wallet 1', 5000.00, 'joint', 1, 0, 11, 1),
('Personal (Dean)', 2500.00, 'personal', 1, 1, 12, 2),
('Joint Wallet 2', 7000.00, 'joint', 1, 0, 12, 2),
('Personal (Stefan)', 1500.00, 'personal', 1, 1, 13, 3),
('Personal (Damon)', 2000.00, 'personal', 1, 1, 14, 4),
('Personal (Elijah)', 3000.00, 'personal', 1, 1, 15, 5),
('Personal (Barry)', 500.00, 'personal', 1, 1, 16, 6),
('Personal (Scott)', 1000.00, 'personal', 1, 1, 17, 7),
('Personal (Uk)', 800.00, 'personal', 1, 1, 18, 8);

INSERT INTO `e-wallet`.transactions (amount, accepted_by_recipient, confirmed, sent_at, received_at, is_recurring, recipient_id, category, wallet_id) VALUES
-- Sam's transactions
(100.00, 1, 1, '2023-06-13 10:00:00', NULL, 1, 12, 'Rent', 5),
(50.00, 1, 1, '2023-06-13 11:00:00', NULL, 1, 11, 'Food & Groceries', 5),
(75.00, 1, 1, '2023-06-14 12:00:00', NULL, 0, 13, 'Utilities', 5),
(50.00, 1, 1, '2023-06-15 14:00:00', NULL, 0, 14, 'Transportation', 5),
(100.00, 1, 1, '2023-06-16 15:00:00', NULL, 0, 15, 'Travel', 5),
(25.00, 1, 1, '2023-06-17 16:00:00', NULL, 0, 16, 'Transportation', 5),
(50.00, 1, 1, '2023-06-18 17:00:00', NULL, 0, 17, 'Health & Fitness', 5),
(100.00, 1, 1, '2023-06-19 18:00:00', NULL, 0, 18, 'Other', 5),
-- Dean's transactions
(200.00, 1, 1, '2023-06-13 10:30:00', NULL, 0, 11, 'Rent', 7),
(30.00, 1, 1, '2023-06-13 11:30:00', NULL, 0, 12, 'Food & Groceries', 7),
(50.00, 1, 1, '2023-06-14 12:30:00', NULL, 0, 14, 'Health & Fitness', 7),
(75.00, 1, 1, '2023-06-15 14:30:00', NULL, 0, 15, 'Travel', 7),
(20.00, 1, 1, '2023-06-16 15:30:00', NULL, 0, 16, 'Transportation', 7),
(40.00, 1, 1, '2023-06-17 16:30:00', NULL, 0, 17, 'Other', 7),
(80.00, 1, 1, '2023-06-18 17:30:00', NULL, 0, 18, 'Health & Fitness', 7),
(150.00, 1, 1, '2023-06-19 18:30:00', NULL, 0, 13, 'Utilities', 7);

INSERT INTO `e-wallet`.currency_conversions (base_currency_id, quote_currency_id, fx_rate, transaction_id) VALUES
(1, 2, 0.85, 13),
(1, 3, 0.75, 14);

INSERT INTO `e-wallet`.recurring_transactions (transaction_id, `interval`, next_occurrence, status) VALUES
(13, 30, '2023-07-13', 'active'),
(14, 7, '2023-06-20', 'active');

INSERT INTO `e-wallet`.referrals (email, expiry_date, is_used, user_id) VALUES
('referral1@example.com', '2023-06-30', 0, 11),
('referral2@example.com', '2023-06-30', 0, 12);

INSERT INTO `e-wallet`.transfers (type, amount, wallet_id) VALUES
('deposit', 100.00, 5),
('withdrawal', 50.00, 5);

INSERT INTO `e-wallet`.users_wallets(user_id,wallet_id,is_creator) VALUES
(11,6,1),(12,6,0),(13,6,0),(14,6,0),(15,6,0),
(12,8,1),(15,8,0),(16,8,0),(17,8,0),(18,6,0);
