-- USER AREA

-- Table for user account management (sign-up, login/logout).
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    img_url VARCHAR(500) DEFAULT 'uploads/default.jpg'
); 

-- DSM AREA

-- Table for DSM categories, each containing multiple disorders.
-- Referenced by 'disorders' and 'clusters'.
-- Some categories may group disorders into "clusters" (subcategories).
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE, 
    description TEXT NOT NULL
);

-- A subcategory type
-- References the 'categories' table.
CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Table for DSM disorders.
-- References 'categories' and optionally 'clusters'.
-- Referenced by 'steps', 'disorders_signs', 'disorders_symptoms', and 'differential_diagnosis'.
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

-- Table for diagnostic steps.
-- References 'disorders'.
CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    step_number INTEGER NOT NULL,
    step_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    disorder_id INTEGER NULL,  -- Allow NULL values for this version of the app
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
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



-- PSYCHOPATHOLOGY ITEMS 

-- Table for defining DSM signs (observable clinical features).
-- Referenced by 'disorders_signs'.
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

-- Table for defining DSM symptoms (reported clinical features).
-- Referenced by 'disorders_symptoms'.
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

-- Junction table linking disorders and signs.
CREATE TABLE disorders_signs (
    disorder_id INTEGER NOT NULL,
    sign_id INTEGER NOT NULL,
    PRIMARY KEY (disorder_id, sign_id),
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    FOREIGN KEY (sign_id) REFERENCES signs(id) ON DELETE CASCADE
);

-- Junction table linking disorders and symptoms.
CREATE TABLE disorders_symptoms (
    disorder_id INTEGER NOT NULL,
    symptom_id INTEGER NOT NULL,
    PRIMARY KEY (disorder_id, symptom_id),
    FOREIGN KEY (disorder_id) REFERENCES disorders(id) ON DELETE CASCADE,
    FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
);

