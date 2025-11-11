# Wiki Documentation

This directory contains the wiki documentation for Bambu Farm Monitor.

## Publishing to GitHub Wiki

These markdown files are designed to be published to the GitHub wiki. To publish:

### Method 1: Manual Copy (Easiest)

1. Go to https://github.com/neospektra/bambu-farm-monitor/wiki
2. Click "New Page" for each article
3. Copy the content from each `.md` file
4. Use the filename without `.md` as the page title (e.g., `Home`, `Installation-Guide`)

### Method 2: Git Clone (Advanced)

```bash
# Clone the wiki repository
git clone https://github.com/neospektra/bambu-farm-monitor.wiki.git

# Copy all wiki files
cp docs/wiki/*.md bambu-farm-monitor.wiki/

# Push to wiki
cd bambu-farm-monitor.wiki
git add .
git commit -m "Add wiki documentation"
git push
```

### Method 3: GitHub Pages (Alternative)

These docs can also be served via GitHub Pages:

1. Enable GitHub Pages in repository settings
2. Point to the `docs` folder
3. Documentation will be available at `https://neospektra.github.io/bambu-farm-monitor/`

## Wiki Structure

The wiki is organized into the following main sections:

### Getting Started
- **Home.md** - Wiki landing page with navigation
- **Installation-Guide.md** - Complete installation instructions
- **Finding-Printer-Information.md** - How to locate printer details

### Reference
- **API-Documentation.md** - Complete REST API reference
- **Common-Issues.md** - Troubleshooting guide

### Additional Pages (To Be Created)

You can add more pages for:
- Quick-Start.md
- First-Time-Setup.md
- Printer-Configuration.md
- Layout-Customization.md
- Backup-and-Restore.md
- QNAP-Installation.md
- Synology-Installation.md
- Unraid-Installation.md
- Docker-Deployment.md
- Podman-Deployment.md
- Environment-Variables.md
- Reverse-Proxy-Setup.md
- Network-Configuration.md
- Security-Best-Practices.md
- Video-Stream-Issues.md
- MQTT-Connection-Problems.md
- Performance-Optimization.md
- Debugging-Guide.md
- Contributing.md
- FAQ.md
- Support.md

## Maintenance

When updating the wiki:

1. Edit the markdown files in this directory
2. Commit changes to the main repository
3. Copy updated files to the wiki repository
4. Keep both repositories in sync

## Formatting Guidelines

- Use GitHub Flavored Markdown
- Include code blocks with language hints (```bash, ```python, etc.)
- Add table of contents for long pages
- Use relative links between wiki pages
- Include "Next Steps" section at the end of guides
- Add screenshots when helpful (store in `docs/images/`)

## Links

- **Main Repository**: https://github.com/neospektra/bambu-farm-monitor
- **Wiki**: https://github.com/neospektra/bambu-farm-monitor/wiki
- **Docker Hub**: https://hub.docker.com/r/neospektra/bambu-farm-monitor
