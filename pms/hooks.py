# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pms"
app_title = "Frappe Hotel Pms"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Hotel Pms - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pms/css/pms.bundle.css"
app_include_js = "/assets/pms/js/pms.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Hotel Pms Entry": {
        "validate": "pms.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "pms.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "pms.tasks.hourly_sync"
    ],
    "daily": [
        "pms.tasks.daily_reconciliation"
    ],
    "weekly": [
        "pms.tasks.weekly_digest"
    ]
}
