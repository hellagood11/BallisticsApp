# import statements
import csv
from typing import Any

#Exception handling for PyScript environment
try:
    from pyscript import document, when  # type: ignore
except ImportError:
    document: Any = None
    def when(*_args, **_kwargs):
        def _decorator(func):
            return func
        return _decorator

# Global state to hold loaded data and current filters
STATE = {"rows": []}

# Define the columns we expect in our reloading data for consistent table rendering
TABLE_COLUMNS = [
    "Source",
    "Cartridge",
    "Bullet Weight",
    "Bullet Type",
    "C.O.L.",
    "Powder",
    "Start Charge",
    "Start Velocity",
    "Max Charge",
    "Max Velocity",
]

# Helper functions for HTML escaping and CSV loading
def _escape_html(value):
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

# Loading and processing CSV data for both pistol and rifle reloading, then populating filters and rendering the table
def _load_source(csv_file, source_name):
    rows = []
    #open the CSV file and read contents
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cartridge_name = row.get("Cartridge", "").strip()
            if not cartridge_name:
                continue
            # Build a unified row structure for both pistol and rifle data, ensuring all expected columns are present
            rows.append(
                {
                    "Source": source_name,
                    "Cartridge": cartridge_name,
                    "Bullet Weight": row.get("Bullet_Weight", ""),
                    "Bullet Type": row.get("Bullet_Type", ""),
                    "C.O.L.": row.get("C_O_L", ""),
                    "Powder": row.get("Powder", ""),
                    "Start Charge": row.get("Start_Charge", ""),
                    "Start Velocity": row.get("Start_Velocity", ""),
                    "Max Charge": row.get("Max_Charge", ""),
                    "Max Velocity": row.get("Max_Velocity", ""),
                }
            )

    return rows

# Function to load both pistol and rifle data
def load_reloading_data():
    try:
        pistol_rows = _load_source("pistolReloading.csv", "Pistol")
        rifle_rows = _load_source("rifleReloading.csv", "Rifle")
        STATE["rows"] = pistol_rows + rifle_rows
        populate_cartridge_filter()
        render_table(STATE["rows"])
    except (OSError, csv.Error, UnicodeDecodeError) as error:
        document.querySelector("#reload-summary").innerText = f"Error loading CSV files: {error}"
        document.querySelector("#reload-table-output").innerHTML = ""

# Function to populate the cartridge filter dropdown based on the loaded data, ensuring only valid cartridge names are included
def populate_cartridge_filter():
    cartridge_filter = document.querySelector("#cartridge-filter")
    cartridge_names = sorted({row["Cartridge"] for row in STATE["rows"]})

    options_html = ["<option value='All'>All Cartridges</option>"]
    for cartridge in cartridge_names:
        safe_value = _escape_html(cartridge)
        options_html.append(f"<option value='{safe_value}'>{safe_value}</option>")

    cartridge_filter.innerHTML = "".join(options_html)

# Function to build the HTML table from the filtered data
def build_table_html(rows):
    html = "<table class='data-table'><thead><tr>"

    for column in TABLE_COLUMNS:
        html += f"<th>{_escape_html(column)}</th>"

    html += "</tr></thead><tbody>"

    for row in rows:
        html += "<tr>"
        for column in TABLE_COLUMNS:
            html += f"<td>{_escape_html(row.get(column, ''))}</td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html

# Function to render the table and update the summary text based on the current filters
def render_table(rows):
    document.querySelector("#reload-summary").innerText = (
        f"Showing {len(rows)} of {len(STATE['rows'])} cartridge loads"
    )

    if not rows:
        document.querySelector("#reload-table-output").innerHTML = (
            "<p>No cartridge matches the selected filters.</p>"
        )
        return

    document.querySelector("#reload-table-output").innerHTML = build_table_html(rows)

# Function to apply filters based on user selection and update the displayed table accordingly
def apply_filters(_event=None):
    selected_source = str(document.querySelector("#source-filter").value)
    selected_cartridge = str(document.querySelector("#cartridge-filter").value)

    filtered_rows = STATE["rows"]

    if selected_source != "All":
        filtered_rows = [
            row for row in filtered_rows if row["Source"] == selected_source
        ]

    if selected_cartridge != "All":
        filtered_rows = [
            row for row in filtered_rows if row["Cartridge"] == selected_cartridge
        ]

    render_table(filtered_rows)

# Event listeners for filter changes to trigger table updates
@when("change", "#source-filter")
def on_source_change(event):
    apply_filters(event)

# Event listener for cartridge filter changes to trigger table updates
@when("change", "#cartridge-filter")
def on_cartridge_change(event):
    apply_filters(event)

# Initial data load when the script runs
load_reloading_data()
