# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pms"
app_title = "Frappe Hotel Pms"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Hotel Pms for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pms/css/pms.bundle.css"
app_include_js = "/assets/pms/js/pms.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "pms.engine.on_document_submit",
        "on_cancel": "pms.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "pms.engine.daily_scheduled_sync"
    ]
}
