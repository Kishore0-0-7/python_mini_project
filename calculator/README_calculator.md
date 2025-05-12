# Advanced Scientific Calculator

A modern, feature-rich calculator application built with Python and Tkinter that provides both basic and scientific calculation capabilities with a clean, intuitive interface.

## Features

### User Interface
- Sleek, modern design with rounded buttons and shadow effects
- Beautiful color scheme with vibrant colors
- Responsive button feedback (hover and click effects)
- Clean display area with result preview
- History tracking for recent calculations

### Basic Calculator Functions
- Standard arithmetic operations (+, -, *, /, %)
- Proper order of operations and bracket support
- Decimal point support
- Positive/negative number toggling

### Scientific Calculator Features
- Trigonometric functions (sin, cos, tan)
- Inverse trigonometric functions (asin, acos, atan)
- Logarithmic functions (log10, ln)
- Constants (π, e)
- Square root and power functions
- Absolute value

### Advanced Input Capabilities
- Full expression editing with cursor positioning
- Implicit multiplication (e.g., 5(3+4) works as 5*(3+4))
- Bracket balance tracking with visual indicator
- Error handling and reporting

### Keyboard Support
- Number and operator keys
- Backspace for deletion
- Enter for calculation
- Arrow keys for cursor movement
- Home/End keys for cursor navigation

## Usage Instructions

### Basic Mode
1. Use the number buttons (0-9) to input numbers
2. Use operation buttons (+, -, *, /) for arithmetic operations
3. Press "=" to calculate the result
4. Use "C" to clear the input
5. Use "DEL" to delete the last character
6. Use "±" to toggle between positive and negative values

### Scientific Mode
1. Click the "↔ Scientific" button to toggle scientific mode
2. Use the scientific function buttons for advanced calculations
3. Constants like π and e can be inserted directly
4. Use power functions (x², x³) with numbers
5. Functions like sin, cos, etc. will automatically add opening brackets

### Input Editing
- Click anywhere in the expression to position the cursor
- Use left and right arrow keys to navigate
- Home/End keys move to the beginning/end of the expression
- Brackets are automatically balanced and tracked

## Requirements
- Python 3.x
- Tkinter (usually included with Python installation)

## Installation
1. Ensure Python 3.x is installed on your system
2. Install Tkinter if not already included:
   ```
   sudo apt-get install python3-tk  # For Debian/Ubuntu
   ```
   or
   ```
   pip install tk  # For other platforms
   ```
3. Run the calculator:
   ```
   python3 calculator.py
   ```

## Tips
- The calculator shows a live preview of the result as you type
- The history section shows your recent calculations
- The bracket indicator helps ensure your expressions are properly balanced
- You can use keyboard shortcuts for faster input 