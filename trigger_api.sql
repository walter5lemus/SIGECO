-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.7.9 - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Volcando estructura para disparador sigec.trig_after_insert_expediente
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_ALL_TABLES,NO_AUTO_CREATE_USER';
DELIMITER //
CREATE TRIGGER `trig_after_insert_expediente` AFTER INSERT ON `pacientes_alumno` FOR EACH ROW BEGIN
declare cod_exp int;
select IFNULL(max(cod_expediente), 0) into cod_exp from pacientes_expediente;


insert into pacientes_expediente (cod_expediente,responsable,telefono,fecha_hora_creacion,alumno_id)
values (cod_exp+1,new.responsable,new.telefono,new.fecha_hora_creacion,new.id);
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;


-- Volcando estructura para disparador sigec.trig_after_update_expediente
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_ALL_TABLES,NO_AUTO_CREATE_USER';
DELIMITER //
CREATE TRIGGER `trig_after_update_expediente` AFTER UPDATE ON `pacientes_alumno` FOR EACH ROW BEGIN

update pacientes_expediente set responsable=new.responsable,telefono=new.telefono where alumno_id=old.id;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
