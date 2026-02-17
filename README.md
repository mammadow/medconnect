# MedConnect

A medical prescription management system with separate dashboards for patients, doctors, chemists, and administrators.

## Features

- Patient registration and prescription management
- Doctor prescription creation
- Chemist order fulfillment
- Admin approval system
- JWT authentication
- Multi-language support (i18n)

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

6. **IMPORTANT:** Edit `.env` and set a strong `JWT_SECRET_KEY`:
```
JWT_SECRET_KEY=your-random-secret-key-here
```

7. Initialize the database:
```bash
flask db upgrade
```

8. Run the backend server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Security Notes

- Never commit `.env` files to version control
- Change the `JWT_SECRET_KEY` to a strong random value in production
- The database file (`database.db`) is excluded from git and contains sensitive user data
- Use HTTPS in production
- Update all default credentials before deploying

## Project Structure

```
medconnect/
├── backend/
│   ├── app.py              # Flask application
│   ├── models.py           # Database models
│   ├── requirements.txt    # Python dependencies
│   └── migrations/         # Database migrations
├── frontend/
│   ├── src/
│   │   ├── views/         # Vue components for pages
│   │   ├── components/    # Reusable Vue components
│   │   ├── stores/        # Pinia state management
│   │   ├── router/        # Vue Router configuration
│   │   └── i18n/          # Internationalization
│   └── package.json       # Node dependencies
└── .gitignore
```

## User Roles

- **Patient:** View and manage prescriptions, place medicine orders
- **Doctor:** Create prescriptions for patients
- **Chemist:** View and fulfill medicine orders
- **Admin:** Approve/reject doctor and chemist registrations

## Technologies Used

### Backend
- Flask
- SQLAlchemy
- Flask-Migrate (Alembic)
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-CORS

### Frontend
- Vue 3
- Vue Router
- Pinia (state management)
- Vite
- Vue I18n (internationalization)

## License

This project is for educational purposes.
