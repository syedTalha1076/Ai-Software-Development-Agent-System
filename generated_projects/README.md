# Simple Calculator

This is a simple web-based calculator application built with Python and Streamlit.

## Features

*   Basic arithmetic operations: Addition, Subtraction, Multiplication, Division.
*   Handles division by zero error.
*   Clear functionality to reset inputs and result.

## Project Structure

```
simple_calculator/
├── app.py                  # Main Streamlit application file (contains UI and calculator logic)
├── requirements.txt        # Lists Python dependencies (e.g., streamlit)
└── README.md               # Project description, setup, and run instructions
```

## Setup and Run Instructions

Follow these steps to set up and run the calculator application locally:

### 1. Clone the repository (if applicable)

```bash
git clone <repository_url>
cd simple_calculator
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

*   **On macOS and Linux:**

    ```bash
    source .venv/bin/activate
    ```

*   **On Windows:**

    ```bash
    .\.venv\Scripts\activate
    ```

### 4. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit Application

Once the dependencies are installed, you can run the application:

```bash
streamlit run app.py
```

This command will open the calculator application in your default web browser.

## Usage

1.  Enter the first number in the "First Number" input field.
2.  Enter the second number in the "Second Number" input field.
3.  Click on one of the operation buttons (+, -, *, /) to perform the calculation.
4.  The result will be displayed below the operation buttons.
5.  Click the "Clear" button to reset both input fields and the result.
