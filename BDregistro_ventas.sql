DROP database if exists BDregistro_ventas;
create database BDregistro_ventas;
use BDregistro_ventas;

Create table ref_pago_comanda (
	codigo_tipo_de_pago char(6) primary key,
	nombre_tipo_pago varchar(8)
) ENGINE=InnoDB;

Create table local (
	id_local char(7) primary key,
	direccion_local varchar(50) 
) ENGINE=InnoDB;

Create table cierre_caja (
	fecha date primary key,
 	yape_Veri decimal(5,2) ,
    efectivo_Veri decimal(5,2) ,
    tarjeta_Veri decimal(5,2) ,
    total_veri decimal(6,2) ,
	efectivo_comanda decimal(5,2) ,
    tarjeta_comanda decimal(5,2) ,
    yape_comanda decimal(5,2) ,
    total_comanda decimal(6,2)
) ENGINE=InnoDB;


Create table comanda (
	id_comanda char(8) primary key,
 	total decimal(5,2) ,
    fecha_cierre_de_caja date,
    foreign key (fecha_cierre_de_caja) references cierre_caja(fecha)
) ENGINE=InnoDB;


Create table producto (
	id_producto char(6) primary key,
 	descripcion_producto varchar(60) ,
    precio_unitario_producto decimal (5,2)
        
) ENGINE=InnoDB;

Create table pago_comanda (
	id_comanda char(8) ,
 	codigo_tipo_de_pago varchar(6) ,
	total_tipo_de_pago decimal(5,2),
    primary key(id_comanda,codigo_tipo_de_pago),
    foreign key (id_comanda) references comanda(id_comanda),
    foreign key (Codigo_Tipo_de_Pago) references ref_pago_comanda(Codigo_Tipo_de_Pago)
) ENGINE=InnoDB;

Create table detalle_comanda (
	id_comanda char(8) ,
 	id_producto char(6) ,
	cantidad_producto int,
    subtotal decimal(5,2),
    primary key(id_comanda,id_producto),
    foreign key (id_comanda) references comanda(id_comanda),
    foreign key (id_producto) references producto(id_producto)
) ENGINE=InnoDB;

Create table ventas_tarjetas (
	ref_pago char(4) primary key,
 	num_tarjetas char(7) ,
    tipo_tarjeta varchar (16),
    monto_cobrado decimal(5,2)
        
) ENGINE=InnoDB;


Create table reporte_tarjetas (
	id_cierre_tarjetas varchar(11) primary key ,
 	fecha date,
	hora time,
    total_credito decimal(5,2),
    total_debito decimal(5,2),
    total_soles decimal(5,2),
    fecha_cierre_de_caja date,
    id_local varchar(7),
    foreign key (fecha_cierre_de_caja) references cierre_caja(fecha),
    foreign key (id_local) references local(id_local)
) ENGINE=InnoDB;



create table pagos_tarjeta(
	id_cierre_tarjetas varchar(11) ,
 	ref_pago varchar(4),
	primary key(id_cierre_tarjetas,ref_pago),
    foreign key (id_cierre_tarjetas) references reporte_tarjetas(id_cierre_tarjetas),
    foreign key (ref_pago) references ventas_tarjetas(ref_pago)
) ENGINE=InnoDB;


-- insertar dartos a las tablas

INSERT INTO Producto (ID_Producto, Descripcion_Producto, Precio_Unitario_Producto) VALUES
-- Piqueos
('PIQ001', 'Choritos a la Chalaca', 20.00),
('PIQ002', 'Pulpito a la Chalaca', 20.00),
('PIQ003', 'Brochetas de Langostino', 30.00),
('PIQ004', 'Brochetas de Pollo', 25.00),
('PIQ005', 'Piqueo Muelle 69 (Ronda Fría)', 45.00),

-- Shots
('SHT001', 'Leche de Tigre', 10.00),
('SHT002', 'Shot de Pescado', 18.00),
('SHT003', 'Shot de Conchas Negras', 30.00),

-- Tiraditos
('TIR001', 'Tiradito de Pescado Clásico', 30.00),
('TIR002', 'Pulpo al Olivo', 33.00),

-- Cebiches
('CEV001', 'Cebiche de Pescado', 28.00),
('CEV002', 'Cebiche de Mariscos', 30.00),
('CEV003', 'Cebiche Mixto', 30.00),
('CEV004', 'Cebiche de Conchas Negras', 30.00),
('CEV005', 'Cebiche de Corvina y Pulpo en Crema de Rocoto', 35.00),
('CEV006', 'Cebiche Muelle 69', 50.00),
('CEV007', 'Cebiche en Cremas', 30.00),
('CEV008', 'Cebiche de Pulpo', 33.00),

-- Arroces y Chaufas
('ARR001', 'Arroz con Mariscos', 28.00),
('ARR002', 'Arroz con Pescado', 28.00),
('ARR003', 'Chaufa con Mariscos', 30.00),
('ARR004', 'Chaufa con Pescado', 30.00),
('ARR005', 'Arroz con Colitas de Camarón', 40.00),

