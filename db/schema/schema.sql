-- =========================================================
-- 1. SUPPLIER MASTER
-- =========================================================

CREATE TABLE supplier_master (
  supplier_id         VARCHAR(12) PRIMARY KEY,
  supplier_name       VARCHAR(100) NOT NULL,
  registration_number CHAR(6)      NOT NULL UNIQUE,
  country             VARCHAR(60)  NOT NULL,
  industry            VARCHAR(60)  NOT NULL,
  annual_revenue      BIGINT       NOT NULL,
  employees           INT          NOT NULL,
  onboarding_date     DATE         NOT NULL
);


-- =========================================================
-- 2. REQUIRED CERTIFICATES MASTER
-- =========================================================

CREATE TABLE required_certificates_master (
  requirement_id            VARCHAR(10) PRIMARY KEY,
  industry                  VARCHAR(60) NOT NULL,
  required_certificate_type VARCHAR(60) NOT NULL,
  description               VARCHAR(150),
  CONSTRAINT uq_industry_cert UNIQUE (industry, required_certificate_type)
);


-- =========================================================
-- 3. COMPLIANCE CERTIFICATES
-- =========================================================

CREATE TABLE compliance_certificates (
  certificate_id      VARCHAR(12) PRIMARY KEY,
  supplier_id         VARCHAR(12) NOT NULL,
  certificate_type    VARCHAR(60) NOT NULL,
  certificate_number  VARCHAR(24) NOT NULL,
  issuing_body        VARCHAR(60) NOT NULL,
  issue_date          DATE NOT NULL,
  expiry_date         DATE,
  valid_status        VARCHAR(12) NOT NULL,
  required            BOOLEAN NOT NULL,
  notes               VARCHAR(200),
  CONSTRAINT fk_cert_supplier
    FOREIGN KEY (supplier_id) REFERENCES supplier_master(supplier_id)
);


-- =========================================================
-- 4. SUPPLIER PERFORMANCE HISTORY
-- =========================================================

CREATE TABLE supplier_performance_history (
  order_id               VARCHAR(12) PRIMARY KEY,
  supplier_id            VARCHAR(12) NOT NULL,
  order_date             DATE NOT NULL,
  promised_delivery_date DATE NOT NULL,
  actual_delivery_date   DATE NOT NULL,
  on_time                BOOLEAN NOT NULL,
  delivery_delay_days    INT,
  quality_compliance_pct DECIMAL(5,2),
  invoice_match_pct      DECIMAL(5,2),
  incidents              INT,
  notes                  VARCHAR(200),
  CONSTRAINT fk_supplier_perf
    FOREIGN KEY (supplier_id) REFERENCES supplier_master(supplier_id)
);
