-- Crear base de datos
CREATE DATABASE IF NOT EXISTS ouladdb;
USE ouladdb;

-- Tabla: courses
CREATE TABLE IF NOT EXISTS courses (
    code_module VARCHAR(20),
    code_presentation VARCHAR(20),
    module_presentation_length INT,
    PRIMARY KEY (code_module, code_presentation)
);

-- Tabla: studentInfo
CREATE TABLE IF NOT EXISTS studentInfo (
    id_student INT PRIMARY KEY,
    gender VARCHAR(10),
    gender_ord INT,
    final_result VARCHAR(20),
    final_result_ord INT
    -- Puedes agregar más campos si usas versiones enriquecidas
);

-- Tabla: assessments
CREATE TABLE IF NOT EXISTS assessments (
    id_assessment INT PRIMARY KEY,
    code_module VARCHAR(20),
    code_presentation VARCHAR(20),
    assessment_type VARCHAR(20),
    assessment_type_ord INT,
    date INT,
    weight FLOAT,
    FOREIGN KEY (code_module, code_presentation)
        REFERENCES courses(code_module, code_presentation)
);

-- Tabla: studentAssessment
CREATE TABLE IF NOT EXISTS studentAssessment (
    id_assessment INT,
    id_student INT,
    date_submitted INT,
    is_banked TINYINT(1),
    score FLOAT,
    PRIMARY KEY (id_assessment, id_student),
    FOREIGN KEY (id_assessment) REFERENCES assessments(id_assessment),
    FOREIGN KEY (id_student) REFERENCES studentInfo(id_student)
);

-- Tabla: studentRegistration
CREATE TABLE IF NOT EXISTS studentRegistration (
    id_student INT,
    code_module VARCHAR(20),
    code_presentation VARCHAR(20),
    date_registration INT,
    date_unregistration INT,
    PRIMARY KEY (id_student, code_module, code_presentation),
    FOREIGN KEY (id_student) REFERENCES studentInfo(id_student),
    FOREIGN KEY (code_module, code_presentation) REFERENCES courses(code_module, code_presentation)
);

-- Tabla: vle
CREATE TABLE IF NOT EXISTS vle (
    id_site INT PRIMARY KEY,
    code_module VARCHAR(20),
    code_presentation VARCHAR(20),
    activity_type VARCHAR(50),
    week INT,
    FOREIGN KEY (code_module, code_presentation)
        REFERENCES courses(code_module, code_presentation)
);

-- Tabla: studentVle
CREATE TABLE IF NOT EXISTS studentVle (
    code_module VARCHAR(20),
    code_presentation VARCHAR(20),
    id_student INT,
    id_site INT,
    date INT,
    sum_click INT,
    PRIMARY KEY (code_module, code_presentation, id_student, id_site, date),
    FOREIGN KEY (code_module, code_presentation) REFERENCES courses(code_module, code_presentation),
    FOREIGN KEY (id_student) REFERENCES studentInfo(id_student),
    FOREIGN KEY (id_site) REFERENCES vle(id_site)
);

-- Vista FullDomain
DROP VIEW IF EXISTS FullDomain;

CREATE VIEW FullDomain AS
SELECT
    sa.code_module,
    sa.code_presentation,
    sa.id_student,
    sa.id_assessment AS event_id,
    a.assessment_type,
    a.assessment_type_ord,
    a.date AS assessment_date,
    a.weight,
    sa.date_submitted,
    sa.is_banked,
    sa.score,
    NULL AS id_site,
    NULL AS activity_type,
    NULL AS activity_type_ord,
    NULL AS week,
    NULL AS sum_click,
    'ASSESS' AS domain_type,
    si.gender,
    si.final_result
FROM studentAssessment sa
JOIN assessments a USING(id_assessment)
JOIN studentInfo si ON si.id_student = sa.id_student

UNION ALL

SELECT
    sv.code_module,
    sv.code_presentation,
    sv.id_student,
    NULL AS event_id,
    NULL AS assessment_type,
    NULL AS assessment_type_ord,
    NULL AS assessment_date,
    NULL AS weight,
    NULL AS date_submitted,
    NULL AS is_banked,
    NULL AS score,
    sv.id_site,
    v.activity_type,
    NULL AS activity_type_ord,
    v.week,
    sv.sum_click,
    'VLE' AS domain_type,
    si.gender,
    si.final_result
FROM studentVle sv
JOIN vle v ON v.id_site = sv.id_site
    AND v.code_module = sv.code_module
    AND v.code_presentation = sv.code_presentation
JOIN studentInfo si ON si.id_student = sv.id_student;
