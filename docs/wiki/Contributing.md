# Contributing

Guide for contributing to Bambu Farm Monitor.

## Welcome Contributors!

Thank you for your interest in contributing to Bambu Farm Monitor! This guide will help you get started with contributing code, documentation, bug reports, and feature requests.

## Ways to Contribute

### 1. Report Bugs

**Before Reporting:**
- Search [existing issues](https://github.com/neospektra/bambu-farm-monitor/issues) to avoid duplicates
- Check [Common Issues](Common-Issues.md) to see if it's a known problem
- Verify you're running the latest version

**What to Include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Docker version, browser)
- Logs and screenshots
- Configuration (remove sensitive info)

**Example Bug Report:**
```markdown
**Describe the bug**
Video stream shows black screen for Printer 2, but Printer 1 works fine.

**To Reproduce**
1. Add two printers with same access code
2. Start container
3. Access web UI
4. Printer 1 video works, Printer 2 is black

**Expected behavior**
Both printers should show video streams.

**Environment**
- OS: Ubuntu 22.04
- Docker: 24.0.5
- Browser: Chrome 120
- Bambu Farm Monitor: 3.3.9

**Logs**
```
[logs here]
```

**Screenshots**
[attach screenshot]
```

### 2. Suggest Features

**Before Suggesting:**
- Search [existing discussions](https://github.com/neospektra/bambu-farm-monitor/discussions) and issues
- Check [planned features](#future-roadmap)
- Consider if it fits project scope

**What to Include:**
- Clear description of the feature
- Use case and motivation
- Potential implementation approach
- UI/UX mockups if applicable
- Willingness to help implement

**Example Feature Request:**
```markdown
**Feature Request: Dark Mode**

**Description**
Add a dark theme option to reduce eye strain when monitoring at night.

**Motivation**
Many users monitor printers overnight and find the bright UI distracting.

**Proposed Implementation**
- Toggle in Settings
- Save preference to localStorage
- CSS variables for theming
- Match system theme by default

**I can help with:**
- CSS implementation
- Testing across browsers
```

### 3. Improve Documentation

**Documentation Needs:**
- Fix typos and grammar
- Add missing information
- Improve clarity
- Add examples and screenshots
- Translate to other languages

**Where Documentation Lives:**
- `/docs/wiki/*.md` - Wiki articles
- `/README.md` - Main documentation
- Code comments - Inline documentation

**How to Contribute Documentation:**
1. Fork the repository
2. Create branch: `docs/your-improvement`
3. Make changes to markdown files
4. Submit pull request
5. Describe your changes

**Example:**
```markdown
**Documentation PR: Add QNAP Troubleshooting**

**Changes:**
- Added common QNAP Container Station errors
- Included screenshots of port configuration
- Added solution for volume permission issues

**Testing:**
Tested on QNAP TS-464 with DSM 7.0
```

### 4. Submit Code

**Development Setup:**
See [Development Setup](#development-setup) below.

**Code Guidelines:**
- Follow existing code style
- Add comments for complex logic
- Write meaningful commit messages
- Update documentation
- Test thoroughly

**Pull Request Process:**
1. Fork the repository
2. Create feature branch
3. Make your changes
4. Test locally
5. Update documentation
6. Submit pull request
7. Address review feedback

## Development Setup

### Prerequisites

**Required:**
- Git
- Docker (for testing container)
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- Text editor/IDE

**Recommended:**
- VS Code with extensions:
  - Python
  - ESLint
  - Prettier
  - Docker
- Bambu Lab printer (for testing)

### Clone Repository

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/bambu-farm-monitor.git
cd bambu-farm-monitor

# Add upstream remote
git remote add upstream https://github.com/neospektra/bambu-farm-monitor.git

# Create branch
git checkout -b feature/your-feature-name
```

### Frontend Development

**Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Opens http://localhost:3000
```

**Structure:**
```
frontend/
├── public/          # Static files
├── src/
│   ├── components/  # React components
│   ├── services/    # API services
│   ├── utils/       # Utilities
│   ├── App.js       # Main app
│   └── index.js     # Entry point
├── package.json
└── README.md
```

**Key Files:**
- `src/App.js` - Main dashboard
- `src/components/PrinterCard.js` - Printer display
- `src/components/Settings.js` - Settings panel
- `src/services/api.js` - API calls
- `src/services/layout.js` - Layout management

**Development:**
```bash
# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

### Backend Development

**Setup:**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run development server
python app.py

# Runs on http://localhost:5000 (Config API)
# And http://localhost:5001 (Status API)
```

**Structure:**
```
backend/
├── app.py                  # Main application
├── config_service.py       # Configuration API
├── status_service.py       # Status API
├── mqtt_client.py          # MQTT connection handler
├── printer_manager.py      # Printer management
├── requirements.txt        # Dependencies
└── README.md
```

**Key Files:**
- `app.py` - Application entry point
- `config_service.py` - Config API endpoints
- `status_service.py` - Status API endpoints
- `mqtt_client.py` - MQTT client implementation
- `printer_manager.py` - Printer lifecycle

**Development:**
```bash
# Run with auto-reload
python app.py

# Run tests
pytest

# Type checking
mypy .

# Linting
pylint *.py
```

### go2rtc Configuration

**Location:** `/backend/go2rtc.yaml`

**Format:**
```yaml
streams:
  printer-1:
    - "rtsps://bblp:{access_code}@{ip}:322/streaming/live/1"

api:
  listen: ":1984"

webrtc:
  candidates:
    - {server_ip}:1984
```

**Auto-generated** by backend when printers are added.

### Docker Development

**Build local image:**
```bash
# From project root
docker build -t bambu-farm-monitor:dev .

# Run locally built image
docker run -d \
  --name bambu-dev \
  -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
  -v $(pwd)/config:/app/config \
  bambu-farm-monitor:dev

# Check logs
docker logs -f bambu-dev
```

**Test changes:**
```bash
# Make code changes
# Rebuild
docker build -t bambu-farm-monitor:dev .

# Restart
docker stop bambu-dev
docker rm bambu-dev
# Run again
```

### Testing

**Frontend Tests:**
```bash
cd frontend

# Unit tests
npm test

# Coverage
npm test -- --coverage

# E2E tests (if available)
npm run test:e2e
```

**Backend Tests:**
```bash
cd backend

# Unit tests
pytest tests/

# Coverage
pytest --cov=. tests/

# Integration tests
pytest tests/integration/
```

**Manual Testing:**
1. Test with real printers
2. Verify video streams work
3. Check MQTT status updates
4. Test all API endpoints
5. Try different layouts
6. Test settings changes
7. Export/import configuration
8. Test in multiple browsers

## Code Style Guidelines

### Python (Backend)

**Style Guide:** PEP 8

**Formatting:**
```python
# Good
def get_printer_status(printer_id: int) -> Dict[str, Any]:
    """Get current status for a printer.

    Args:
        printer_id: Unique printer identifier

    Returns:
        Dictionary containing printer status

    Raises:
        ValueError: If printer_id is invalid
    """
    if printer_id < 1:
        raise ValueError("Invalid printer_id")

    return {
        "printer_id": printer_id,
        "status": "idle",
        "connected": True
    }
```

**Key Points:**
- Use type hints
- Docstrings for functions/classes
- Meaningful variable names
- Keep functions small and focused
- Handle errors explicitly

### JavaScript/React (Frontend)

**Style Guide:** Airbnb JavaScript Style Guide (with modifications)

**Formatting:**
```javascript
// Good
const PrinterCard = ({ printer, onUpdate }) => {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await api.getPrinterStatus(printer.id);
        setStatus(response.data);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);

    return () => clearInterval(interval);
  }, [printer.id]);

  return (
    <div className="printer-card">
      <h3>{printer.name}</h3>
      <StatusDisplay status={status} />
    </div>
  );
};

export default PrinterCard;
```

**Key Points:**
- Use functional components with hooks
- Destructure props
- Clean up effects
- Handle loading/error states
- Meaningful component names

### Git Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```bash
# Good
feat(frontend): Add dark mode toggle

Added dark mode option in settings panel. Theme preference
is saved to localStorage and persists across sessions.
Uses CSS variables for easy theming.

Closes #123

# Good
fix(mqtt): Handle connection timeout gracefully

MQTT client now retries connection on timeout instead of
crashing. Added exponential backoff with max 5 retries.

Fixes #456

# Good
docs(wiki): Add Synology installation guide

Comprehensive guide for installing on Synology NAS with
Container Manager. Includes GUI and CLI methods.
```

## Pull Request Guidelines

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Added tests for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is complete

### PR Description Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- List of changes
- Another change
- etc.

## Testing
How was this tested?

## Screenshots
If UI changes, add screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No merge conflicts

## Related Issues
Closes #123
Relates to #456
```

### Review Process

**What to Expect:**
1. Automated checks run (if configured)
2. Maintainer reviews code
3. Feedback provided
4. You address feedback
5. Approved and merged

**Timeline:**
- Initial review: 1-3 days
- Follow-up: 1-2 days per iteration

**Tips:**
- Be patient and responsive
- Address all feedback
- Ask questions if unclear
- Be open to suggestions

## Community Guidelines

### Code of Conduct

**Be respectful:**
- Treat everyone with respect
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy

**Not tolerated:**
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information

**Reporting:**
Report violations to: [email or contact method]

### Communication

**GitHub Discussions:**
- Ask questions
- Share ideas
- Help others
- Showcase setups

**GitHub Issues:**
- Bug reports only
- Feature requests
- Technical problems

**Be helpful:**
- Search before asking
- Provide details
- Follow up on your issues
- Help others when you can

## Recognition

**Contributors are recognized in:**
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

**Top contributors may become:**
- Project collaborators
- Maintainers
- Documentation leads

## Future Roadmap

**Planned Features:**
- Dark mode / theming
- Mobile app (React Native)
- Email/SMS notifications
- Multi-language support
- Plugin system
- Advanced analytics
- Time-lapse recording
- Print queue management
- Multiple farms support
- Cloud sync (optional)

**Help Wanted:**
Check issues tagged with:
- `good first issue` - Easy for beginners
- `help wanted` - Need assistance
- `enhancement` - New features

## Resources

**Documentation:**
- [README](../README.md)
- [Wiki](Home.md)
- [API Documentation](API-Documentation.md)

**External:**
- [Bambu Lab API Docs](https://github.com/Bambulab/BambuStudio/wiki)
- [go2rtc Documentation](https://github.com/AlexxIT/go2rtc)
- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)

**Tools:**
- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Postman](https://www.postman.com/) - API testing
- [React DevTools](https://react.dev/learn/react-developer-tools)

## Questions?

**Need help getting started?**
- Ask in [GitHub Discussions](https://github.com/neospektra/bambu-farm-monitor/discussions)
- Check [existing issues](https://github.com/neospektra/bambu-farm-monitor/issues)
- Read the [documentation](Home.md)

**Thank you for contributing!** 🎉
