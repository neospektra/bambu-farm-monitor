// Global state
let printersConfig = [];
const lastKnownStatus = {};
let statusUpdateInterval = null;

// Check if setup is required and redirect
async function checkSetupRequired() {
    try {
        const response = await fetch('/api/config/setup-required');
        const data = await response.json();
        if (data.setup_required) {
            window.location.href = '/setup.html';
            return true;
        }
        return false;
    } catch (error) {
        console.error('Error checking setup status:', error);
        return false;
    }
}

// Load printer configuration from API
async function loadPrintersConfig() {
    try {
        const response = await fetch('/api/config/printers');
        const data = await response.json();
        printersConfig = data.printers || [];
        return printersConfig;
    } catch (error) {
        console.error('Error loading printer configuration:', error);
        return [];
    }
}

// Create printer card HTML
function createPrinterCard(printer) {
    const card = document.createElement('div');
    card.className = 'camera-card resizable';
    card.id = `printer-card-${printer.id}`;
    card.innerHTML = `
        <div class="camera-header">
            <h2 id="printer-name-${printer.id}">${printer.name}</h2>
            <span class="stream-status" id="stream-status-${printer.id}">●</span>
        </div>
        <div class="video-container" id="container-${printer.id}">
            <iframe class="camera-video" id="video-${printer.id}"
                    src="/stream.html?src=printer${printer.id}"
                    allowfullscreen></iframe>
            <button class="fullscreen-btn" onclick="toggleFullscreen('container-${printer.id}')" title="Fullscreen">⛶</button>
        </div>
        <div class="printer-status" id="status-${printer.id}">
            <div class="status-loading">Loading status...</div>
        </div>
        <div class="resize-handle"></div>
    `;
    return card;
}

// Initialize printer cards
async function initializePrinters() {
    const grid = document.getElementById('printers-grid');
    if (!grid) return;

    // Clear existing cards
    grid.innerHTML = '';

    // Load configuration
    const printers = await loadPrintersConfig();

    if (printers.length === 0) {
        grid.innerHTML = '<div class="no-printers">No printers configured. Go to Settings to add printers.</div>';
        return;
    }

    // Create and append cards
    printers.forEach(printer => {
        const card = createPrinterCard(printer);
        grid.appendChild(card);

        // Initialize status cache
        lastKnownStatus[printer.id] = null;
    });

    // Make cards resizable
    makeCardsResizable();

    // Update status indicator
    setTimeout(() => {
        const statusIndicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        if (statusIndicator && statusText) {
            statusIndicator.classList.add('connected');
            statusText.textContent = 'System Ready';
        }
    }, 1000);
}

// Make printer cards resizable
function makeCardsResizable() {
    const cards = document.querySelectorAll('.camera-card.resizable');

    cards.forEach(card => {
        const handle = card.querySelector('.resize-handle');
        if (!handle) return;

        let startX, startY, startWidth, startHeight;

        handle.addEventListener('mousedown', (e) => {
            e.preventDefault();
            startX = e.clientX;
            startY = e.clientY;
            startWidth = parseInt(document.defaultView.getComputedStyle(card).width, 10);
            startHeight = parseInt(document.defaultView.getComputedStyle(card).height, 10);

            document.addEventListener('mousemove', resize);
            document.addEventListener('mouseup', stopResize);
        });

        function resize(e) {
            const width = startWidth + e.clientX - startX;
            const height = startHeight + e.clientY - startY;

            // Set minimum dimensions
            if (width > 300) {
                card.style.width = width + 'px';
            }
            if (height > 250) {
                card.style.height = height + 'px';
            }
        }

        function stopResize() {
            document.removeEventListener('mousemove', resize);
            document.removeEventListener('mouseup', stopResize);
        }
    });
}

