"""Models for Diagnosis tool."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, UniqueConstraint, func
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import UniqueConstraint
# from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect the Flask app to the database."""
    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)

################################################################################################
# Models

# USER AREA

class User(db.Model):
    """Represents a user account for authentication and profile management.

    Supports features such as sign-up, login/logout, and profile customization."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(500), nullable=False, default='/static/uploads/default.jpg')
    
    def __repr__(self):
        """Provide a human-readable representation of a User."""
        return f"<User id={self.id} username={self.username} email={self.email}>"

    @classmethod
    def signup(cls, username, email, first_name, last_name, password, img_url=None):
        """
        Register a new user with a hashed password.

        Args:
            username (str): The user's unique username.
            email (str): The user's unique email address.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            password (str): The user's password to be hashed.
            img_url (str, optional): URL of the user's profile image. Defaults to None.

        Returns:
            User: The newly created User object.
        """

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=hashed_password,
            img_url=img_url if img_url else None  # Ensures None, not "None"
        )

        db.session.add(user)

        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """
        Authenticate a user by username and password.

        Args:
            username (str): The user's username.
            password (str): The user's plaintext password.

        Returns:
            User | None: The authenticated User object if credentials are valid, else None.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password_hash, password)
            if is_auth:
                return user

        return None

################################################################################################
# DSM-5-TR AREA 


class Category(db.Model):
    """
    Represents a diagnostic category in the DSM-5-TR.

    Each category includes multiple disorders and, optionally, clusters (subcategories).
    """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)

    # Relationship to 'Disorder' and 'Cluster'
    disorders = relationship('Disorder', back_populates='category', cascade='all, delete-orphan')
    clusters = relationship('Cluster', back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        """Provide a human-readable representation of a Category."""
        return f"<Category id={self.id}, name={self.name}>"

 
class Disorder(db.Model):
    """
    Represents a specific mental disorder, as defined in the DSM-5-TR.

    Each disorder belongs to a category and, optionally, a cluster.
    """

    __tablename__ = 'disorders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=False)
    description = db.Column(db.Text, nullable=False)
    criteria = db.Column(db.Text, nullable=False)    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('clusters.id', ondelete='SET NULL'), nullable=True)

    # Define relationships for ORM convenience
    category = relationship('Category', back_populates='disorders')
    cluster = relationship('Cluster', back_populates='disorders')
    steps = relationship('Step', back_populates='disorder', cascade='all, delete-orphan')
    disorder_signs = relationship('DisorderSign', back_populates='disorder', cascade='all, delete-orphan')
    disorder_symptoms = relationship('DisorderSymptom', back_populates='disorder', cascade='all, delete-orphan')
    
    def __repr__(self):
        """Provide a human-readable representation of a Disorder."""
        return f"<Disorder id={self.id} name={self.name} category_id={self.category_id} cluster_id={self.cluster_id}>"


class Cluster(db.Model):
    """
    Represents a cluster, a subcategory within a DSM-5-TR category.

    Clusters group related disorders within the same category.
    Each cluster is linked to a parent category and can contain multiple disorders.
    """

    __tablename__ = 'clusters'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    
    # Define relationships for ORM convenience
    category = relationship('Category', back_populates='clusters')
    disorders = relationship('Disorder', back_populates='cluster')

    def __repr__(self):
        """Provide a string representation of a Cluster."""
        return f"<Cluster id={self.id} name={self.name} category_id={self.category_id}>"


class Step(db.Model):
    """
    Represents a diagnostic step for a specific disorder.

    Each step details a part of the diagnostic process required to reach an accurate diagnosis.
    This model is linked to the 'disorders' table, representing the disorder for which the step is defined.
    """

    __tablename__ = 'steps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), nullable=True)  # Allow NULL values

    # Relationship with 'Disorder'
    disorder = db.relationship('Disorder', back_populates='steps')

    def __repr__(self):
        """Provide a string representation of a Step."""
        return f"<Step(step_number={self.step_number}, step_name='{self.step_name}', disorder_id={self.disorder_id})>"

