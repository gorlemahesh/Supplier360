-- =========================================================
-- Supplier360 – DATA INSERTS
-- =========================================================


-- =========================================================
-- 1. SUPPLIER MASTER (ALL FEEDS COMBINED)
-- =========================================================
INSERT INTO supplier_master
(supplier_id, supplier_name, registration_number, country, industry, annual_revenue, employees, onboarding_date)
VALUES
-- AUTOMOTIVE (4)
('7F9K3A2B','Ford Motor Company','458201','United States','Automotive',170000000000,173000,'2023-05-12'),
('9D3L6P1Q','General Motors','219384','United States','Automotive',160000000000,163000,'2023-07-18'),
('5Z8X2C7N','Toyota Motor Corporation','672910','Japan','Automotive',310000000000,375000,'2024-01-23'),
('1M4R9T6V','Volkswagen Group','340582','Germany','Automotive',300000000000,675000,'2024-03-05'),

-- AEROSPACE & DEFENSE (4)
('3Q7H2W9E','The Boeing Company','904731','United States','Aerospace & Defense',82000000000,170000,'2023-06-02'),
('8B2N5K4S','Airbus','728517','France','Aerospace & Defense',75000000000,140000,'2024-04-15'),
('6T1Y9U3J','Lockheed Martin','775302','United States','Aerospace & Defense',68000000000,122000,'2023-09-27'),
('4P6D8A5L','RTX (Raytheon Technologies)','665908','United States','Aerospace & Defense',67000000000,185000,'2024-02-07'),

-- ELECTRONICS & SEMICONDUCTORS (4)
('2V5C9M1X','Intel Corporation','451209','United States','Electronics & Semiconductors',55000000000,125000,'2023-08-30'),
('9K1L8J3H','Samsung Electronics','900128','South Korea','Electronics & Semiconductors',230000000000,270000,'2024-05-10'),
('7S4D2F8G','TSMC','873615','Taiwan','Electronics & Semiconductors',80000000000,76000,'2023-11-14'),
('5N2B8V6C','Sony Group Corporation','510492','Japan','Electronics & Semiconductors',85000000000,114000,'2024-06-03'),

-- CHEMICALS (4)
('8M3Q1R7T','BASF SE','834201','Germany','Chemicals',90000000000,112000,'2023-10-06'),
('1A9S4D6F','Dow Inc.','175609','United States','Chemicals',45000000000,37000,'2024-01-11'),
('2H7J5K9L','DuPont de Nemours, Inc.','206742','United States','Chemicals',13000000000,24000,'2023-12-19'),
('3G8F2D5S','LyondellBasell','521890','Netherlands','Chemicals',50000000000,19000,'2024-02-28'),

-- CONSUMER GOODS (4)
('6L4K2J8H','Procter & Gamble','312457','United States','Consumer Goods',85000000000,107000,'2023-05-29'),
('7U1Y3T9R','Unilever','498203','United Kingdom','Consumer Goods',60000000000,128000,'2024-03-21'),
('5W9E2Q6A','Nestlé','652317','Switzerland','Consumer Goods',100000000000,270000,'2023-07-07'),
('4C7V1B8N','The Coca-Cola Company','861540','United States','Consumer Goods',45000000000,79000,'2024-04-01'),

-- ADDITIONAL SUPPLIER MASTER FEED
('F7A9K3D2','Ford','458201','United States','Automotive',170000000000,173000,'2023-08-20'),
('G9M6L1Q3','General Motors Co.','219384','United States','Automotive',160000000000,163000,'2023-10-02'),
('T5Y8Z7C1','Toyota Motor Co.','672910','Japan','Automotive',310000000000,375000,'2024-04-15'),
('V1W4G9R6','Volkswagen Group GmbH','340582','Germany','Automotive',300000000000,675000,'2024-06-10'),
('B3O7E9G1','Boeing','904731','United States','Aerospace & Defense',82000000000,170000,'2023-09-12'),
('I2N5T9L1','Intel Corp.','451209','United States','Electronics & Semiconductors',55000000000,125000,'2023-12-01'),
('B8A3S1F7','BASF','834201','Germany','Chemicals',90000000000,112000,'2024-02-20');


