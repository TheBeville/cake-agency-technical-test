# Cake Agency Technical Test
A command line application that fetches order data from an API and calculates the average order value, written in Python.

## Installation

1. Check Python 3.7+ is installed
   <br>(Note: if older versions of python also installed, may need to replace 'python' command with 'python3' in below snippets)<br><br>
2. Create a virtual environment (recommended):
   ```bash
   python -m venv cake-agency-test
   source cake-agency-test/bin/activate  # On Windows: cake-agency-test\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Main application:
```bash
python main.py
```

For unit tests, run the following command:
```bash
python -m unittest tests/test_cake_agency.py -v
```
