# Contributing to MedConnect

Thank you for considering contributing to MedConnect! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, browser, Python version, Node version)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install dependencies**:
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`
3. **Make your changes**:
   - Write clear, concise commit messages
   - Follow the existing code style
   - Add comments for complex logic
4. **Test your changes**:
   - Ensure the backend runs without errors
   - Test all affected features in the frontend
   - Check for console errors
5. **Update documentation** if needed (README, code comments)
6. **Submit a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots for UI changes

## Development Guidelines

### Code Style

**Python (Backend)**:
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small

**JavaScript/Vue (Frontend)**:
- Use Vue 3 Composition API where possible
- Follow Vue style guide
- Use meaningful component names
- Keep components modular and reusable

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add patient medicine order history
Fix prescription date formatting bug
Update doctor dashboard layout
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## Project Structure

```
medconnect/
├── backend/           # Flask API
│   ├── app.py        # Main application
│   ├── models.py     # Database models
│   └── migrations/   # Database migrations
├── frontend/         # Vue 3 application
│   └── src/
│       ├── views/    # Page components
│       ├── components/ # Reusable components
│       ├── stores/   # Pinia state management
│       └── router/   # Routing configuration
```

## Setting Up Development Environment

1. Clone your fork
2. Set up backend (see README.md)
3. Set up frontend (see README.md)
4. Create `.env` files from `.env.example`
5. Initialize database: `flask db upgrade`

## Testing

Before submitting a PR:
- Test all user roles (patient, doctor, chemist, admin)
- Verify authentication flows
- Check responsive design
- Test in different browsers

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