class DifferentialDiagnosis(db.Model):
    """
    Represents potential alternative diagnoses in the process of differential diagnosis.

    Links a primary disorder to other disorders with similar symptoms to aid in ruling out other conditions.
    """
    
    __tablename__ = 'differential_diagnosis'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), nullable=False)
    differential_disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), nullable=True)
    disorder_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    __table_args__ = (
        # UniqueConstraint('disorder_id', 'differential_disorder_id', name='uix_disorder_diff_disorder'),
    )
    
    # Define relationships
    disorder = relationship('Disorder', foreign_keys=[disorder_id], backref='primary_differentials')
    differential_disorder = relationship('Disorder', foreign_keys=[differential_disorder_id], backref='secondary_differentials')
    
    def __repr__(self):
        """Provide a string representation of a DifferentialDiagnosis."""
        return (f"<DifferentialDiagnosis(id={self.id}, disorder_id={self.disorder_id}, "
                f"differential_disorder_id={self.differential_disorder_id}, disorder_name={self.disorder_name})>")

################################################################################################
# PSYCHOPATHOLOGY ITEMS 


class Sign(db.Model):
    """Represents observable clinical signs used in diagnosis.

    Signs are objective indicators of a disorder and can be linked to examples and disorders."""

    __tablename__ = 'signs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Define relationships for ORM convenience
    sign_examples = relationship('SignExample', back_populates='sign', cascade='all, delete-orphan')
    disorder_signs = relationship('DisorderSign', back_populates='sign', cascade='all, delete-orphan')

    def __repr__(self):
        """Provide a string representation of a Sign."""
        return f"<Sign(id={self.id}, name='{self.name}')>"


class SignExample(db.Model):
    """
    Represents an example of a clinical sign.

    Examples provide specific instances or manifestations of a clinical sign.
    """

    __tablename__ = 'sign_examples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.id', ondelete='CASCADE'), nullable=False)
    example = db.Column(db.Text, nullable=False)

    sign = relationship('Sign', back_populates='sign_examples')

    def __repr__(self):
        """Provide a string representation of a SignExample."""
        return f"<SignExample(id={self.id}, sign_id={self.sign_id}, example='{self.example}')>"

   
class Symptom(db.Model):
    """
    Represents subjective symptoms reported by individuals during diagnosis.

    Symptoms are linked to examples and disorders through junction tables.
    """

    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Define relationships for ORM convenience
    symptom_examples = relationship('SymptomExample', back_populates='symptom', cascade='all, delete-orphan')
    disorder_symptoms = relationship('DisorderSymptom', back_populates='symptom', cascade='all, delete-orphan')

    def __repr__(self):
        """Provide a string representation of a Symptom."""
        return f"<Symptom(id={self.id}, name='{self.name}', description='{self.description}')>"


class SymptomExample(db.Model):
    """Represents an example of a clinical symptom.

    Linked to the 'symptoms' model."""

    __tablename__ = 'symptom_examples'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id', ondelete='CASCADE'), nullable=False)
    example = db.Column(db.Text, nullable=False)

    # Relationships
    symptom = relationship('Symptom', back_populates='symptom_examples')

    def __repr__(self):
        """Provide a string representation of a SymptomExample."""
        return f"<SymptomExample(id={self.id}, symptom_id={self.symptom_id}, example='{self.example}')>"


class DisorderSign(db.Model):
    """Junction table linking disorders to signs.

    Represents connections between a specific disorder and its observable signs."""

    __tablename__ = 'disorders_signs'

    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    sign_id = db.Column(db.Integer, db.ForeignKey('signs.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # Relationships to 'disorders' and 'signs'
    disorder = relationship('Disorder', back_populates='disorder_signs')
    sign = relationship('Sign', back_populates='disorder_signs')

    def __repr__(self):
        """Provide a string representation of a DisorderSign."""
        return f"<DisorderSign(disorder_id={self.disorder_id}, sign_id={self.sign_id})>"


class DisorderSymptom(db.Model):
    """Junction table linking disorders to symptoms.

    Represents a connection between a specific disorder and its reported symptoms."""

    __tablename__ = 'disorders_symptoms'

    disorder_id = db.Column(db.Integer, db.ForeignKey('disorders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    # Relationships to 'disorders' and 'symptoms'
    disorder = relationship('Disorder', back_populates='disorder_symptoms')
    symptom = relationship('Symptom', back_populates='disorder_symptoms')

    def __repr__(self):
        """Provide a string representation of a DisorderSymptom."""
        return f"<DisorderSymptom(disorder_id={self.disorder_id}, symptom_id={self.symptom_id})>"


    

    



    






  




















    
    

    
