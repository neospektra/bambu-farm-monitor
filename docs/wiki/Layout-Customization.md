# Layout Customization

Customize how printer windows are arranged on your dashboard.

## Layout Selector

The layout selector provides 6 pre-configured grid layouts to organize your printer views.

### Accessing Layout Controls

Located in the header bar between the status indicator and settings icon.

**Visual Icons:**
- Each layout option has a visual icon showing the grid pattern
- Active layout is highlighted with green glow
- Click any icon to switch layouts instantly

### Available Layouts

#### Auto Grid (Default)
**Icon:** Dashed 2x2 grid  
**Behavior:** Responsive grid that adapts to screen size  
**Best For:**
- Variable number of printers
- Different screen sizes
- General use

**Grid Behavior:**
- Desktop: 2 columns minimum
- Tablet: 1-2 columns
- Mobile: 1 column

#### 1 Column
**Icon:** Single vertical bar  
**Behavior:** All printers stacked vertically  
**Best For:**
- Focusing on one printer at a time
- Scrolling through printers
- Mobile devices
- Narrow screens

#### 2 Columns
**Icon:** Two vertical bars  
**Behavior:** Side-by-side printer views  
**Best For:**
- 2 printers
- 4 printers (2x2)
- Wide screens
- Comparing two prints

#### 2x2 Grid
**Icon:** Four squares in grid  
**Behavior:** Exactly 4 printers in 2x2 layout  
**Best For:**
- Exactly 4 printers
- Balanced view
- Standard monitors

#### 3 Columns
**Icon:** Three vertical bars  
**Behavior:** Three printers across  
**Best For:**
- 3, 6, or 9 printers
- Wide/ultrawide monitors
- Print farm overview

#### 4 Columns
**Icon:** Four vertical bars  
**Behavior:** Four printers across  
**Best For:**
- 4, 8, or 12+ printers
- Ultrawide monitors
- Maximum density
- Large print farms

## Layout Persistence

**Automatic Saving:**
- Your layout choice is saved to browser localStorage
- Automatically restored when you return
- Per-browser setting (not shared across devices)

**Clearing:**
```javascript
// Browser console
localStorage.removeItem('preferred-layout');
```

## Resizing Windows

### Individual Window Resizing

**Resize Handle:**
- Located in bottom-right corner of each printer card
- Diagonal arrow icon (↘)

**How to Resize:**
1. Hover over resize handle
2. Click and drag
3. Release when desired size reached

**Minimum Size:**
- Width: 300px
- Height: 250px

**Notes:**
- Resize works in all layouts
- Other windows may reflow depending on layout
- Custom sizes are not saved (reset on layout change)

### Fullscreen Mode

**Per-Printer Fullscreen:**
1. Click fullscreen button (⛶) on video
2. Printer video goes fullscreen
3. Press Esc to exit

**Browser Fullscreen:**
- Press F11 for full browser fullscreen
- All printers visible
- Press F11 again to exit

## Responsive Behavior

### Desktop (>1400px)
- All layouts work as described
- Auto grid shows 2+ columns
- Maximum detail visible

### Tablet (768px - 1400px)
- Auto grid shows 1-2 columns
- Multi-column layouts still work
- Some horizontal scrolling on 4-column

### Mobile (<768px)
- All layouts force to 1 column
- Stack vertically for scrolling
- Resize handles hidden

## Layout Tips

### For 2 Printers
**Recommended:** 2 Columns  
**Why:** Equal space, side-by-side comparison

### For 3 Printers
**Recommended:** 3 Columns  
**Why:** All visible, no wasted space

**Alternative:** Auto Grid  
**Why:** Adapts to screen rotation

### For 4 Printers
**Recommended:** 2x2 Grid  
**Why:** Balanced, symmetrical view

**Alternative:** 2 Columns  
**Why:** Less vertical scrolling

### For 5-6 Printers
**Recommended:** 3 Columns  
**Why:** Fits 6 perfectly, 5 leaves one space

**Alternative:** 2 Columns  
**Why:** More space per printer

### For 7-8 Printers
**Recommended:** 4 Columns  
**Why:** Fits 8 perfectly

**Alternative:** 2x2 Grid  
**Why:** Requires scrolling but larger views

### For 9+ Printers
**Recommended:** 4 Columns  
**Why:** Maximum density

**Alternative:** Auto Grid  
**Why:** Flexible as you scroll

## Performance Considerations

### Video Streams

**Resource Usage:**
- Each visible stream uses CPU/GPU
- More streams = higher resource usage

**Optimization:**
- Use 1 Column layout
- Scroll to show only active printers
- Browsers pause off-screen videos (most)

### Layout Changes

**Instant:**
- Layout changes apply immediately
- No page reload required
- CSS grid transition

## Customization via CSS (Advanced)

### Custom Layouts

**Not currently supported in UI**, but possible via browser DevTools:

```css
/* Example: 5 column layout */
.grid-container {
    grid-template-columns: repeat(5, 1fr) !important;
}
```

**Future Feature:**
- Custom layout creator
- Save multiple layouts
- Quick-switch between saved layouts

## Keyboard Shortcuts

**Not currently implemented**, but planned:

```
1-4: Switch to 1-4 column layout
G: Toggle grid/list view
F: Toggle fullscreen
R: Reset to auto layout
```

## Troubleshooting

### Layout Doesn't Change

**Problem:** Clicking layout buttons does nothing

**Solutions:**
1. Hard refresh (Ctrl+Shift+R)
2. Check browser console for errors
3. Update to latest version (v3.3.7+)
4. Clear browser cache

### Layout Resets on Refresh

**Problem:** Returns to Auto on every page load

**Solutions:**
1. Check localStorage is enabled in browser
2. Not in incognito/private mode
3. Browser allows localStorage
4. Check browser console for errors

### Windows Don't Resize

**Problem:** Resize handle doesn't work

**Solutions:**
1. Check you're dragging the resize handle (↘)
2. Minimum size limits prevent smaller
3. Try different browser
4. Update to latest version

### Layout Looks Wrong on Mobile

**Problem:** Overlapping or cut-off windows

**Solutions:**
1. All layouts force to 1 column on mobile
2. This is expected behavior
3. Rotate to landscape for more space
4. Use desktop for multi-column layouts

## Related Features

### Status Display Modes

**Compact Mode** (future):
- Hide idle printers
- Show only printing
- Dense information display

### Grid Gaps

**Fixed gap:** 20px between cards

**Future customization:**
- Adjustable gap size
- No-gap mode for maximum density

### Window Snapping

**Not currently implemented**

**Planned:**
- Snap to grid
- Align to other windows
- Distribute evenly

## Next Steps

- **[Printer Configuration](Printer-Configuration.md)** - Add/remove printers
- **[Common Issues](Common-Issues.md)** - Troubleshoot display problems
- **[Performance Optimization](Performance-Optimization.md)** - Improve performance
