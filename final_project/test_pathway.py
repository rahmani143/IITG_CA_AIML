import pathway as pw
import time

# Try to create a table from a dictionary of columns
try:
    # Attempt direct Table creation (may require internal _context)
    table = pw.Table({"id": [1, 2, 3], "value": [10, 20, 30]})
except TypeError as e:
    print("Direct Table() creation failed:", e)
    # Try to use a factory method if available
    if hasattr(pw, "table_transformer"):
        try:
            table = pw.table_transformer.from_dict({"id": [1, 2, 3], "value": [10, 20, 30]})
            print("Created table via table_transformer.from_dict")
        except Exception as e2:
            print("table_transformer.from_dict failed:", e2)
            raise
    else:
        raise

# Define a reactive function that prints each row from the table
@pw.react
def print_rows(row=table):
    print(f"id: {row['id']}, value: {row['value']}")

# Run the pathway event loop
pw.run()

# Sleep briefly so output appears before script exits
time.sleep(1)
