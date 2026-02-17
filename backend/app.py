from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv
from models import db, Doctor, Patient, Chemist, Prescription, Medicine, Order, Admin

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- Config ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-CHANGE-IN-PRODUCTION')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# --- Init ---
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# Allow frontend Authorization headers consistently
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    expose_headers=["Authorization"],
    allow_headers=["Content-Type", "Authorization"]
)

# Debug helper to verify Authorization header reaches the API
@app.before_request
def log_auth_header():
    if request.path.startswith('/api/'):
        auth_header = request.headers.get('Authorization')
        print(f"[auth-debug] {request.method} {request.path} Authorization: {auth_header}")


# ========== HELPER FUNCTIONS ========== #
def get_current_user():
    """Get current user object based on JWT identity"""
    claims = get_jwt()
    role = claims.get('role')
    user_id = int(get_jwt_identity())
    
    model_map = {'doctor': Doctor, 'patient': Patient, 'chemist': Chemist, 'admin': Admin}
    user_model = model_map.get(role)
    
    if user_model:
        return user_model.query.get(user_id), role
    return None, None

# ========== AUTH ROUTES ========== #
@app.route('/api/register/<role>', methods=['POST'])
def register(role):
    """Register a new user (doctor, patient, or chemist)"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'number', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    name = data.get('name')
    email = data.get('email')
    number = data.get('number')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    
    # Check if user already exists
    model_map = {'doctor': Doctor, 'patient': Patient, 'chemist': Chemist}
    user_model = model_map.get(role)
    
    if not user_model:
        return jsonify({'error': 'Invalid role'}), 400
    
    existing_user = user_model.query.filter(
        (user_model.email == email) | (user_model.number == number)
    ).first()
    
    if existing_user:
        return jsonify({'error': 'User with this email or number already exists'}), 400
    
    # Create user based on role
    if role == 'doctor':
        user = Doctor(
            name=name,
            email=email,
            number=number,
            password=password,
            specialization=data.get('specialization')
        )
    elif role == 'patient':
        user = Patient(
            name=name,
            email=email,
            number=number,
            password=password,
            address=data.get('address'),
            date_of_birth=datetime.fromisoformat(data.get('date_of_birth')) if data.get('date_of_birth') else None
        )
    elif role == 'chemist':
        user = Chemist(
            name=name,
            email=email,
            number=number,
            password=password,
            pharmacy_name=data.get('pharmacy_name'),
            address=data.get('address')
        )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': f'{role.capitalize()} registered successfully',
        'user': user.to_dict()
    }), 201


@app.route('/api/login/<role>', methods=['POST'])
def login(role):
    """Login for doctor, patient, chemist, or admin"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    model_map = {'doctor': Doctor, 'patient': Patient, 'chemist': Chemist, 'admin': Admin}
    user_model = model_map.get(role)
    
    if not user_model:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = user_model.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Incorrect password'}), 401

    if role in ['doctor', 'chemist'] and not user.approved:
        return jsonify({'error': 'Account pending admin approval'}), 403
    
    token = create_access_token(identity=str(user.id), additional_claims={'role': role})
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': role
        }
    })


def is_admin():
    claims = get_jwt()
    return claims.get('role') == 'admin'


@app.route('/api/admin/overview', methods=['GET'])
@jwt_required()
def admin_overview():
    """Admin overview of key metrics and recent activity."""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403

    try:
        limit = int(request.args.get('limit', 5))
    except (TypeError, ValueError):
        limit = 5
    limit = max(1, min(limit, 20))

    counts = {
        'doctors': Doctor.query.count(),
        'patients': Patient.query.count(),
        'chemists': Chemist.query.count(),
        'prescriptions': Prescription.query.count(),
        'orders': Order.query.count(),
        'pending_doctors': Doctor.query.filter_by(approved=False).count(),
        'pending_chemists': Chemist.query.filter_by(approved=False).count()
    }

    recent = {
        'doctors': [d.to_dict() for d in Doctor.query.order_by(Doctor.created_at.desc()).limit(limit).all()],
        'patients': [p.to_dict() for p in Patient.query.order_by(Patient.created_at.desc()).limit(limit).all()],
        'chemists': [c.to_dict() for c in Chemist.query.order_by(Chemist.created_at.desc()).limit(limit).all()],
        'prescriptions': [
            p.to_dict(include_relations=True)
            for p in Prescription.query.order_by(Prescription.date.desc()).limit(limit).all()
        ],
        'orders': [
            o.to_dict(include_relations=True)
            for o in Order.query.order_by(Order.created_at.desc()).limit(limit).all()
        ]
    }

    return jsonify({'counts': counts, 'recent': recent})