-- Sopas y Sudados
('SUD001', 'Parihuela', 35.00),
('SUD002', 'Chupe de Camarón', 40.00),
('SUD003', 'Sudado de Mariscos', 30.00),
('SUD004', 'Sudado de Pescado (Filete)', 30.00),

-- Pescados a la Parrilla y Fritos
('PES001', 'Pescado a la Menier', 30.00),
('PES002', 'Pescado a lo Macho', 35.00),
('PES003', 'Pescado a la Chorrillana', 30.00),
('PES004', 'Pescado Frito', 28.00),
('PES005', 'Filete de Corvina', 35.00),
('PES006', 'Pescado a la Plancha', 30.00),

-- Chicharrones
('CHI001', 'Chicharron de Pescado', 32.00),
('CHI002', 'Chicharron Mixto (Mariscos + Pescado)', 33.00),
('CHI003', 'Chicharron de Langostino', 40.00),
('CHI004', 'Chicharron de Calamar', 30.00),
('CHI005', 'Chicharron de Pulpo', 33.00),
('CHI006', 'Chicharron de Camarón', 40.00),

-- Especialidades
('ESP001', 'Lapas Arrebosadas', 35.00),
('ESP002', 'Jalea Muelle 69 Chicharron Mixto + Cebiche de Pescado', 45.00),
('ESP003', 'Americano de Pescado y Mariscos', 50.00),

-- Otros Pescados y Mariscos
('OTR001', 'Trucha Frita', 25.00),
('OTR002', 'Cojinova Frita', 35.00),
('OTR003', 'Lenguado al Ajo', 37.00),
('OTR004', 'Lenguado Frito', 35.00),
('OTR005', 'Lenguado a lo Macho', 40.00),
('OTR006', 'Chita Frita', 35.00),
('OTR007', 'Corvinilla Frita', 35.00),

-- Bebidas
('BEB001', 'Inka Cola Personal', 3.00),
('BEB002', 'Inka Cola 1L', 7.00),
('BEB003', 'Coca Cola Personal', 3.00),
('BEB004', 'Coca Cola 1L', 7.00),
('BEB005', 'Agua Sin Gas', 3.00),
('BEB006', 'Agua Con Gas', 3.00),
('BEB007', 'Jarra de Limonada', 12.00),
('BEB008', 'Jarra de Chicha', 12.00),
('BEB009', 'Cerveza Pilsen', 10.00),
('BEB010', 'Cerveza Cusquena Trigo', 11.00),
('BEB011', 'Cerveza Cusquena', 10.00),
('BEB012', 'Cerveza Arequipeña', 10.00),
('BEB013', 'Vino Tinto Copa', 12.00),
('BEB014', 'Vino Blanco Copa', 12.00),
('BEB015', 'Pisco Sour', 15.00);



INSERT INTO Local (ID_Local, Direccion_Local) VALUES
('8513875', 'Av. Lambramani 158');

INSERT INTO Ref_Pago_Comanda (Codigo_Tipo_de_Pago, Nombre_Tipo_Pago) VALUES
('EFE001', 'EFECTIVO'),
('TAR001', 'TARJETA'),
('YAP001', 'YAPE');


