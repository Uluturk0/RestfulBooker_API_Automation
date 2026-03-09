# 🏨 Restful-Booker API Test Automation Framework

This repository contains a fully structured, Enterprise-level API Test Automation framework built with **Python** and **Pytest**. It tests the publicly available [Restful-Booker API](https://restful-booker.herokuapp.com/).

## 🚀 Key Features & Architecture
- **Separation of Concerns:** Clear boundaries between test data, API clients, and test logic.
- **Data-Driven Testing:** Dynamic payload generation using `Faker` and boundary value injection via JSON files.
- **Schema Validation:** Strict JSON Schema validation using `jsonschema` to ensure API contract integrity.
- **Performance Testing:** Validating API response times against defined SLAs.
- **Centralized Logging:** Custom logger implementation that records all pre/post API executions and test steps into a permanent `automation.log` file.
- **Allure Reporting & API Snapshots:** Comprehensive HTML reports that automatically capture and attach actual API JSON responses (Snapshots) for every test execution.
- **Execution Archive:** Dynamically generates timestamped report folders (`reports/YYYY-MM-DD/HH-MM-SS`) to preserve historical test run data.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Testing Framework:** Pytest
- **HTTP Client:** Requests
- **Data Generation:** Faker
- **Reporting:** Allure
- **Validation:** JSON Schema

## 📦 Project Structure
```text
tests/            # Test suites (E2E, Negative, Performance, Schema)
api/              # API endpoints abstraction (Booking, Auth)
core/             # Base client, Configuration, and Logger
schemas/          # JSON Schema blueprints
test_data/        # Static payloads for Data-Driven boundary testing
utils/            # Helper functions (Faker generators, Custom assertions)
```

## ⚙️ How to Run Locally

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Run All Tests**
```bash
pytest
```

**3. Generate and View Allure Report**
Allure results are dynamically saved in timestamped folders. To view the latest run:
```bash
allure serve reports/YYYY-MM-DD/HH-MM-SS_results
```

## 🐛 Known API Bugs (Caught by this Framework!)
1. **Security:** Sending invalid credentials returns `200 OK` instead of `401 Unauthorized`.
2. **Validation:** System accepts negative values for `totalprice` and lacks maximum length validation for `firstname` (Returns `200 OK` instead of `400 Bad Request`).