-- =========================================================
-- 2. REQUIRED CERTIFICATES MASTER
-- =========================================================
INSERT INTO required_certificates_master
(requirement_id, industry, required_certificate_type, description)
VALUES
-- AUTOMOTIVE (3)
('R101','Automotive','IATF 16949','Core automotive quality management'),
('R102','Automotive','ISO 9001','General quality management system'),
('R103','Automotive','ISO 14001','Environmental management'),

-- AEROSPACE & DEFENSE (3)
('R201','Aerospace & Defense','AS9100','Aerospace quality management'),
('R202','Aerospace & Defense','ISO 9001','General quality management'),
('R203','Aerospace & Defense','ISO 14001','Environmental management'),

-- ELECTRONICS & SEMICONDUCTORS (3)
('R301','Electronics & Semiconductors','ISO 9001','Quality management for electronics'),
('R302','Electronics & Semiconductors','ISO 27001','Information security management'),
('R303','Electronics & Semiconductors','RoHS','Restriction of hazardous substances'),

-- CHEMICALS (3)
('R401','Chemicals','ISO 14001','Environmental management for chemicals'),
('R402','Chemicals','REACH','EU chemical safety/registration'),
('R403','Chemicals','ISO 9001','Quality management'),

-- CONSUMER GOODS (4)
('R501','Consumer Goods','ISO 9001','Quality management'),
('R502','Consumer Goods','ISO 22000','Food safety management'),
('R503','Consumer Goods','HACCP','Hazard analysis & critical control points'),
('R504','Consumer Goods','GMP','Good manufacturing practice');


-- =========================================================
-- 3. COMPLIANCE CERTIFICATES
-- =========================================================
INSERT INTO compliance_certificates
(certificate_id, supplier_id, certificate_type, certificate_number, issuing_body, issue_date, expiry_date, valid_status, required, notes)
VALUES
/* AUTOMOTIVE */
('C2001','7F9K3A2B','IATF 16949','IATF-FORD-2315','IATF','2023-02-15','2026-02-14','Valid',TRUE,'Automotive QMS'),
('C2002','7F9K3A2B','ISO 9001','ISO9001-FORD-2311','ISO','2023-11-04','2026-11-03','Valid',TRUE,'Quality management'),
('C2003','7F9K3A2B','ISO 14001','ISO14001-FORD-2061','ISO','2020-06-01','2023-05-31','Expired',TRUE,'Environmental mgmt expired'),

('C2004','9D3L6P1Q','IATF 16949','IATF-GM-2319','IATF','2023-03-20','2026-03-19','Valid',TRUE,'Automotive QMS'),
('C2005','9D3L6P1Q','ISO 9001','ISO9001-GM-2306','ISO','2023-06-05','2026-06-04','Valid',TRUE,'Quality management'),
('C2006','9D3L6P1Q','ISO 14001','ISO14001-GM-2212','ISO','2022-12-01','2025-11-30','Valid',TRUE,'Environmental mgmt'),

('C2007','5Z8X2C7N','IATF 16949','IATF-TOY-2018','IATF','2021-01-10','2024-01-09','Expired',TRUE,'Automotive QMS expired'),
('C2008','5Z8X2C7N','ISO 9001','ISO9001-TOY-2401','ISO','2024-01-12','2027-01-11','Valid',TRUE,'Quality management'),
('C2009','5Z8X2C7N','ISO 14001','ISO14001-TOY-2402','ISO','2024-02-01','2027-01-31','Valid',TRUE,'Environmental mgmt'),