INSERT INTO Cierre_Caja (Fecha, Yape_Veri, Efectivo_Veri, Tarjeta_Veri, Total_Veri, Efectivo_Comanda, Tarjeta_Comanda, Yape_Comanda, Total_Comanda) VALUES
('2023-09-28', 210.00, 480.00, 290.00, 980.00, 460.00, 300.00, 220.00, 980.00),
('2023-09-29', 230.00, 510.00, 330.00, 1070.00, 470.00, 320.00, 230.00, 1020.00),
('2023-09-30', 240.00, 520.00, 350.00, 1110.00, 490.00, 330.00, 240.00, 1060.00),
('2023-10-01', 200.00, 500.00, 300.00, 1000.00, 450.00, 320.00, 200.00, 970.00),
('2023-10-02', 180.00, 550.00, 320.00, 1050.00, 520.00, 330.00, 180.00, 1030.00),
('2023-10-03', 210.00, 480.00, 290.00, 980.00, 460.00, 300.00, 220.00, 980.00),
('2023-10-04', 190.00, 600.00, 310.00, 1100.00, 500.00, 320.00, 210.00, 1030.00),
('2023-10-05', 220.00, 530.00, 340.00, 1090.00, 480.00, 310.00, 220.00, 1010.00),
('2023-10-06', 230.00, 510.00, 330.00, 1070.00, 470.00, 320.00, 230.00, 1020.00),
('2023-10-07', 240.00, 520.00, 350.00, 1110.00, 490.00, 330.00, 240.00, 1060.00),
('2023-10-08', 250.00, 530.00, 360.00, 1140.00, 500.00, 340.00, 250.00, 1090.00),
('2023-10-09', 260.00, 540.00, 370.00, 1170.00, 510.00, 350.00, 260.00, 1120.00),
('2023-10-10', 270.00, 550.00, 380.00, 1200.00, 520.00, 360.00, 270.00, 1150.00),
('2023-10-11', 210.00, 550.00, 320.00, 1080.00, 520.00, 330.00, 230.00, 1030.00),
('2023-10-12', 220.00, 500.00, 340.00, 1060.00, 490.00, 320.00, 250.00, 1060.00),
('2023-10-13', 240.00, 530.00, 350.00, 1120.00, 530.00, 340.00, 250.00, 1110.00),
('2023-10-14', 260.00, 520.00, 360.00, 1140.00, 540.00, 330.00, 270.00, 1150.00),
('2023-10-15', 280.00, 560.00, 370.00, 1210.00, 560.00, 350.00, 300.00, 1160.00),
('2023-10-16', 290.00, 580.00, 360.00, 1230.00, 580.00, 360.00, 290.00, 1180.00),
('2023-10-17', 310.00, 550.00, 390.00, 1250.00, 570.00, 350.00, 300.00, 1220.00),
('2023-10-18', 300.00, 600.00, 370.00, 1270.00, 590.00, 360.00, 320.00, 1230.00),
('2023-10-19', 320.00, 610.00, 380.00, 1310.00, 600.00, 370.00, 330.00, 1280.00),
('2023-10-20', 330.00, 620.00, 390.00, 1340.00, 620.00, 390.00, 330.00, 1300.00),
('2023-10-21', 340.00, 630.00, 410.00, 1380.00, 640.00, 390.00, 350.00, 1340.00),
('2023-10-22', 360.00, 650.00, 430.00, 1440.00, 650.00, 410.00, 380.00, 1380.00),
('2023-10-23', 370.00, 660.00, 420.00, 1450.00, 670.00, 400.00, 380.00, 1390.00),
('2023-10-24', 380.00, 670.00, 450.00, 1500.00, 680.00, 420.00, 390.00, 1420.00),
('2023-10-25', 400.00, 680.00, 460.00, 1540.00, 700.00, 430.00, 400.00, 1450.00);


INSERT INTO Comanda (Id_Comanda, Total, Fecha_Cierre_de_Caja) VALUES
('COM1001', 120.00, '2023-09-28'),
('COM1002', 150.00, '2023-09-28'),
('COM1003', 180.00, '2023-09-29'),
('COM1004', 130.00, '2023-09-29'),
('COM1005', 200.00, '2023-09-30'),
('COM1006', 170.00, '2023-09-30'),
('COM0001', 120.00, '2023-10-01'),
('COM0002', 150.00, '2023-10-01'),
('COM0003', 180.00, '2023-10-02'),
('COM0004', 130.00, '2023-10-02'),
('COM0005', 200.00, '2023-10-03'),
('COM0006', 170.00, '2023-10-03'),
('COM0007', 140.00, '2023-10-04'),
('COM0008', 160.00, '2023-10-04'),
('COM0009', 180.00, '2023-10-11'),
('COM0010', 210.00, '2023-10-12'),
('COM0011', 170.00, '2023-10-13'),
('COM0012', 240.00, '2023-10-14'),
('COM0013', 230.00, '2023-10-15'),
('COM0014', 220.00, '2023-10-16'),
('COM0015', 195.00, '2023-10-17'),
('COM0016', 260.00, '2023-10-18'),
('COM0017', 210.00, '2023-10-19'),
('COM0018', 215.00, '2023-10-20'),
('COM0019', 250.00, '2023-10-21'),
('COM0020', 280.00, '2023-10-22'),
('COM0021', 240.00, '2023-10-23'),
('COM0022', 275.00, '2023-10-24'),
('COM0023', 300.00, '2023-10-25');


