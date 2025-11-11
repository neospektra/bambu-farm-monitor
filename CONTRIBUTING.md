# Contributing to Bambu Farm Monitor

Thank you for your interest in contributing to Bambu Farm Monitor! This document provides guidelines and information for contributors.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Assume good faith

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details**:
   - Docker/Podman version
   - OS/Platform (QNAP, Synology, etc.)
   - Container logs if applicable
5. **Screenshots** if relevant

### Suggesting Features

Feature requests are welcome! Please include:

1. **Use case**: Why is this feature needed?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches you've thought about
4. **Additional context**: Any other relevant information

### Pull Requests

1. **Fork the repository** and create a branch from `main`
2. **Make your changes** following the code style guidelines below
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

#### Code Style Guidelines

**Python (APIs)**:
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

**JavaScript (Frontend)**:
- Use modern ES6+ syntax
- Use `async/await` for asynchronous code
- Add comments for complex logic
- Keep functions pure where possible

**HTML/CSS**:
- Semantic HTML5 elements
- Mobile-first responsive design
- Use CSS variables for theming
- Keep styles modular

#### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable (`Fixes #123`)

Example:
```
Add support for 5+ printers

- Modify config API to support dynamic printer count
- Update UI to handle variable grid layouts
- Add tests for multi-printer scenarios

Fixes #42
```

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/bambu-farm-monitor.git
   cd bambu-farm-monitor
   ```

2. **Build the container**:
   ```bash
   docker build -t bambu-farm-monitor:dev .
   ```

3. **Run for development**:
   ```bash
   docker run -d \
     --name bambu-dev \
     -p 8080:8080 -p 1984:1984 -p 5000:5000 -p 5001:5001 \
     -v $(pwd)/config:/app/config \
     -v $(pwd)/www:/var/www/html \
     -v $(pwd)/api:/app/api \
     bambu-farm-monitor:dev
   ```

4. **View logs**:
   ```bash
   docker logs -f bambu-dev
   ```

### Testing

- **Manual testing**: Test with real Bambu printers if possible
- **API testing**: Test API endpoints with curl or Postman
- **Browser testing**: Test UI in Chrome, Firefox, Safari
- **Mobile testing**: Test responsive design on mobile devices

### Areas That Need Help

- **Documentation**: Improve README, add tutorials
- **Testing**: Add automated tests
- **Features**: See open issues tagged with `enhancement`
- **Bug fixes**: See open issues tagged with `bug`
- **Platform support**: Test on different NAS platforms (Synology, Unraid, etc.)
- **Internationalization**: Add support for multiple languages

## Project Structure

```
bambu-farm-monitor/
├── Dockerfile           # Container build definition
├── docker-compose.yml   # Docker Compose example
├── entrypoint.sh        # Container startup script
├── supervisord.conf     # Process manager config
├── nginx.conf           # Web server config
├── go2rtc.yaml          # Streaming server config
├── api/
│   ├── config_api.py    # Configuration management API
│   ├── status_api.py    # MQTT status monitoring API
│   └── requirements.txt # Python dependencies
├── www/
│   ├── index.html       # Main dashboard
│   ├── setup.html       # Setup wizard
│   ├── settings.html    # Settings page
│   ├── stream.html      # Video stream iframe
│   └── style.css        # Shared styles
├── config/
│   └── printers.json    # Printer configuration
└── README.md            # Documentation
```

## Release Process

1. Update version in README badges
2. Update CHANGELOG.md
3. Create a git tag: `git tag -a v2.1.0 -m "Release v2.1.0"`
4. Push tag: `git push origin v2.1.0`
5. Build and push Docker image:
   ```bash
   docker build -t neospektra/bambu-farm-monitor:v2.1.0 .
   docker tag neospektra/bambu-farm-monitor:v2.1.0 neospektra/bambu-farm-monitor:latest
   docker push neospektra/bambu-farm-monitor:v2.1.0
   docker push neospektra/bambu-farm-monitor:latest
   ```
6. Create GitHub release with changelog

## Questions?

Feel free to open a discussion or reach out in the issues section!

Thank you for contributing! 🎉
