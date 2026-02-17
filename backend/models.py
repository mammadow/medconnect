from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Doctor(db.Model):
    __tablename__ = 'doctor'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'email': self.email,
            'number': self.number,
            'approved': self.approved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Patient(db.Model):
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'number': self.number,
            'address': self.address,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Prescription(db.Model):
    __tablename__ = 'prescription'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, fulfilled, cancelled
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Relationships
    medicines = db.relationship('Medicine', backref='prescription', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='prescription', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'diagnosis': self.diagnosis,
            'notes': self.notes,
            'status': self.status,
            'doctor_id': self.doctor_id,
            'patient_id': self.patient_id
        }
        
        if include_relations:
            data['doctor'] = self.doctor.to_dict() if self.doctor else None
            data['patient'] = self.patient.to_dict() if self.patient else None
            data['medicines'] = [m.to_dict() for m in self.medicines]
            
        return data

class Medicine(db.Model):
    __tablename__ = 'medicine'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))  # e.g., "3 times a day"
    duration = db.Column(db.String(50))   # e.g., "7 days"
    instructions = db.Column(db.Text)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'instructions': self.instructions,
            'prescription_id': self.prescription_id
        }

class Chemist(db.Model):
    __tablename__ = 'chemist'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pharmacy_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='chemist', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pharmacy_name': self.pharmacy_name,
            'address': self.address,
            'email': self.email,
            'number': self.number,
            'approved': self.approved,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescription.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    chemist_id = db.Column(db.Integer, db.ForeignKey('chemist.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, preparing, ready, completed, cancelled
    delivery_address = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_relations=False):
        data = {
            'id': self.id,
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'chemist_id': self.chemist_id,
            'status': self.status,
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_relations:
            data['prescription'] = self.prescription.to_dict(include_relations=True) if self.prescription else None
            data['patient'] = self.patient.to_dict() if self.patient else None
            data['chemist'] = self.chemist.to_dict() if self.chemist else None
            
        return data

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
