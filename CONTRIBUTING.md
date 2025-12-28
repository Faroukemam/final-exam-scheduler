# Contributing to Final Exam Scheduler

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues
1. Check if the issue already exists in [GitHub Issues](https://github.com/Faroukemam/final-exam-scheduler/issues)
2. If not, create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version)

### Suggesting Features
1. Open a new issue with `[Feature Request]` prefix
2. Describe the feature and its use case
3. Explain why it would be valuable

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Maintain the layered architecture
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test all affected functionality
   - Ensure no regressions

5. **Commit with descriptive messages**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what changed and why
   - Reference any related issues
   - Wait for review

## 📋 Coding Standards

### Architecture
- Follow the 5-layer architecture:
  - **Models**: Data structures only, no logic
  - **Utils**: Reusable functions, no layer dependencies
  - **Data**: File I/O operations
  - **Business**: Core algorithms and logic
  - **Presentation**: GUI components

### Python Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Naming Conventions
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names (avoid abbreviations)

### File Organization
- Place new models in `models/`
- Place new utilities in `utils/`
- Place business logic in `business/`
- Place GUI components in `presentation/`

## 🧪 Testing Guidelines

While this project doesn't have automated tests yet, please manually test:
- All affected functionality
- Different input scenarios
- Error handling
- GUI responsiveness

## 📝 Documentation

- Update README.md if adding features
- Update CHANGELOG.md with your changes
- Add inline comments for complex algorithms
- Include docstrings for new functions/classes

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 📧 Contact

For questions about contributing:
- Email: farouk.waked@must.edu.eg
- Open a discussion on GitHub

Thank you for contributing! 🎉