INSERT INTO Pago_Comanda (ID_Comanda, Codigo_Tipo_de_Pago, Total_Tipo_de_Pago) VALUES
('COM1001', 'EFE001', 60.00),
('COM1001', 'TAR001', 60.00),
('COM1002', 'YAP001', 150.00),
('COM1003', 'EFE001', 100.00),
('COM1003', 'TAR001', 80.00),
('COM1004', 'YAP001', 130.00),
('COM1005', 'EFE001', 120.00),
('COM1005', 'TAR001', 80.00),
('COM0001', 'EFE001', 60.00),
('COM0001', 'TAR001', 60.00),
('COM0002', 'YAP001', 150.00),
('COM0003', 'EFE001', 100.00),
('COM0003', 'TAR001', 80.00),
('COM0004', 'YAP001', 130.00),
('COM0005', 'EFE001', 120.00),
('COM0005', 'TAR001', 80.00),
('COM0006', 'YAP001', 170.00),
('COM0007', 'EFE001', 90.00),
('COM0007', 'TAR001', 50.00),
('COM0008', 'YAP001', 160.00),
('COM0009', 'EFE001', 80.00),
('COM0009', 'TAR001', 100.00),
('COM0010', 'EFE001', 110.00),
('COM0010', 'YAP001', 100.00),
('COM0011', 'TAR001', 70.00),
('COM0011', 'YAP001', 100.00),
('COM0012', 'EFE001', 150.00),
('COM0012', 'TAR001', 90.00),
('COM0013', 'EFE001', 130.00),
('COM0013', 'YAP001', 100.00),
('COM0014', 'TAR001', 120.00),
('COM0014', 'YAP001', 100.00),
('COM0015', 'EFE001', 95.00),
('COM0015', 'YAP001', 100.00),
('COM0016', 'TAR001', 160.00),
('COM0016', 'EFE001', 100.00),
('COM0017', 'EFE001', 110.00),
('COM0017', 'TAR001', 100.00),
('COM0018', 'EFE001', 115.00),
('COM0018', 'YAP001', 100.00),
('COM0019', 'EFE001', 140.00),
('COM0019', 'TAR001', 110.00),
('COM0020', 'EFE001', 150.00),
('COM0020', 'TAR001', 130.00),
('COM0021', 'EFE001', 120.00),
('COM0021', 'TAR001', 120.00),
('COM0022', 'EFE001', 140.00),
('COM0022', 'YAP001', 135.00),
('COM0023', 'EFE001', 160.00),
('COM0023', 'YAP001', 140.00);

INSERT INTO Detalle_Comanda (ID_Comanda, ID_Producto, Cantidad_Producto, Subtotal) VALUES
('COM0001', 'PIQ001', 2, 40.00),
('COM0001', 'CEV001', 1, 28.00),
('COM0001', 'SHT001', 5, 52.00),
('COM0002', 'SHT002', 1, 18.00),
('COM0002', 'CEV003', 2, 60.00),
('COM0002', 'BEB004', 2, 14.00),
('COM0002', 'ARR001', 2, 56.00),
('COM0003', 'ARR001', 1, 28.00),
('COM0003', 'PES001', 1, 30.00),
('COM0003', 'TIR002', 2, 66.00),
('COM0003', 'BEB001', 4, 12.00),
('COM0003', 'CEV002', 1, 30.00),
('COM0003', 'PIQ003', 1, 20.00),
('COM0004', 'TIR001', 1, 30.00),
('COM0004', 'PES002', 2, 70.00),
('COM0004', 'BEB003', 1, 30.00),
('COM0005', 'SUD001', 2, 70.00),
('COM0005', 'CHI001', 2, 64.00),
('COM0005', 'ARR003', 2, 60.00),
('COM0006', 'ESP001', 1, 35.00),
('COM0006', 'OTR001', 1, 25.00),
('COM0006', 'PIQ002', 2, 60.00),
('COM0006', 'CEV004', 1, 50.00),
('COM0007', 'BEB001', 1, 3.00),
('COM0007', 'CEV002', 2, 60.00),
('COM0007', 'ARR005', 1, 40.00),
('COM0007', 'PIQ003', 1, 37.00),
('COM0008', 'BEB004', 2, 14.00),
('COM0008', 'ARR005', 2, 80.00),
('COM0008', 'CHI002', 1, 33.00),
('COM0008', 'CEV005', 1, 33.00),
('COM0009', 'PIQ002', 3, 60.00),
('COM0009', 'BEB002', 2, 20.00),
('COM0010', 'CEV002', 1, 30.00),
('COM0010', 'ARR001', 3, 84.00),
('COM0011', 'TIR001', 2, 60.00),
('COM0011', 'CEV001', 1, 28.00),
('COM0012', 'ARR003', 1, 30.00),
('COM0012', 'CHI004', 2, 60.00),
('COM0013', 'SHT003', 3, 90.00),
('COM0013', 'PES002', 1, 35.00),
('COM0014', 'CHI003', 2, 80.00),
('COM0014', 'OTR006', 1, 35.00),
('COM0015', 'ESP001', 1, 50.00),
('COM0015', 'ARR005', 1, 40.00),
('COM0016', 'CEV003', 1, 30.00),
('COM0016', 'SHT001', 5, 50.00),
('COM0017', 'CEV006', 2, 100.00),
('COM0017', 'ARR004', 2, 60.00),
('COM0018', 'CEV007', 3, 90.00),
('COM0018', 'ARR003', 1, 30.00),
('COM0019', 'PES003', 2, 70.00),
('COM0019', 'PIQ004', 3, 75.00),
('COM0020', 'CHI001', 1, 35.00),
('COM0020', 'TIR002', 1, 33.00),
('COM0021', 'CEV005', 2, 70.00),
('COM0021', 'CHI002', 1, 30.00),
('COM0022', 'ESP002', 2, 90.00),
('COM0022', 'BEB005', 2, 6.00),
('COM0023', 'CHI006', 2, 80.00),
('COM0023', 'ARR002', 3, 84.00);

