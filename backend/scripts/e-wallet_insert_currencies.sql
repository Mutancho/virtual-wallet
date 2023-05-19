INSERT IGNORE INTO `e-wallet`.`currencies` (`id`, `currency`)
VALUES
  (1, 'USD'),
  (2, 'EUR'),
  (3, 'GBP'),
  (4, 'JPY'),
  (5, 'CAD'),
  (6, 'AUD'),
  (7, 'TRY'),
  (8, 'BGN');

ALTER TABLE `e-wallet`.`currencies`
MODIFY COLUMN `currency` CHAR(8);