@app.route('/api/admin/pending', methods=['GET'])
@jwt_required()
def admin_pending():
    """List pending doctors and chemists for approval."""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403

    role = request.args.get('role')
    if role == 'doctor':
        doctors = Doctor.query.filter_by(approved=False).order_by(Doctor.created_at.desc()).all()
        return jsonify({'doctors': [d.to_dict() for d in doctors]})
    if role == 'chemist':
        chemists = Chemist.query.filter_by(approved=False).order_by(Chemist.created_at.desc()).all()
        return jsonify({'chemists': [c.to_dict() for c in chemists]})

    doctors = Doctor.query.filter_by(approved=False).order_by(Doctor.created_at.desc()).all()
    chemists = Chemist.query.filter_by(approved=False).order_by(Chemist.created_at.desc()).all()
    return jsonify({
        'doctors': [d.to_dict() for d in doctors],
        'chemists': [c.to_dict() for c in chemists]
    })


@app.route('/api/admin/approve', methods=['POST'])
@jwt_required()
def admin_approve():
    """Approve a doctor or chemist account."""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    role = data.get('role')
    user_id = data.get('id')
    if role not in ['doctor', 'chemist'] or not user_id:
        return jsonify({'error': 'role and id are required'}), 400

    model_map = {'doctor': Doctor, 'chemist': Chemist}
    user_model = model_map.get(role)
    user = user_model.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.approved = True
    db.session.commit()
    return jsonify({'message': 'User approved', 'user': user.to_dict()})


@app.route('/api/admin/refuse', methods=['POST'])
@jwt_required()
def admin_refuse():
    """Refuse a doctor or chemist account (removes the record)."""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    role = data.get('role')
    user_id = data.get('id')
    if role not in ['doctor', 'chemist'] or not user_id:
        return jsonify({'error': 'role and id are required'}), 400

    model_map = {'doctor': Doctor, 'chemist': Chemist}
    user_model = model_map.get(role)
    user = user_model.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User refused'})


@app.route('/api/me', methods=['GET'])
@jwt_required()
def me():
    """Get current user profile"""
    user, role = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_data = user.to_dict()
    user_data['role'] = role
    return jsonify(user_data)


@app.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    user, role = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json() or {}

    if role == 'doctor':
        allowed_fields = ['name', 'email', 'number', 'specialization']
    elif role == 'patient':
        allowed_fields = ['name', 'email', 'number', 'address', 'date_of_birth']
    elif role == 'chemist':
        allowed_fields = ['name', 'email', 'number', 'pharmacy_name', 'address']
    elif role == 'admin':
        allowed_fields = ['name', 'email']
    else:
        return jsonify({'error': 'Unsupported role'}), 400

    def is_unique(model, field, value, current_id):
        if not value:
            return True
        existing = model.query.filter(getattr(model, field) == value, model.id != current_id).first()
        return existing is None

    if 'email' in data:
        if role == 'admin':
            if not is_unique(Admin, 'email', data.get('email'), user.id):
                return jsonify({'error': 'Email already in use'}), 400
        else:
            model_map = {'doctor': Doctor, 'patient': Patient, 'chemist': Chemist}
            model = model_map.get(role)
            if not is_unique(model, 'email', data.get('email'), user.id):
                return jsonify({'error': 'Email already in use'}), 400

    if 'number' in data and role in ['doctor', 'patient', 'chemist']:
        model_map = {'doctor': Doctor, 'patient': Patient, 'chemist': Chemist}
        model = model_map.get(role)
        if not is_unique(model, 'number', data.get('number'), user.id):
            return jsonify({'error': 'Number already in use'}), 400

    for field in allowed_fields:
        if field not in data:
            continue
        if field == 'date_of_birth':
            value = data.get(field)
            if value:
                try:
                    user.date_of_birth = datetime.fromisoformat(value).date()
                except ValueError:
                    return jsonify({'error': 'Invalid date_of_birth'}), 400
            else:
                user.date_of_birth = None
        else:
            setattr(user, field, data.get(field))

    db.session.commit()

    user_data = user.to_dict()
    user_data['role'] = role
    return jsonify({'message': 'Profile updated', 'user': user_data})