INSERT INTO Ventas_Tarjetas (Ref_Pago, Num_Tarjetas, Tipo_Tarjeta, Monto_Cobrado) VALUES
('0835', '***4567', 'Visa', 60.00),
('0836', '***5678', 'Visa', 80.00),
('0837', '***6789', 'Visa', 100.00),
('0838', '***7890', 'Visa', 70.00),
('0839', '***8901', 'Visa', 90.00),
('0840', '***9012', 'Visa', 110.00);

INSERT INTO Reporte_Tarjetas (id_cierre_tarjetas, fecha, hora, total_credito, total_debito, total_soles, fecha_cierre_de_caja, id_local) VALUES 
('RT101', '2023-09-28', '18:00:00', 200.00, 100.00, 300.00, '2023-09-28', '8513875'), 
('RT102', '2023-09-29', '18:30:00', 150.00, 130.00, 280.00, '2023-09-29', '8513875'), 
('RT103', '2023-09-30', '17:45:00', 180.00, 120.00, 300.00, '2023-09-30', '8513875'), 
('RT001', '2023-10-01', '18:00:00', 200.00, 100.00, 300.00, '2023-10-01', '8513875'), 
('RT002', '2023-10-02', '18:30:00', 150.00, 130.00, 280.00, '2023-10-02', '8513875'), 
('RT003', '2023-10-03', '17:45:00', 180.00, 120.00, 300.00, '2023-10-03', '8513875'), 
('RT004', '2023-10-04', '19:00:00', 160.00, 140.00, 300.00, '2023-10-04', '8513875'),
('RT005', '2023-10-11', '16:00:00', 220.00, 140.00, 360.00, '2023-10-11', '8513875'), 
('RT006', '2023-10-12', '17:15:00', 180.00, 160.00, 340.00, '2023-10-12', '8513875'), 
('RT007', '2023-10-13', '15:30:00', 210.00, 120.00, 330.00, '2023-10-13', '8513875'), 
('RT008', '2023-10-14', '18:45:00', 250.00, 150.00, 400.00, '2023-10-14', '8513875'), 
('RT009', '2023-10-15', '19:00:00', 270.00, 160.00, 430.00, '2023-10-15', '8513875'), 
('RT010', '2023-10-16', '18:30:00', 260.00, 150.00, 410.00, '2023-10-16', '8513875'), 
('RT011', '2023-10-17', '17:30:00', 230.00, 170.00, 400.00, '2023-10-17', '8513875'), 
('RT012', '2023-10-18', '18:00:00', 280.00, 180.00, 460.00, '2023-10-18', '8513875'), 
('RT013', '2023-10-19', '18:30:00', 300.00, 200.00, 500.00, '2023-10-19', '8513875'), 
('RT014', '2023-10-20', '19:00:00', 290.00, 210.00, 500.00, '2023-10-20', '8513875');


INSERT INTO Pagos_Tarjeta (ID_Cierre_Tarjetas, Ref_Pago) VALUES
('RT001', '0835'),
('RT001', '0836'),
('RT002', '0837'),
('RT002', '0838'),
('RT003', '0839'),
('RT004', '0840'),
('RT005', '0835'),
('RT005', '0836'),
('RT006', '0837'),
('RT006', '0838'),
('RT007', '0839'),
('RT007', '0840'),
('RT008', '0835'),
('RT008', '0836'),
('RT009', '0837'),
('RT010', '0838');



DELIMITER $$

CREATE PROCEDURE RegistrarReporteTarjetas(
    IN p_fecha DATE,
    IN p_hora TIME,
    IN p_total_credito DECIMAL(5,2),
    IN p_total_debito DECIMAL(5,2),
    IN p_total_soles DECIMAL(5,2),
    IN p_fecha_cierre_de_caja DATE,
    IN p_id_local VARCHAR(7)
)
BEGIN
    DECLARE nuevo_id VARCHAR(11);

    -- Calcular el próximo ID basado en el último registro
    SELECT CONCAT('RT', LPAD(COALESCE(MAX(CAST(SUBSTRING(id_cierre_tarjetas, 3) AS UNSIGNED)), 0) + 1, 3, '0'))
    INTO nuevo_id
    FROM reporte_tarjetas;

    -- Insertar el nuevo reporte
    INSERT INTO reporte_tarjetas (
        id_cierre_tarjetas,
        fecha,
        hora,
        total_credito,
        total_debito,
        total_soles,
        fecha_cierre_de_caja,
        id_local
    )
    VALUES (
        nuevo_id,
        p_fecha,
        p_hora,
        p_total_credito,
        p_total_debito,
        p_total_soles,
        p_fecha_cierre_de_caja,
        p_id_local
    );
END$$

DELIMITER ;

DELIMITER $$

-- Obtener tipos de pago
CREATE PROCEDURE ObtenerTiposDePago()
BEGIN
    SELECT codigo_tipo_de_pago, nombre_tipo_pago
    FROM ref_pago_comanda;
END$$

