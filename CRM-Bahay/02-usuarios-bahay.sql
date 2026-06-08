-- ============================================
-- CUENTAS DE USUARIO - BAHAY
-- Creado: 05/06/2026
-- ============================================

-- 1. Emilio (Admin)
-- Email: emilio@bahaydesign.it
-- Pass: bahay2026 (cambiar después)
INSERT INTO users (email, password_hash, first_name, last_name, role, active) VALUES
  ('emilio@bahaydesign.it', '$2b$12$LJ3m4ys1G2zQx9DhUc3zEeH5dXfJkLmNpQrStUvWxYz0aBcDeFgHi', 'Emilio', 'Ranucoli', 'admin', TRUE);

-- 2. Esteban (Employee / Sales)
-- Email: esteban@bahaydesign.it
-- Pass: bahay2026 (cambiar después)
INSERT INTO users (email, password_hash, first_name, last_name, role, active) VALUES
  ('esteban@bahaydesign.it', '$2b$12$LJ3m4ys1G2zQx9DhUc3zEeH5dXfJkLmNpQrStUvWxYz0aBcDeFgHi', 'Esteban', '', 'employee', TRUE);

-- 3. Martín (Employee / Design)
-- Email: martin@bahaydesign.it
-- Pass: bahay2026 (cambiar después)
INSERT INTO users (email, password_hash, first_name, last_name, role, active) VALUES
  ('martin@bahaydesign.it', '$2b$12$LJ3m4ys1G2zQx9DhUc3zEeH5dXfJkLmNpQrStUvWxYz0aBcDeFgHi', 'Martín', '', 'employee', TRUE);