// Fullscreen toggle function
function toggleFullscreen(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!document.fullscreenElement) {
        // Enter fullscreen
        if (container.requestFullscreen) {
            container.requestFullscreen();
        } else if (container.webkitRequestFullscreen) {
            container.webkitRequestFullscreen();
        } else if (container.mozRequestFullScreen) {
            container.mozRequestFullScreen();
        } else if (container.msRequestFullscreen) {
            container.msRequestFullscreen();
        }
    } else {
        // Exit fullscreen
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }
}

// Handle fullscreen changes
function handleFullscreenChange() {
    const buttons = document.querySelectorAll('.fullscreen-btn');
    buttons.forEach(btn => {
        if (document.fullscreenElement) {
            btn.style.opacity = '0';
        } else {
            btn.style.opacity = '0.7';
        }
    });
}

// Check if status data is complete/valid
function isCompleteStatus(status) {
    if (status.printing && status.print_progress > 0) {
        return status.print_file &&
               status.print_layer !== undefined &&
               status.print_total_layers !== undefined;
    }
    return true;
}

// Merge new status with cached status
function mergeStatus(cached, newStatus) {
    if (!cached) return newStatus;

    const merged = { ...cached };

    // Always update temps and connection status
    merged.nozzle_temp = newStatus.nozzle_temp;
    merged.bed_temp = newStatus.bed_temp;
    merged.connected = newStatus.connected;

    // Always update AMS data if present
    if (newStatus.ams) {
        merged.ams = newStatus.ams;
    }

    // Only update printing info if the new data is complete
    if (newStatus.printing && newStatus.print_progress > 0 && newStatus.print_file) {
        merged.printing = newStatus.printing;
        merged.print_progress = newStatus.print_progress;
        merged.print_file = newStatus.print_file;
        merged.print_layer = newStatus.print_layer;
        merged.print_total_layers = newStatus.print_total_layers;
        merged.print_time_remaining = newStatus.print_time_remaining;
        merged.nozzle_target = newStatus.nozzle_target;
        merged.bed_target = newStatus.bed_target;
    } else if (newStatus.print_progress === 0 && newStatus.print_file === '') {
        // Clear printing data if truly idle
        merged.printing = false;
        merged.print_progress = 0;
        merged.print_file = '';
        merged.print_layer = 0;
        merged.print_total_layers = 0;
        merged.print_time_remaining = 0;
        merged.nozzle_target = 0;
        merged.bed_target = 0;
    }

    return merged;
}

// Format time remaining
function formatTimeRemaining(minutes) {
    if (!minutes || minutes <= 0) return '--';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
        return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
}

