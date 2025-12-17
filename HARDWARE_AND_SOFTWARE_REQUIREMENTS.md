# Hardware and Software Requirements

The effective implementation and operation of the **AI-Integrated Smart Campus Placement Portal** require specific hardware and software configurations. These requirements ensure optimal performance, reliability, and security of the application during development and deployment.

## 2.4.1 Hardware Requirements
The system is designed to be lightweight and cloud-native, minimizing the need for expensive local hardware for end-users.

**Client-Side (User)**:
*   **Device**: Laptop, Desktop, or Tablet.
*   **Processor**: Intel Core i3 or equivalent (Minimum).
*   **RAM**: 4 GB (Minimum) / 8 GB (Recommended for smooth graphics rendering).
*   **Internet Connection**: Stable broadband or 4G connection (Required for API calls and AI Voice interaction).
*   **Peripherals**: Microphone (Required for AI Mock Interview features).

**Server-Side (Development Environment)**:
*   **Processor**: Intel Core i5 / Ryzen 5 (Quad-core or higher).
*   **RAM**: 8 GB (Minimum) / 16 GB (Recommended for running local databases and Docker).
*   **Storage**: 256 GB SSD (Faster I/O for database operations).

## 2.4.2 Software Requirements
The project relies on a specific set of software tools and libraries for development and execution.

**Development Environment**:
*   **Operating System**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+).
*   **Code Editor (IDE)**: Visual Studio Code (Recommended) or PyCharm.
*   **Version Control**: Git (2.3+).
*   **API Testing**: Postman (for testing Flask API endpoints).

**Application Stack**:
*   **Backend Runtime**: Python 3.10 or higher.
*   **Web Framework**: Flask 2.0+.
*   **Database**: MySQL 8.0 (Local) / TiDB Cloud (Production).
*   **Front-End**: Modern Web Browser (Chrome v90+, Edge, Firefox).

**External Libraries (Python)**:
*   `flask`: Web server gateway.
*   `google-generativeai`: Client SDK for Gemini Pro.
*   `mysql-connector-python`: Database driver.
*   `werkzeug`: For security and utilities.
*   `PyPDF2` / `python-docx`: For parsing resume files.
