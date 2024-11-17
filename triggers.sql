-- Trigger para validar que las horas de los turnos sean correctas.
CREATE TRIGGER turnos_insert
BEFORE INSERT ON turnos
FOR EACH ROW
BEGIN
	IF NEW.hora_inicio >= NEW.hora_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La hora de inicio debe ser menor que hora de finalizar';
    END IF;
END;

CREATE TRIGGER turnos_update
BEFORE UPDATE ON turnos
FOR EACH ROW
BEGIN
    IF NEW.hora_inicio >= NEW.hora_fin THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La hora de inicio debe ser menor que la hora de fin.';
    END IF;
END;

-- Trigger para evitar que dos instructores den clases en el mismo turno.
CREATE TRIGGER instructor
BEFORE INSERT ON clase
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM clase
        WHERE ciInstructor = NEW.ciInstructor AND idTurno = NEW.idTurno
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Un instructor no puede dar dos clases en el mismo turno.';
    END IF;
END;

-- Trigger para evitar que un alumno se inscriba en dos clases diferentes en el mismo turno.
CREATE TRIGGER alumno_clase
BEFORE INSERT ON alumno_clase
FOR EACH ROW
BEGIN
    DECLARE turno_inscrito INT;

    SELECT idTurno INTO turno_inscrito
    FROM clase
    WHERE idClase = NEW.idClase;

    IF EXISTS (
        SELECT 1
        FROM alumno_clase ac
        JOIN clase c ON ac.idClase = c.idClase
        WHERE ac.ciAlumno = NEW.ciAlumno AND c.idTurno = turno_inscrito
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El alumno ya está inscrito en una clase en este turno.';
    END IF;
END;

-- Trigger para verificar la restricción de edad antes de inscribir al alumno.
CREATE TRIGGER restriccion_edad
BEFORE INSERT ON alumno_clase
FOR EACH ROW
BEGIN
    DECLARE restriccion_edad INT;
    DECLARE fecha_nacimiento DATE;
    DECLARE edad_alumno INT;

    SELECT a.restriccionEdad INTO restriccion_edad
    FROM actividades a
    JOIN clase c ON c.idActividad = a.idActividad
    WHERE c.idClase = NEW.idClase;

    SELECT fecha_nacimiento INTO fecha_nacimiento
    FROM alumnos
    WHERE ciAlumno = NEW.ciAlumno;

    SET edad_alumno = TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE());

    IF edad_alumno < restriccion_edad THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El alumno no cumple con la restricción de edad para la actividad.';
    END IF;
END;

-- Trigger para que no se puedan modificar ni eliminar clases durante su horario.
CREATE TRIGGER clase_update
BEFORE UPDATE ON clase
FOR EACH ROW
BEGIN
    DECLARE hora_actual TIME;

    SET hora_actual = CURRENT_TIME;

    IF EXISTS (
        SELECT 1
        FROM turnos
        WHERE idTurno = NEW.idTurno
          AND hora_actual BETWEEN hora_inicio AND hora_fin
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede modificar la clase durante su horario.';
    END IF;
END;

CREATE TRIGGER clase_delete
BEFORE DELETE ON clase
FOR EACH ROW
BEGIN
    DECLARE hora_actual TIME;

    SET hora_actual = CURRENT_TIME;

    IF EXISTS (
        SELECT 1
        FROM turnos
        WHERE idTurno = OLD.idTurno
          AND hora_actual BETWEEN hora_inicio AND hora_fin
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede eliminar la clase durante su horario.';
    END IF;
END;

-- Trigger para que no se puedan agregar o quitar alumnos durante el horario de la clase.
CREATE TRIGGER alumno_clase_update
BEFORE INSERT ON alumno_clase
FOR EACH ROW
BEGIN
    DECLARE hora_actual TIME;

    SET hora_actual = CURRENT_TIME;

    IF EXISTS (
        SELECT 1
        FROM clase c
        JOIN turnos t ON c.idTurno = t.idTurno
        WHERE c.idClase = NEW.idClase
          AND hora_actual BETWEEN t.hora_inicio AND t.hora_fin
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se pueden agregar alumnos durante el horario de la clase.';
    END IF;
END;

CREATE TRIGGER alumno_clase_delete
BEFORE DELETE ON alumno_clase
FOR EACH ROW
BEGIN
    DECLARE hora_actual TIME;

    SET hora_actual = CURRENT_TIME;

    IF EXISTS (
        SELECT 1
        FROM clase c
        JOIN turnos t ON c.idTurno = t.idTurno
        WHERE c.idClase = OLD.idClase
          AND hora_actual BETWEEN t.hora_inicio AND t.hora_fin
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se pueden quitar alumnos durante el horario de la clase.';
    END IF;
END;