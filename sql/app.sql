CREATE TABLE flood_data (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `erosion_degree` CHAR(1) NOT NULL, 
    `soil_moisture` DECIMAL(5,2) NOT NULL, 
    `rainfall` DECIMAL(5,2) NOT NULL, 
    `river_discharge` DECIMAL(5,2) NOT NULL, 
    `rf_model` INT NOT NULL, 
    `lr_model` INT NOT NULL, 
    `svc_model` INT NOT NULL,
  	`accuracy` DECIMAL(5,2) NOT NULL,
  	`prediction` VARCHAR(50) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_flood_id ON flood_data (id);

--- db name, flashflood_db
--- table name, flood_data
--- features; erosion_degree, soil_moisture, rainfall, river_discharge