('C2010','1M4R9T6V','IATF 16949','IATF-VW-2310','IATF','2023-10-05','2026-10-04','Valid',TRUE,'Automotive QMS'),
('C2011','1M4R9T6V','ISO 9001','ISO9001-VW-2307','ISO','2023-07-01','2026-06-30','Valid',TRUE,'Quality management'),
('C2012','1M4R9T6V','ISO 14001','ISO14001-VW-2403','ISO','2024-03-01','2027-02-28','Valid',TRUE,'Environmental mgmt'),

/* AEROSPACE & DEFENSE */
('C2013','3Q7H2W9E','AS9100','AS9100-BOE-2308','SAE','2023-08-15','2026-08-14','Valid',TRUE,'Aerospace QMS'),
('C2014','3Q7H2W9E','ISO 9001','ISO9001-BOE-2401','ISO','2024-01-10','2027-01-09','Valid',TRUE,'Quality management'),
('C2015','3Q7H2W9E','ISO 14001','ISO14001-BOE-2203','ISO','2022-03-10','2025-03-09','Valid',TRUE,'Environmental mgmt'),

('C2016','8B2N5K4S','AS9100','AS9100-AIR-2019','SAE','2021-05-01','2024-04-30','Expired',TRUE,'Aerospace QMS expired'),
('C2017','8B2N5K4S','ISO 14001','ISO14001-AIR-2402','ISO','2024-02-06','2027-02-05','Valid',TRUE,'Environmental mgmt'),

('C2018','6T1Y9U3J','AS9100','AS9100-LOCK-2304','SAE','2023-04-12','2026-04-11','Valid',TRUE,'Aerospace QMS'),
('C2019','6T1Y9U3J','ISO 9001','ISO9001-LOCK-2310','ISO','2023-10-09','2026-10-08','Valid',TRUE,'Quality management'),

('C2020','4P6D8A5L','AS9100','AS9100-RTX-2309','SAE','2023-09-02','2026-09-01','Valid',TRUE,'Aerospace QMS'),
('C2021','4P6D8A5L','ISO 9001','ISO9001-RTX-2303','ISO','2023-03-05','2026-03-04','Valid',TRUE,'Quality management'),
('C2022','4P6D8A5L','ISO 14001','ISO14001-RTX-2007','ISO','2020-07-01','2023-06-30','Expired',TRUE,'Environmental mgmt expired'),

/* ELECTRONICS & SEMICONDUCTORS */
('C2023','2V5C9M1X','ISO 9001','ISO9001-INT-2306','ISO','2023-06-20','2026-06-19','Valid',TRUE,'Quality mgmt'),
('C2024','2V5C9M1X','ISO 27001','ISO27001-INT-2311','ISO','2023-11-01','2026-10-31','Valid',TRUE,'InfoSec controls'),
('C2025','2V5C9M1X','RoHS','RoHS-INT-2401','IEC','2024-01-25','2027-01-24','Valid',TRUE,'Hazardous substances'),

('C2026','9K1L8J3H','ISO 27001','ISO27001-SAM-2309','ISO','2023-09-12','2026-09-11','Valid',TRUE,'InfoSec controls'),
('C2027','9K1L8J3H','RoHS','RoHS-SAM-2303','IEC','2023-03-15','2026-03-14','Valid',TRUE,'Hazardous substances'),

('C2028','7S4D2F8G','ISO 9001','ISO9001-TSMC-2210','ISO','2022-10-01','2025-09-30','Valid',TRUE,'Quality mgmt'),
('C2029','7S4D2F8G','ISO 27001','ISO27001-TSMC-2501','ISO','2025-01-10',NULL,'Pending',TRUE,'Awaiting final audit'),
('C2030','7S4D2F8G','RoHS','RoHS-TSMC-2405','IEC','2024-05-20','2027-05-19','Valid',TRUE,'Hazardous substances'),

('C2031','5N2B8V6C','ISO 9001','ISO9001-SONY-1904','ISO','2019-04-01','2022-03-31','Expired',TRUE,'Quality mgmt expired'),
('C2032','5N2B8V6C','RoHS','RoHS-SONY-2308','IEC','2023-08-05','2026-08-04','Valid',TRUE,'Hazardous substances'),

