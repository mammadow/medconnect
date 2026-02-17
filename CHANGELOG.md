# Changelog

All notable changes to the MedConnect project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- MIT License
- Contributing guidelines (CONTRIBUTING.md)
- Docker support with docker-compose setup
- EditorConfig for consistent code formatting
- Nginx configuration for frontend deployment
- This CHANGELOG file

## [1.0.0] - 2026-02-17

### Added
- Initial release of MedConnect
- Patient registration and authentication
- Doctor registration and prescription creation
- Chemist registration and order management
- Admin approval system for doctors and chemists
- JWT-based authentication
- Multi-language support (i18n)
- Responsive Vue 3 frontend
- Flask REST API backend
- SQLite database with migrations
- User roles: Patient, Doctor, Chemist, Admin
- Prescription management system
- Medicine order fulfillment workflow

### Security
- Bcrypt password hashing
- JWT token authentication
- CORS configuration
- Environment variable support for sensitive data

## Release Notes

### Version 1.0.0
First stable release of MedConnect medical prescription management system. Includes full authentication system, role-based dashboards, and prescription workflow from creation to order fulfillment.

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
