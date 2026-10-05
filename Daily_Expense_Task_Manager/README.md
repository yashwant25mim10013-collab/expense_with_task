# Daily Expense & Task Manager — Smart Edition v2.0

A complete student productivity desktop application using Python + CustomTkinter + SQLite, now extended with automation, profiles, reminders, local AI-style insights, advanced PDF reports and a browser version.

## Implemented systems

### Core
- Dashboard
- Expense CRUD
- Task CRUD
- Search
- Budget tracking
- Analytics charts
- CSV / Excel export
- SQLite persistence
- Input validation
- Basic unit tests

### New automation
- Recurring expenses: Daily / Weekly / Monthly
- Recurring tasks: Daily / Weekly / Monthly
- Automatic generation of due recurring records

### Productivity
- Desktop reminders
- Due-time popup notifications
- User login and multiple profiles
- Profile listing

### Smart insights
- Largest spending category
- Budget status
- Remaining budget
- Task completion rate
- Pending-task workload warning

The insights are local rule-based analytics, so no API key or internet connection is required.

### Reports / backup
- Advanced PDF monthly report
- CSV
- Excel
- SQLite database backup

### Web / mobile access
Run:

```bash
python web_app.py
```

Then open `http://127.0.0.1:5000` in a browser. The Flask interface can also be opened from a phone on the same local network using the computer's local IP address.

## Login
Demo account:
- Username: `admin`
- Password: `admin123`

Create additional profiles from the login screen.

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Project structure

```text
Daily_Expense_Task_Manager/
├── main.py
├── web_app.py
├── database/
├── models/
├── pages/
├── components/
├── utils/
├── analytics/
├── exports/
└── tests/
```

## Notes
A true production cloud-sync service requires a cloud provider/account and secure authentication. This version implements local database backup plus a browser-accessible Flask interface without requiring an external cloud service.
