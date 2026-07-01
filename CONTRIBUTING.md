# 🤝 Contributing to Safety Road

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Report issues privately if needed
- Focus on the code, not the person

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR-USERNAME/pothole-detector.git
cd pothole-detector
```

### 2. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Make Changes

**Frontend (TypeScript)**

- Use functional components
- Add PropTypes or interfaces
- Keep components small & focused

**Backend (Python)**

- Follow PEP 8
- Add type hints
- Write docstrings

### 4. Test Your Changes

```bash
# Frontend
npm test

# Backend
pytest tests/
```

### 5. Commit & Push

```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature
```

### 6. Open Pull Request

- Clear description of changes
- Link to related issues
- Screenshot if UI changes

---

## Contribution Ideas

### 🐛 Bug Fixes

- Fix detection accuracy issues
- Improve error handling
- Optimize performance

### ✨ Features

- Add new severity levels
- Implement batch processing UI
- Add statistical reports

### 📚 Documentation

- Improve setup guide
- Add API examples
- Create tutorials

### 🧪 Testing

- Write unit tests
- Add integration tests
- Improve coverage

---

## Code Guidelines

### Frontend Standards

```typescript
// ✅ Good
interface PotholeMarker {
  id: string;
  severity: 'low' | 'medium' | 'high';
}

const PotholeMarker: React.FC<Props> = ({ data }) => {
  return <View>{/* component */}</View>;
};
```

### Backend Standards

```python
# ✅ Good
def detect_potholes(image: np.ndarray, confidence_threshold: float = 0.5):
    """Detect potholes in image using YOLOv8."""
    pass
```

---

## Reporting Issues

Include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details

---

## Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: resolve bug
docs: update documentation
style: format code
refactor: restructure code
test: add tests
chore: update dependencies
```

---

**Thank you for contributing!** 🙏
