-- ============================================================
-- PostgreSQL Schema — Food & Recipe Management
-- ============================================================
-- ความแตกต่างจาก MySQL:
--   AUTO_INCREMENT  → SERIAL (หรือ GENERATED ALWAYS AS IDENTITY)
--   ON UPDATE CURRENT_TIMESTAMP → ต้องใช้ TRIGGER
--   camelCase column → ต้องใส่ double-quote เพื่อ preserve case
--   ENGINE=InnoDB   → ไม่จำเป็น (PostgreSQL ใช้ MVCC เป็น default)
-- ============================================================

-- สร้าง Database (รันก่อน connect ถ้ายังไม่มี)
-- CREATE DATABASE food_recipe_db ENCODING 'UTF8';

-- ============================================================
-- TABLE: foods
-- ============================================================
CREATE TABLE IF NOT EXISTS foods (
    id          SERIAL PRIMARY KEY,
    "nameTh"    VARCHAR(100) NOT NULL,
    category    VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: recipes
-- ============================================================
CREATE TABLE IF NOT EXISTS recipes (
    id            SERIAL PRIMARY KEY,
    food_id       INTEGER NOT NULL,
    "recipeName"  VARCHAR(100) NOT NULL,
    quantity      NUMERIC(10, 2) NOT NULL CHECK (quantity > 0),
    "unitName"    VARCHAR(50) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_recipes_food
        FOREIGN KEY (food_id)
        REFERENCES foods (id)
        ON DELETE CASCADE   -- ลบ Food → ลบ Recipes ทั้งหมดอัตโนมัติ
        ON UPDATE CASCADE
);

-- ============================================================
-- FUNCTION + TRIGGER: auto-update updated_at
-- (MySQL มี ON UPDATE CURRENT_TIMESTAMP — PostgreSQL ต้องใช้ trigger)
-- ============================================================
CREATE OR REPLACE FUNCTION fn_update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger สำหรับ foods
DROP TRIGGER IF EXISTS trg_foods_updated_at ON foods;
CREATE TRIGGER trg_foods_updated_at
    BEFORE UPDATE ON foods
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_updated_at();

-- Trigger สำหรับ recipes
DROP TRIGGER IF EXISTS trg_recipes_updated_at ON recipes;
CREATE TRIGGER trg_recipes_updated_at
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE FUNCTION fn_update_updated_at();

-- ============================================================
-- INDEX (optional — เพิ่ม performance สำหรับ query ที่ใช้บ่อย)
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_recipes_food_id ON recipes (food_id);

-- ============================================================
-- SAMPLE DATA
-- ============================================================
INSERT INTO foods ("nameTh", category) VALUES
    ('ข้าวผัดกุ้ง', 'อาหารไทย'),
    ('ต้มยำกุ้ง',   'อาหารไทย'),
    ('สปาเก็ตตี้',  'อาหารตะวันตก');

INSERT INTO recipes (food_id, "recipeName", quantity, "unitName") VALUES
    (1, 'กุ้ง',      200, 'กรัม'),
    (1, 'ข้าวสวย',  2,   'ถ้วย'),
    (1, 'กระเทียม', 5,   'กลีบ'),
    (2, 'กุ้ง',      300, 'กรัม'),
    (2, 'ตะไคร้',   2,   'ต้น'),
    (2, 'ใบมะกรูด', 5,   'ใบ');
