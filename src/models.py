"""Models for Diagnosis tool."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, UniqueConstraint, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)

# Models

# USER AREA

# User sign-up, login/logout purposes only 
class User(db.Model):
    """User sign-up, login/logout purposes only."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(500), nullable=True, default="static/images/default-pic.png")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"

    # Register new user
    @classmethod
    def signup(cls, username, email, first_name, last_name, password, img_url=None):
        """Register user w/hashed password & return user."""
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password,
            img_url=img_url or "static/images/default-pic.png"
        )

        db.session.add(user)

        return user
    
    # User authentication and sign-in
    @classmethod
    def authenticate(cls, username, password):
        """Find user with username and password."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password_hash, password)
            if is_auth:
                return user

        return False

# DSM-5-TR AREA 

# Introduction to what the DSM-5 is.
# MOVE THIS COMMENT TO THE ROUTE --> SECTION II WILL HAVE A HYPERLINK (NOT THROUGH THE TABLE, JUST ON THE FRONTEND)
class DSM(db.Model):
    """Provides an introduction to what the DSM-5 is, what it is for, sections, and general use."""

    __tablename__ = 'dsm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manual_info = db.Column(db.Text, nullable=False)
    sections = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<DSM id={self.id}, sections={self.sections}>"

# Categories description
class Category(db.Model):
    """
    Categories description: Each category has several disorders.
    
    Referenced by the tables:'disorders', and 'clusters'. 
    
    Some categories have "clusters" (they group some disorders of the category into a sub-category). 
    """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    # Relationship to 'Disorder' and 'Cluster'
    disorders = relationship('Disorder', back_populates='category', cascade='all, delete-orphan')
    clusters = relationship('Cluster', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category id={self.id}, name={self.name}>"

# Describes disorders (it's also a diagnosis)
class Disorder(db.Model):
    """
    Represents a specific disorder in the diagnosis process. Each disorder belongs to a category and, optionally, a cluster (sub-category).

    It references the tables: 'categories', and 'clusters'.

    It's referenced by the tables: 'steps', 'disorders_signs', 'disorders_symptoms', and 'differential_diagnosis'.
    """

    __tablename__ = 'disorders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    criteria = db.Column(db.Text, nullable=False)    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id', ondelete='SET NULL'), nullable=True)

    # Define relationships for ORM convenience
    category = relationship('Category', back_populates='disorders')
    cluster = relationship('Cluster', back_populates='disorders')
    step = relationship('Step', back_populates='disorders')
    disorder_signs = relationship('DisorderSign', back_populates='disorder', cascade='all, delete-orphan')
    disorder_symptoms = relationship('DisorderSymptom', back_populates='disorder', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Disorder id={self.id} name={self.name} category_id={self.category_id} cluster_id={self.cluster_id}>"

# For those categories that have sub-groups of disorders
class Cluster(db.Model):
    """References table: 'categories'."""

    __tablename__ = 'clusters'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    
    # Define relationships for ORM convenience
    category = relationship('Category', back_populates='clusters')
    disorders = relationship('Disorder', back_populates='cluster')

    def __repr__(self):
        return f"<Cluster id={self.id} name={self.name} category_id={self.category_id}>"

# Describes the steps of the diagnostic process
class Step(db.Model):
    """Represents a step in the diagnostic process for a disorder. Each step outlines part of the process needed to reach an accurate diagnosis.
    
    References 'disorders'."""

    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), nullable=False)

    # Unique constraints for 'step_number' and 'step_name' per disorder
    __table_args__ = (
        UniqueConstraint('disorder_id', 'step_number', name='uq_disorder_step_number'),
        UniqueConstraint('disorder_id', 'step_name', name='uq_disorder_step_name'),
    )

    def __repr__(self):
        return f"<Step(step_number={self.step_number}, step_name='{self.step_name}', disorder_id={self.disorder_id})>"
    
# List of potential diagnoses used to rule out other conditions and determine the final diagnosis.
class DifferentialDiagnosis(db.Model):
    """Represents the process of differential diagnosis. Links a disorder to potential alternative diagnoses, helping healthcare professionals rule out other conditions with similar symptoms.

    Junction table - References 'disorders'."""

    __tablename__ = 'differential_diagnosis'

    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    differential_disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<DifferentialDiagnosis(disorder_id={self.disorder_id}, differential_disorder_id={self.differential_disorder_id})>"


# PSYCHOPATHOLOGY ITEMS (Present in the DSM-5-TR)

# Referenced by 'sign_examples', and 'disorders_signs'.
class Sign(db.Model):
    """Represents observable signs used in diagnoses. Signs are objective indicators of a disorder and are linked to specific examples and disorders."""

    __tablename__ = 'signs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    # Define relationships for ORM convenience
    sign_examples = relationship('SignExample', back_populates='signs', cascade='all, delete-orphan')
    disorder_signs = relationship('DisorderSign', back_populates='sign', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Sign(id={self.id}, name='{self.name}')>"

# Provides examples of a sign
class SignExample(db.Model):
    """Provides examples of a sign. References 'signs'."""

    __tablename__ = 'sign_examples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.id', ondelete='CASCADE'), nullable=False)
    example = db.Column(db.Text, nullable=False)

    sign = relationship('Sign', back_populates='sign_examples')

    def __repr__(self):
        return f"<SignExample(id={self.id}, sign_id={self.sign_id}, example='{self.example}')>"

# Referenced by 'symptom_examples', and 'disorders_symptoms'.   
class Symptom(db.Model):
    """Represents subjective symptoms reported by individuals. Symptoms are associated with specific examples and linked to disorders."""

    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    # Define relationships for ORM convenience
    symptom_examples = relationship('SymptomExample', back_populates='symptom', cascade='all, delete-orphan')
    disorder_symptoms = relationship('DisorderSymptom', back_populates='symptom', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Symptom(id={self.id}, name='{self.name}', description='{self.description}')>"

# Provides examples of a symptom.
class SymptomExample(db.Model):
    """Provides examples of a symptom. References 'symptoms'."""

    __tablename__ = 'symptom_examples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id', ondelete='CASCADE'), nullable=False)
    example = db.Column(db.Text, nullable=False)

    symptom = relationship('Symptom', back_populates='symptom_examples')

    def __repr__(self):
        return f"<SymptomExample(id={self.id}, symptom_id={self.symptom_id}, example='{self.example}')>"


# JUNCTION TABLES for signs, symptoms and disorders

# Junction table - References 'disorders', and 'signs'
class DisorderSign(db.Model):
    """Junction table connecting disorders to signs. Each record links a specific disorder to its associated signs (observable indicators)."""

    __tablename__ = 'disorders_signs'

    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # Relationships to 'disorders' and 'signs'
    disorder = relationship('Disorder', back_populates='disorder_signs')
    sign = relationship('Sign', back_populates='disorder_signs')

    def __repr__(self):
        return f"<DisorderSign(disorder_id={self.disorder_id}, sign_id={self.sign_id})>"


# Junction table - References 'disorders', and 'symptoms'.
class DisorderSymptom(db.Model):
    """Junction table connecting disorders to symptoms. Each record links a specific disorder to its associated symptoms (reported subjective experiences)."""

    __tablename__ = 'disorders_symptoms'

    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # Relationships to 'disorders' and 'symptoms'
    disorder = relationship('Disorder', back_populates='disorder_symptoms')
    symptom = relationship('Symptom', back_populates='disorder_symptoms')

    def __repr__(self):
        return f"<DisorderSymptom(disorder_id={self.disorder_id}, symptom_id={self.symptom_id})>"


    

    



    






  




















    
    

    