@app.route('/api/forgot', methods=['POST'])
def forgot_password():
    """Placeholder for password reset"""
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    return jsonify({
        'message': 'If an account exists for that email, you will receive reset instructions.'
    })


# ========== DOCTOR ROUTES ========== #
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    doctors = Doctor.query.filter_by(approved=True).all()
    return jsonify([d.to_dict() for d in doctors])


@app.route('/api/patients/search', methods=['GET'])
@jwt_required()
def search_patients():
    """Search patients by email or number (for doctors)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')

    if role != 'doctor':
        return jsonify({'error': 'Only doctors can search patients'}), 403
    
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    patients = Patient.query.filter(
        (Patient.email.contains(query)) | 
        (Patient.number.contains(query)) |
        (Patient.name.contains(query))
    ).limit(10).all()
    
    return jsonify([p.to_dict() for p in patients])


# ========== PRESCRIPTION ROUTES ========== #
@app.route('/api/prescriptions', methods=['POST'])
@jwt_required()
def create_prescription():
    """Create a new prescription (doctors only)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')

    if role != 'doctor':
        return jsonify({'error': 'Only doctors can create prescriptions'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    if not data.get('diagnosis') or not data.get('patient_id'):
        return jsonify({'error': 'Diagnosis and patient_id are required'}), 400
    
    # Create prescription
    new_pres = Prescription(
        date=datetime.utcnow(),
        diagnosis=data.get('diagnosis'),
        notes=data.get('notes'),
        doctor_id=user_id,
        patient_id=data.get('patient_id')
    )
    
    db.session.add(new_pres)
    db.session.flush()  # Get the prescription ID
    
    # Add medicines
    medicines = data.get('medicines', [])
    for med_data in medicines:
        medicine = Medicine(
            name=med_data.get('name'),
            dosage=med_data.get('dosage'),
            frequency=med_data.get('frequency'),
            duration=med_data.get('duration'),
            instructions=med_data.get('instructions'),
            prescription_id=new_pres.id
        )
        db.session.add(medicine)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Prescription created successfully',
        'prescription': new_pres.to_dict(include_relations=True)
    }), 201


@app.route('/api/prescriptions', methods=['GET'])
@jwt_required()
def get_prescriptions():
    """Get prescriptions for current user"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    
    if role == 'doctor':
        pres = Prescription.query.filter_by(doctor_id=user_id).order_by(Prescription.date.desc()).all()
    elif role == 'patient':
        pres = Prescription.query.filter_by(patient_id=user_id).order_by(Prescription.date.desc()).all()
    else:
        return jsonify({'error': 'Unauthorized role'}), 403
    
    return jsonify([p.to_dict(include_relations=True) for p in pres])


@app.route('/api/prescriptions/<int:prescription_id>', methods=['GET'])
@jwt_required()
def get_prescription(prescription_id):
    """Get a specific prescription"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    prescription = Prescription.query.get(prescription_id)
    
    if not prescription:
        return jsonify({'error': 'Prescription not found'}), 404
    
    # Check authorization
    if role == 'doctor' and prescription.doctor_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    elif role == 'patient' and prescription.patient_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(prescription.to_dict(include_relations=True))


