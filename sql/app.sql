CREATE TABLE flood_data (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `prediction_text` VARCHAR(100) NOT NULL, 
    `lr_model` INT NOT NULL, 
    `rf_model` INT NOT NULL, 
    `svc_model` INT NOT NULL,
    `accuracy` INT NOT NULL, 
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_flood_id ON flood_data (id);

--- db name, flashflood_db
--- table name, flood_data