/* CHEMICALS */
('C2033','8M3Q1R7T','ISO 14001','ISO14001-BASF-2302','ISO','2023-02-20','2026-02-19','Valid',TRUE,'Environmental mgmt'),
('C2034','8M3Q1R7T','REACH','REACH-BASF-2207','ECHA','2022-07-01','2025-06-30','Valid',TRUE,'EU chemicals compliance'),
('C2035','8M3Q1R7T','ISO 9001','ISO9001-BASF-2404','ISO','2024-04-02','2027-04-01','Valid',TRUE,'Quality mgmt'),

('C2036','1A9S4D6F','ISO 14001','ISO14001-DOW-2212','ISO','2022-12-10','2025-12-09','Valid',TRUE,'Environmental mgmt'),
('C2037','1A9S4D6F','REACH','REACH-DOW-2009','ECHA','2020-09-01','2023-08-31','Expired',TRUE,'REACH registration lapsed'),

('C2038','2H7J5K9L','ISO 9001','ISO9001-DUP-2311','ISO','2023-11-15','2026-11-14','Valid',TRUE,'Quality mgmt'),
('C2039','2H7J5K9L','ISO 14001','ISO14001-DUP-2106','ISO','2021-06-25','2024-06-24','Expired',TRUE,'Environmental mgmt expired'),

('C2040','3G8F2D5S','ISO 14001','ISO14001-LYO-2305','ISO','2023-05-05','2026-05-04','Valid',TRUE,'Environmental mgmt'),
('C2041','3G8F2D5S','REACH','REACH-LYO-2305','ECHA','2023-05-05','2026-05-04','Valid',TRUE,'Chemicals compliance'),
('C2042','3G8F2D5S','ISO 9001','ISO9001-LYO-2403','ISO','2024-03-04','2027-03-03','Valid',TRUE,'Quality mgmt'),

/* CONSUMER GOODS */
('C2043','6L4K2J8H','ISO 9001','ISO9001-PG-2502','ISO','2025-02-01','2028-01-31','Valid',TRUE,'Quality mgmt'),
('C2044','6L4K2J8H','HACCP','HACCP-PG-2409','Codex','2024-09-10',NULL,'Pending',TRUE,'Awaiting final audit'),
('C2045','6L4K2J8H','GMP','GMP-PG-2310','SGS','2023-10-01','2026-09-30','Valid',TRUE,'Good manufacturing practice'),

('C2046','7U1Y3T9R','ISO 9001','ISO9001-UNI-2107','ISO','2021-07-15','2024-07-14','Expired',TRUE,'Renewal overdue'),
('C2047','7U1Y3T9R','ISO 22000','ISO22000-UNI-2403','ISO','2024-03-12','2027-03-11','Valid',TRUE,'Food safety mgmt'),
('C2048','7U1Y3T9R','HACCP','HACCP-UNI-2311','Codex','2023-11-20','2026-11-19','Valid',TRUE,'Food safety'),
('C2049','7U1Y3T9R','GMP','GMP-UNI-2209','SGS','2022-09-14','2025-09-13','Valid',TRUE,'Good manufacturing practice'),

('C2050','5W9E2Q6A','ISO 9001','ISO9001-NES-2312','ISO','2023-12-10','2026-12-09','Valid',TRUE,'Quality mgmt'),
('C2051','5W9E2Q6A','ISO 22000','ISO22000-NES-2403','ISO','2024-03-01','2027-02-28','Valid',TRUE,'Food safety mgmt'),
('C2052','5W9E2Q6A','HACCP','HACCP-NES-2403','Codex','2024-03-01','2027-02-28','Valid',TRUE,'Food safety'),
('C2053','5W9E2Q6A','GMP','GMP-NES-2404','SGS','2024-04-15','2027-04-14','Valid',TRUE,'GMP compliance'),