@app.route('/api/prescriptions/<int:prescription_id>', methods=['PUT'])
@jwt_required()
def update_prescription(prescription_id):
    """Update a prescription (doctors only)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    if role != 'doctor':
        return jsonify({'error': 'Only doctors can update prescriptions'}), 403
    
    prescription = Prescription.query.get(prescription_id)
    
    if not prescription:
        return jsonify({'error': 'Prescription not found'}), 404
    
    if prescription.doctor_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update prescription fields
    if 'diagnosis' in data:
        prescription.diagnosis = data['diagnosis']
    if 'notes' in data:
        prescription.notes = data['notes']
    if 'status' in data:
        prescription.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Prescription updated successfully',
        'prescription': prescription.to_dict(include_relations=True)
    })


# ========== ORDER ROUTES ========== #
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order (patients only)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')

    if role != 'patient':
        return jsonify({'error': 'Only patients can create orders'}), 403
    
    data = request.get_json()
    
    if not data.get('prescription_id'):
        return jsonify({'error': 'prescription_id is required'}), 400
    
    # Verify prescription belongs to patient
    prescription = Prescription.query.get(data['prescription_id'])
    if not prescription:
        return jsonify({'error': 'Prescription not found'}), 404
    
    if prescription.patient_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Create order
    new_order = Order(
        prescription_id=data['prescription_id'],
        patient_id=user_id,
        chemist_id=data.get('chemist_id'),
        delivery_address=data.get('delivery_address'),
        notes=data.get('notes')
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': new_order.to_dict(include_relations=True)
    }), 201


@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get orders for current user"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    
    if role == 'patient':
        orders = Order.query.filter_by(patient_id=user_id).order_by(Order.created_at.desc()).all()
    elif role == 'chemist':
        # Get all pending orders or orders assigned to this chemist
        orders = Order.query.filter(
            (Order.chemist_id == user_id) | (Order.status == 'pending')
        ).order_by(Order.created_at.desc()).all()
    else:
        return jsonify({'error': 'Unauthorized role'}), 403
    
    return jsonify([o.to_dict(include_relations=True) for o in orders])


@app.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check authorization
    if role == 'patient' and order.patient_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    elif role == 'chemist' and order.chemist_id != user_id and order.status != 'pending':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(order.to_dict(include_relations=True))


@app.route('/api/orders/<int:order_id>/accept', methods=['POST'])
@jwt_required()
def accept_order(order_id):
    """Accept an order (chemists only)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    if role != 'chemist':
        return jsonify({'error': 'Only chemists can accept orders'}), 403
    
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.status != 'pending':
        return jsonify({'error': 'Order is not pending'}), 400
    
    order.chemist_id = user_id
    order.status = 'accepted'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order accepted successfully',
        'order': order.to_dict(include_relations=True)
    })


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (chemists only)"""
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get('role')
    if role != 'chemist':
        return jsonify({'error': 'Only chemists can update order status'}), 403
    
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.chemist_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    valid_statuses = ['accepted', 'preparing', 'ready', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    order.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': 'Order status updated successfully',
        'order': order.to_dict(include_relations=True)
    })


# ========== CHEMIST ROUTES ========== #
@app.route('/api/chemists', methods=['GET'])
def get_chemists():
    """Get all chemists"""
    chemists = Chemist.query.filter_by(approved=True).all()
    return jsonify([c.to_dict() for c in chemists])


# ========== TEST ROUTES ========== #
@app.route('/api/hello')
def hello():
    return jsonify(message="Hello from Flask + SQLite backend!")


@app.route('/api/health')
def health():
    return jsonify(status="healthy", database="connected")


# ========== JWT ERROR HANDLERS ========== #
@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle requests without a valid access token"""
    print(f"[auth-debug] unauthorized_loader: {error}")
    return jsonify({'error': 'Missing or invalid token', 'message': error}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle malformed tokens"""
    print(f"[auth-debug] invalid_token_loader: {error}")
    return jsonify({'error': 'Invalid token', 'message': error}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired tokens"""
    print(f"[auth-debug] expired_token_loader: {jwt_payload}")
    return jsonify({'error': 'Token expired'}), 401


@jwt.needs_fresh_token_loader
def fresh_token_callback(jwt_header, jwt_payload):
    """Handle endpoints that require fresh tokens"""
    print(f"[auth-debug] needs_fresh_token_loader: {jwt_payload}")
    return jsonify({'error': 'Fresh token required'}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Handle revoked tokens"""
    print(f"[auth-debug] revoked_token_loader: {jwt_payload}")
    return jsonify({'error': 'Token revoked'}), 401


# ========== ERROR HANDLERS ========== #
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ========== DATABASE INITIALIZATION ========== #
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command('create_admin')
def create_admin():
    """Create an admin user using ADMIN_EMAIL and ADMIN_PASSWORD."""
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')
    name = os.environ.get('ADMIN_NAME', 'Admin')

    if not email or not password:
        print('Set ADMIN_EMAIL and ADMIN_PASSWORD to create an admin user.')
        return

    existing = Admin.query.filter_by(email=email).first()
    if existing:
        print('Admin user already exists.')
        return

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    admin = Admin(name=name, email=email, password=hashed)
    db.session.add(admin)
    db.session.commit()
    print('Admin user created.')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