-- Obtener productos
CREATE PROCEDURE ObtenerProductos()
BEGIN
    SELECT id_producto, descripcion_producto, precio_unitario_producto
    FROM producto;
END$$

-- Crear comanda
CREATE PROCEDURE CrearComanda(
    IN p_id_comanda CHAR(8),
    IN p_total DECIMAL(5,2),
    IN p_fecha DATE
)
BEGIN
    INSERT INTO comanda (id_comanda, total, fecha_cierre_de_caja)
    VALUES (p_id_comanda, p_total, p_fecha);
END$$

-- Agregar detalle de comanda
CREATE PROCEDURE AgregarDetalleComanda(
    IN p_id_comanda CHAR(8),
    IN p_id_producto CHAR(6),
    IN p_cantidad INT,
    IN p_subtotal DECIMAL(5,2)
)
BEGIN
    INSERT INTO detalle_comanda (id_comanda, id_producto, cantidad_producto, subtotal)
    VALUES (p_id_comanda, p_id_producto, p_cantidad, p_subtotal);
END$$

-- Registrar pago en comanda
CREATE PROCEDURE RegistrarPagoComanda(
    IN p_id_comanda CHAR(8),
    IN p_codigo_tipo_pago CHAR(6),
    IN p_total_tipo_pago DECIMAL(5,2)
)
BEGIN
    INSERT INTO pago_comanda (id_comanda, codigo_tipo_de_pago, total_tipo_de_pago)
    VALUES (p_id_comanda, p_codigo_tipo_pago, p_total_tipo_pago);
END$$

-- Productos más vendidos
CREATE PROCEDURE ProductosMasVendidos()
BEGIN
    SELECT p.descripcion_producto AS Producto, SUM(dc.cantidad_producto) AS CantidadTotal
    FROM detalle_comanda dc
    JOIN producto p ON dc.id_producto = p.id_producto
    GROUP BY p.descripcion_producto
    ORDER BY CantidadTotal DESC;
END$$

-- Cierres de caja con desajustes
CREATE PROCEDURE CierresCajaDesajustes()
BEGIN
    SELECT fecha, total_veri AS TotalVerificado, total_comanda AS TotalCalculado
    FROM cierre_caja
    WHERE total_veri != total_comanda;
END$$

-- Detalle de productos vendidos por comanda



CREATE PROCEDURE DetalleProductosPorComanda(IN id_comanda_param CHAR(8))
BEGIN
    SELECT 
        p.descripcion_producto AS Producto,
        dc.cantidad_producto AS Cantidad,
        dc.subtotal AS Subtotal
    FROM detalle_comanda dc
    JOIN producto p ON dc.id_producto = p.id_producto
    WHERE dc.id_comanda = id_comanda_param;
END$$


CREATE PROCEDURE CerrarCaja(
    IN fecha_cierre DATE,
    IN yape_verificado DECIMAL(5, 2),
    IN efectivo_verificado DECIMAL(5, 2)
)
BEGIN
    DECLARE total_tarjeta DECIMAL(5, 2);

    -- Calcular el total de tarjetas desde reporte_tarjetas para la fecha
    SELECT COALESCE(SUM(total_soles), 0) INTO total_tarjeta
    FROM reporte_tarjetas
    WHERE fecha = fecha_cierre;

    -- Insertar o actualizar la tabla cierre_caja para la fecha específica
    INSERT INTO cierre_caja (
        fecha, 
        yape_veri, 
        efectivo_veri, 
        tarjeta_veri, 
        total_veri, 
        yape_comanda, 
        efectivo_comanda, 
        tarjeta_comanda, 
        total_comanda
    )
    SELECT 
        fecha_cierre,
        yape_verificado,
        efectivo_verificado,
        total_tarjeta, -- Total de tarjetas obtenido
        yape_verificado + efectivo_verificado + total_tarjeta, -- Total verificado
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'YAP001' THEN total_tipo_de_pago ELSE 0 END), 0), -- Total Yape por comandas
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'EFE001' THEN total_tipo_de_pago ELSE 0 END), 0), -- Total Efectivo por comandas
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'TAR001' THEN total_tipo_de_pago ELSE 0 END), 0), -- Total Tarjeta por comandas
        COALESCE(SUM(total_tipo_de_pago), 0) -- Total por comandas
    FROM pago_comanda
    WHERE id_comanda IN (
        SELECT id_comanda 
        FROM comanda 
        WHERE fecha_cierre_de_caja = fecha_cierre
    )
    GROUP BY fecha_cierre
    ON DUPLICATE KEY UPDATE 
        yape_veri = VALUES(yape_veri),
        efectivo_veri = VALUES(efectivo_veri),
        tarjeta_veri = VALUES(tarjeta_veri),
        total_veri = VALUES(total_veri),
        yape_comanda = VALUES(yape_comanda),
        efectivo_comanda = VALUES(efectivo_comanda),
        tarjeta_comanda = VALUES(tarjeta_comanda),
        total_comanda = VALUES(total_comanda);
