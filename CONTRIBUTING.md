# Contributing to ChurnGuard AI

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Git
- GitHub account

### Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd S84_ChurnGuards_PredictCare

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Setup database
python run_pipeline.py

# Run application
python -m streamlit run streamlit_app.py
```

---

## 🌿 Branch Strategy

### Main Branches
- **`main`** - Production-ready code (protected)
- **`develop`** - Integration branch for features

### Feature Branches
Use descriptive names with prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

**Examples:**
```bash
feature/rag-document-processing
fix/risk-calculation-bug
docs/api-documentation
```

---

## 🔄 Workflow

### 1. Create Feature Branch
```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, readable code
- Follow Python PEP 8 style
- Add comments for complex logic
- Update documentation

### 3. Commit Changes
```bash
# Stage files
git add <files>

# Commit with conventional commit message
git commit -m "feat: add document chunking for RAG pipeline"
```

### 4. Push Branch
```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request
```bash
# Using GitHub CLI
gh pr create --title "feat: Document Chunking" --body "Description..."

# Or manually on GitHub.com
```

### 6. Code Review
- Request review from team members
- Address feedback
- Update PR as needed

### 7. Merge
- Squash and merge to main
- Delete feature branch after merge

---

## 📝 Commit Message Convention

Follow **Conventional Commits** format:

```
<type>: <description>

[optional body]

[optional footer]
```

### Types
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

### Examples
```bash
feat: implement RAG document processing pipeline

fix: correct risk score calculation for renewal dates

docs: update README with RAG setup instructions

refactor: extract embedding logic into separate module

test: add unit tests for chunking strategies
```

---

## 🧪 Testing

### Before Committing
```bash
# Run tests
python -m pytest tests/

# Check database integrity
python verify_database.py

# Lint code (optional)
flake8 streamlit_app.py
```

---

## 📋 Pull Request Template

When creating a PR, include:

**Title:** `feat: Brief description`

**Description:**
```markdown
## Summary
Brief description of changes

## Changes
- ✅ Change 1
- ✅ Change 2

## Testing
- ✅ Test scenario 1
- ✅ Test scenario 2

## Module
Module X.XX - Topic Name

## Screenshots (if UI changes)
[Add screenshots]
```

---

## 🎨 Code Style

### Python
- Follow PEP 8
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use type hints where helpful
- Add docstrings to functions

### Example
```python
def calculate_risk_score(customer_id: int, tickets_df: pd.DataFrame) -> int:
    """
    Calculate customer churn risk score.
    
    Args:
        customer_id: Unique customer identifier
        tickets_df: DataFrame containing support tickets
        
    Returns:
        Risk score from 0-100
    """
    # Implementation
    pass
```

---

## 🔒 Security

### Never Commit
- ❌ API keys
- ❌ Passwords
- ❌ `.env` files
- ❌ Database files (except for small test DBs)
- ❌ Personal credentials

### Always Use
- ✅ `.env.example` for templates
- ✅ Environment variables for secrets
- ✅ `.gitignore` to exclude sensitive files

---

## 📞 Getting Help

### Questions?
- Create an issue on GitHub
- Ask in team chat
- Review existing documentation

### Found a Bug?
1. Check if issue already exists
2. Create new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

---

## 👥 Team

- **Akshit Sharma**
- **Arman Singh**
- **Saksham Kaushal**

---

## ✅ Checklist Before PR

- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No console errors
- [ ] `.env.example` updated if new variables added
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main

---

**Thank you for contributing to ChurnGuard AI! 🎉**