// Update printer status display
function updatePrinterStatus(printerId, status) {
    const statusDiv = document.getElementById(`status-${printerId}`);
    const streamStatus = document.getElementById(`stream-status-${printerId}`);

    if (!statusDiv) return;

    // Merge with cached status
    const mergedStatus = mergeStatus(lastKnownStatus[printerId], status);
    lastKnownStatus[printerId] = mergedStatus;

    // Helper function to render AMS colors
    function renderAMSColors(amsData) {
        if (!amsData || !amsData.has_ams || !amsData.trays || amsData.trays.length === 0) {
            return '';
        }

        const traysHTML = amsData.trays.map((tray, index) => {
            const isActive = amsData.active_tray === tray.id || amsData.active_tray === String(index);
            const color = tray.empty ? 'CCCCCC' : tray.color;
            const activeClass = isActive ? 'active' : '';
            const emptyClass = tray.empty ? 'empty' : '';
            const type = tray.type || 'Empty';

            return `
                <div class="ams-tray ${activeClass} ${emptyClass}" title="${type}">
                    <div class="ams-color" style="background-color: #${color}"></div>
                    ${isActive ? '<div class="ams-indicator">▼</div>' : ''}
                </div>
            `;
        }).join('');

        return `
            <div class="ams-section">
                <div class="ams-label">AMS:</div>
                <div class="ams-trays">
                    ${traysHTML}
                </div>
            </div>
        `;
    }

    // Update stream status indicator
    if (streamStatus) {
        if (mergedStatus.connected) {
            streamStatus.classList.add('connected');
        } else {
            streamStatus.classList.remove('connected');
        }
    }

    // Build status HTML
    if (!mergedStatus.connected) {
        statusDiv.innerHTML = '<div class="status-disconnected">Disconnected</div>';
        return;
    }

    if (mergedStatus.printing) {
        const fileName = mergedStatus.print_file.split('/').pop().replace('.gcode', '');
        const progress = Math.round(mergedStatus.print_progress || 0);
        const layer = mergedStatus.print_layer || 0;
        const totalLayers = mergedStatus.print_total_layers || 0;
        const timeRemaining = formatTimeRemaining(mergedStatus.print_time_remaining);

        statusDiv.innerHTML = `
            <div class="status-printing">
                <div class="print-info">
                    <div class="file-name">${fileName}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${progress}%"></div>
                        <span class="progress-text">${progress}%</span>
                    </div>
                </div>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-icon">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm0 1h12a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                            </svg>
                        </div>
                        <div class="status-info">
                            <div class="status-label">Layer</div>
                            <div class="status-value">${layer} / ${totalLayers}</div>
                        </div>
                    </div>

                    <div class="status-item">
                        <div class="status-icon">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                            </svg>
                        </div>
                        <div class="status-info">
                            <div class="status-label">Remaining</div>
                            <div class="status-value">${timeRemaining}</div>
                        </div>
                    </div>

                    <div class="status-item">
                        <div class="status-icon nozzle">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M9.293 0H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h2.5l-1 2.5V14a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-.5L8.5 11H11a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H9.293z"/>
                            </svg>
                        </div>
                        <div class="status-info">
                            <div class="status-label">Nozzle</div>
                            <div class="status-value">${Math.round(mergedStatus.nozzle_temp || 0)}° / ${Math.round(mergedStatus.nozzle_target || 0)}°</div>
                        </div>
                    </div>

                    <div class="status-item">
                        <div class="status-icon bed">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                <path d="M0 11v4h16v-4H0zm1 3v-2h14v2H1zM3 8h10v2H3V8z"/>
                            </svg>
                        </div>
                        <div class="status-info">
                            <div class="status-label">Bed</div>
                            <div class="status-value">${Math.round(mergedStatus.bed_temp || 0)}° / ${Math.round(mergedStatus.bed_target || 0)}°</div>
                        </div>
                    </div>
                </div>
                ${renderAMSColors(mergedStatus.ams)}
            </div>
        `;
    } else {
        statusDiv.innerHTML = `
            <div class="status-idle">
                <div class="idle-text">Idle</div>
                <div class="status-temps">
                    <span>🌡️ Nozzle: ${Math.round(mergedStatus.nozzle_temp || 0)}°</span>
                    <span>🌡️ Bed: ${Math.round(mergedStatus.bed_temp || 0)}°</span>
                </div>
                ${renderAMSColors(mergedStatus.ams)}
            </div>
        `;
    }
}

// Update all printer statuses
async function updateStatuses() {
    try {
        const response = await fetch('/api/status/printers');
        const statuses = await response.json();

        printersConfig.forEach(printer => {
            const status = statuses[printer.id];
            if (status) {
                updatePrinterStatus(printer.id, status);
            }
        });
    } catch (error) {
        console.error('Error updating statuses:', error);
    }
}

// Initialize application
async function initialize() {
    console.log('Initializing Bambu Labs Farm Monitor');

    // Check if setup is required
    const setupRequired = await checkSetupRequired();
    if (setupRequired) return;

    // Initialize printers
    await initializePrinters();

    // Start status updates
    if (printersConfig.length > 0) {
        updateStatuses(); // Initial update
        statusUpdateInterval = setInterval(updateStatuses, 2000); // Update every 2 seconds
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', initialize);

document.addEventListener('fullscreenchange', handleFullscreenChange);
document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
document.addEventListener('mozfullscreenchange', handleFullscreenChange);
document.addEventListener('MSFullscreenChange', handleFullscreenChange);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (statusUpdateInterval) {
        clearInterval(statusUpdateInterval);
    }
});