END$$


CREATE PROCEDURE ConsultarCierreCaja(IN fecha_consulta DATE)
BEGIN
    SELECT 
        yape_veri AS Yape_Verificado,
        efectivo_veri AS Efectivo_Verificado,
        tarjeta_veri AS Tarjeta_Verificada,
        total_veri AS Total_Verificado,
        yape_comanda AS Yape_Comanda,
        efectivo_comanda AS Efectivo_Comanda,
        tarjeta_comanda AS Tarjeta_Comanda,
        total_comanda AS Total_Comanda
    FROM cierre_caja
    WHERE fecha = fecha_consulta;
END$$


-- Consumo promedio por comanda
CREATE PROCEDURE ConsumoPromedioComanda()
BEGIN
    SELECT AVG(total) AS ConsumoPromedio
    FROM comanda;
END$$


-- Ventas por categoría

CREATE PROCEDURE VentasPorCategoria(IN categoria_nombre VARCHAR(50))
BEGIN
    SELECT p.descripcion_producto AS Producto, 
           SUM(dc.cantidad_producto) AS Cantidad, 
           SUM(dc.subtotal) AS Total
    FROM detalle_comanda dc
    JOIN producto p ON dc.id_producto = p.id_producto
    WHERE p.descripcion_producto LIKE CONCAT(categoria_nombre, '%')
    GROUP BY p.descripcion_producto;
END$$


-- Ventas mensuales totales
CREATE PROCEDURE VentasMensualesTotales()
BEGIN
    SELECT DATE_FORMAT(c.fecha_cierre_de_caja, '%Y-%m') AS Mes, SUM(c.total) AS TotalVentas
    FROM comanda c
    GROUP BY Mes
    ORDER BY Mes;
END$$

-- Tipos de pago por comanda

CREATE PROCEDURE TiposPagoPorComanda(IN comanda_id CHAR(8))
BEGIN
    SELECT r.nombre_tipo_pago AS TipoPago, 
           p.total_tipo_de_pago AS Monto
    FROM pago_comanda p
    JOIN ref_pago_comanda r ON p.codigo_tipo_de_pago = r.codigo_tipo_de_pago
    WHERE p.id_comanda = comanda_id;
END$$


-- Total por método de pago por mes
CREATE PROCEDURE TotalPorMetodoPagoMes()
BEGIN
    SELECT DATE_FORMAT(c.fecha_cierre_de_caja, '%Y-%m') AS Mes, r.nombre_tipo_pago AS TipoPago, SUM(p.total_tipo_de_pago) AS Total
    FROM pago_comanda p
    JOIN comanda c ON p.id_comanda = c.id_comanda
    JOIN ref_pago_comanda r ON p.codigo_tipo_de_pago = r.codigo_tipo_de_pago
    GROUP BY Mes, TipoPago
    ORDER BY Mes, TipoPago;
END$$


CREATE PROCEDURE ConsultarComandasDelDia(IN p_fecha DATE)
BEGIN
    SELECT id_comanda, fecha_cierre_de_caja, total
    FROM comanda
    WHERE fecha_cierre_de_caja = p_fecha;
END$$


CREATE PROCEDURE VerificarOCrearFechaCierreCaja(
    IN p_fecha DATE
)
BEGIN
    -- Verificar si la fecha ya existe en la tabla cierre_caja
    IF NOT EXISTS (SELECT 1 FROM cierre_caja WHERE fecha = p_fecha) THEN
        -- Insertar un registro para esa fecha con valores iniciales
        INSERT INTO cierre_caja (
            fecha, yape_veri, efectivo_veri, tarjeta_veri, total_veri, 
            efectivo_comanda, tarjeta_comanda, yape_comanda, total_comanda
        ) VALUES (p_fecha, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00);
    END IF;
END$$


CREATE PROCEDURE EliminarComanda(IN p_id_comanda CHAR(8))
BEGIN
    -- Elimina los registros relacionados en detalle_comanda
    DELETE FROM detalle_comanda WHERE id_comanda = p_id_comanda;

    -- Elimina los registros relacionados en pago_comanda
    DELETE FROM pago_comanda WHERE id_comanda = p_id_comanda;

    -- Elimina la comanda principal
    DELETE FROM comanda WHERE id_comanda = p_id_comanda;
END$$


CREATE PROCEDURE AgregarProducto(
    IN p_id_producto CHAR(6),
    IN p_descripcion_producto VARCHAR(60),
    IN p_precio_unitario DECIMAL(5,2)
)
BEGIN
    INSERT INTO producto (id_producto, descripcion_producto, precio_unitario_producto)
    VALUES (p_id_producto, p_descripcion_producto, p_precio_unitario);
END$$

CREATE PROCEDURE EliminarProducto(IN p_id_producto CHAR(6))
BEGIN
    DELETE FROM producto WHERE id_producto = p_id_producto;
END$$

