-- USER AREA

-- user sign-up, login/logout purposes only
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    img_url VARCHAR(500) DEFAULT '/static/uploads/default.jpg'
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DSM-5-TR AREA 

-- Provides an introduction to what the DSM-5 is, what it is for, sections, and general use
-- MOVE THIS COMMENT TO THE ROUTE --> SECTION II WILL HAVE A HYPERLINK (NOT THROUGH THE TABLE, JUST ON THE FRONTEND)
-- I'M REMOVING THIS TABLE BECAUSE I'M NOT GOING TO USE IT CONSIDERING THE INFO IT'S GOING TO BE STATIC AND NEVER DYNAMIC (FOR THE CAPSTONE PURPOSES).
-- CREATE TABLE dsm (
--     id SERIAL PRIMARY KEY,
--     manual_info TEXT NOT NULL,
--     sections TEXT NOT NULL
-- )

-- Categories description (each category contains several disorders). 
-- Referenced by the tables: 'disorders', and 'clusters'. Some categories have "clusters" (they group some disorders of the category into a sub-category).
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE, 
    description TEXT NOT NULL
);

-- For those categories which have sub-groups of disorders.
-- References table: 'categories' 
CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Describes disorders, and it's a diagnosis.
-- It references tables: 'categories', and 'clusters'.
-- It's referenced by the tables: 'steps', 'disorders_signs', 'disorders_symptoms', and 'differential_diagnosis'.
CREATE TABLE disorders (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    criteria TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    cluster_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (cluster_id) REFERENCES clusters(id) ON DELETE SET NULL
);


-- Describes the steps of the diagnostic process.
-- References 'disorders'.
CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    step_number INTEGER NOT NULL,
    step_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    disorder_id INTEGER NULL,  -- Allow NULL values for this version
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    -- Change UNIQUE constraints to include only non-NULL `disorder_id`
    -- UNIQUE (disorder_id, step_number) WHERE disorder_id IS NOT NULL,
    -- UNIQUE (disorder_id, step_name) WHERE disorder_id IS NOT NULL
    CONSTRAINT unique_step_number UNIQUE (disorder_id, step_number),
    CONSTRAINT unique_step_name UNIQUE (disorder_id, step_name)

);

-- Junction table - References 'disorders'.
CREATE TABLE differential_diagnosis (
    id SERIAL PRIMARY KEY,
    disorder_id INTEGER NOT NULL,
    differential_disorder_id INTEGER,
    disorder_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    FOREIGN KEY (differential_disorder_id) REFERENCES disorders(id) ON DELETE CASCADE
);



-- PSYCHOPATHOLOGY ITEMS (Present in the DSM-5-TR)

-- Referenced by 'sign_examples', and 'disorders_signs'
CREATE TABLE signs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL
);

-- Provides examples of a sign
--  References 'signs'
CREATE TABLE sign_examples (
    id SERIAL PRIMARY KEY,
    sign_id INTEGER NOT NULL,
    example TEXT NOT NULL,
    FOREIGN KEY (sign_id) REFERENCES signs(id) ON DELETE CASCADE
);

-- Referenced by 'symptom_examples', and 'disorders_symptoms'.
CREATE TABLE symptoms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL
);

-- Provides examples of a symptom.
-- References 'symptoms'
CREATE TABLE symptom_examples (
    id SERIAL PRIMARY KEY,
    symptom_id INTEGER NOT NULL,
    example TEXT NOT NULL,
    FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
);

-- Junction table - References 'disorders', and 'signs'
CREATE TABLE disorders_signs (
    disorder_id INTEGER NOT NULL,
    sign_id INTEGER NOT NULL,
    PRIMARY KEY (disorder_id, sign_id),
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    FOREIGN KEY (sign_id) REFERENCES signs(id) ON DELETE CASCADE
);

-- Junction table - References 'disorders', and 'symptoms'
CREATE TABLE disorders_symptoms (
    disorder_id INTEGER NOT NULL,
    symptom_id INTEGER NOT NULL,
    PRIMARY KEY (disorder_id, symptom_id),
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
);