('C2054','4C7V1B8N','ISO 9001','ISO9001-CC-2301','ISO','2023-01-25','2026-01-24','Valid',TRUE,'Quality mgmt'),
('C2055','4C7V1B8N','ISO 22000','ISO22000-CC-2402','ISO','2024-02-10','2027-02-09','Valid',TRUE,'Food safety mgmt'),
('C2056','4C7V1B8N','HACCP','HACCP-CC-2008','Codex','2020-08-20','2023-08-19','Expired',TRUE,'Food safety expired'),
('C2057','4C7V1B8N','GMP','GMP-CC-2403','SGS','2024-03-12','2027-03-11','Valid',TRUE,'GMP compliance');


-- =========================================================
-- 4. PERFORMANCE HISTORY
-- =========================================================
INSERT INTO supplier_performance_history
(order_id, supplier_id, order_date, promised_delivery_date, actual_delivery_date, on_time,
 delivery_delay_days, quality_compliance_pct, invoice_match_pct, incidents, notes)
VALUES
-- AUTOMOTIVE
('O3001','7F9K3A2B','2023-06-01','2023-06-21','2023-06-20',TRUE,-1,98,99,0,'Early by 1 day'),
('O3002','7F9K3A2B','2023-09-10','2023-10-01','2023-10-04',FALSE,3,95,97,1,'Carrier delay'),

('O3003','9D3L6P1Q','2023-08-05','2023-08-25','2023-08-24',TRUE,-1,97,98,0,'On time'),
('O3004','9D3L6P1Q','2023-11-12','2023-12-05','2023-12-09',FALSE,4,96,96,0,'Weather delay'),

('O3005','5Z8X2C7N','2024-02-01','2024-02-20','2024-02-18',TRUE,-2,99,99,0,'Early delivery'),
('O3006','5Z8X2C7N','2024-04-02','2024-04-25','2024-04-27',FALSE,2,97,98,0,'Minor delay'),

('O3007','1M4R9T6V','2024-03-10','2024-03-31','2024-03-31',TRUE,0,96,95,1,'One cosmetic defect'),
('O3008','1M4R9T6V','2024-05-15','2024-06-06','2024-06-10',FALSE,4,94,93,1,'Packaging issue'),

-- AEROSPACE & DEFENSE
('O3009','3Q7H2W9E','2023-07-01','2023-08-15','2023-08-23',FALSE,8,92,94,2,'Rework required'),
('O3010','3Q7H2W9E','2023-10-05','2023-11-05','2023-11-04',TRUE,-1,96,97,0,'Recovered performance'),

('O3011','6T1Y9U3J','2023-05-18','2023-06-10','2023-06-12',FALSE,2,95,96,0,'Supplier side queue'),
('O3012','6T1Y9U3J','2023-09-02','2023-09-25','2023-09-24',TRUE,-1,97,98,0,'Good recovery'),

-- ELECTRONICS & SEMICONDUCTORS
('O3013','2V5C9M1X','2023-09-01','2023-09-20','2023-09-19',TRUE,-1,99,99,0,'Perfect batch'),
('O3014','2V5C9M1X','2023-12-10','2024-01-05','2024-01-07',FALSE,2,98,99,0,'Logistics backlog'),

('O3015','9K1L8J3H','2023-10-04','2023-10-28','2023-10-29',FALSE,1,96,94,1,'One BOM mismatch'),

('O3016','7S4D2F8G','2024-01-12','2024-02-03','2024-02-01',TRUE,-2,98,97,0,'Early, clean docs'),
('O3017','5N2B8V6C','2023-07-22','2023-08-10','2023-08-14',FALSE,4,90,92,2,'High defect rate'),

-- CHEMICALS
('O3018','8M3Q1R7T','2023-11-01','2023-11-22','2023-11-22',TRUE,0,97,98,0,'On spec'),

('O3019','1A9S4D6F','2022-12-05','2022-12-27','2022-12-30',FALSE,3,95,93,1,'Docs corrected post-GR'),

('O3020','3G8F2D5S','2024-02-18','2024-03-12','2024-03-11',TRUE,-1,98,97,0,'Good performance');