CREATE PROCEDURE ActualizarProducto(IN p_id_producto CHAR(6), IN p_descripcion VARCHAR(60), IN p_precio DECIMAL(5,2))
BEGIN
    UPDATE producto
    SET descripcion_producto = p_descripcion, precio_unitario_producto = p_precio
    WHERE id_producto = p_id_producto;
END$$




CREATE PROCEDURE RegistrarOActualizarReporteTarjetas(
    IN p_id_cierre_tarjetas VARCHAR(11),
    IN p_fecha DATE,
    IN p_hora TIME,
    IN p_total_credito DECIMAL(5,2),
    IN p_total_debito DECIMAL(5,2),
    IN p_total_soles DECIMAL(5,2),
    IN p_fecha_cierre_de_caja DATE,
    IN p_id_local VARCHAR(7)
)
BEGIN
    -- Verificar si ya existe un registro para la misma fecha
    IF EXISTS (SELECT 1 FROM reporte_tarjetas WHERE fecha = p_fecha) THEN
        -- Si existe, actualiza los datos del reporte
        UPDATE reporte_tarjetas
        SET 
            id_cierre_tarjetas = p_id_cierre_tarjetas,
            hora = p_hora,
            total_credito = p_total_credito,
            total_debito = p_total_debito,
            total_soles = p_total_soles,
            fecha_cierre_de_caja = p_fecha_cierre_de_caja,
            id_local = p_id_local
        WHERE fecha = p_fecha;
    ELSE
        -- Si no existe, inserta un nuevo reporte
        INSERT INTO reporte_tarjetas (
            id_cierre_tarjetas,
            fecha,
            hora,
            total_credito,
            total_debito,
            total_soles,
            fecha_cierre_de_caja,
            id_local
        ) VALUES (
            p_id_cierre_tarjetas,
            p_fecha,
            p_hora,
            p_total_credito,
            p_total_debito,
            p_total_soles,
            p_fecha_cierre_de_caja,
            p_id_local
        );
    END IF;
END$$



CREATE TRIGGER ActualizarTotalesCierreCaja
AFTER INSERT ON pago_comanda
FOR EACH ROW
BEGIN
    DECLARE total_efectivo DECIMAL(5,2);
    DECLARE total_tarjeta DECIMAL(5,2);
    DECLARE total_yape DECIMAL(5,2);
    DECLARE fecha_cierre DATE;

    -- Obtener la fecha de cierre de la comanda
    SELECT fecha_cierre_de_caja
    INTO fecha_cierre
    FROM comanda
    WHERE id_comanda = NEW.id_comanda;

    -- Calcular los totales desde pago_comanda
    SELECT 
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'EFE001' THEN total_tipo_de_pago ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'TAR001' THEN total_tipo_de_pago ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN codigo_tipo_de_pago = 'YAP001' THEN total_tipo_de_pago ELSE 0 END), 0)
    INTO total_efectivo, total_tarjeta, total_yape
    FROM pago_comanda
    WHERE id_comanda IN (
        SELECT id_comanda
        FROM comanda
        WHERE fecha_cierre_de_caja = fecha_cierre
    );

    -- Actualizar totales en cierre_caja
    UPDATE cierre_caja
    SET 
        efectivo_comanda = total_efectivo,
        tarjeta_comanda = total_tarjeta,
        yape_comanda = total_yape,
        total_comanda = total_efectivo + total_tarjeta + total_yape
    WHERE fecha = fecha_cierre;
END$$


CREATE TRIGGER ValidarTotalesPagoComanda
BEFORE INSERT ON pago_comanda
FOR EACH ROW
BEGIN
    DECLARE total_actual DECIMAL(5,2);

    -- Sumar los pagos existentes de la comanda
    SELECT COALESCE(SUM(total_tipo_de_pago), 0)
    INTO total_actual
    FROM pago_comanda
    WHERE id_comanda = NEW.id_comanda;

    -- Verificar que no exceda el total de la comanda
    IF (total_actual + NEW.total_tipo_de_pago) > (
        SELECT total
        FROM comanda
        WHERE id_comanda = NEW.id_comanda
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El total de los pagos excede el total de la comanda.';
    END IF;
END$$


DELIMITER //

CREATE PROCEDURE ConsultarTotalesPorTipoPago(
    IN fecha_inicio DATE,
    IN fecha_fin DATE
)
BEGIN
    SELECT 
        rpc.nombre_tipo_pago AS `Tipo de Pago`,
        SUM(pc.total_tipo_de_pago) AS `Total`
    FROM 
        pago_comanda pc
    INNER JOIN 
        ref_pago_comanda rpc ON pc.codigo_tipo_de_pago = rpc.codigo_tipo_de_pago
    INNER JOIN 
        comanda c ON pc.id_comanda = c.id_comanda
    WHERE 
        c.fecha_cierre_de_caja BETWEEN fecha_inicio AND fecha_fin
    GROUP BY 
        rpc.nombre_tipo_pago;
END //

DELIMITER ;
