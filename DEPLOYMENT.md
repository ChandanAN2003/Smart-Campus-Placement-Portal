# 🚀 Deployment Guide: Smart Placement Portal

This guide will help you deploy your **Flask + MySQL + Gemini AI** project for **FREE** using **Render.com** (for the website) and **TiDB Cloud** (for the database).

---

## 📋 Prerequisites
1.  **GitHub Account**: Your code must be pushed to GitHub (which you have already done!).
2.  **Render Account**: Sign up at [render.com](https://render.com).
3.  **TiDB Cloud Account**: Sign up at [tidbcloud.com](https://tidbcloud.com) (Offers free 5GB MySQL database).

---

## 🛠 Step 1: Set up the Free Database (MySQL)

Since Render's free tier database expires after 30 days, we will use **TiDB Cloud** which provides a generous "Serverless" free tier that never expires.

1.  **Create Cluster**:
    *   Log in to TiDB Cloud.
    *   Click **"Create Cluster"**.
    *   Select **"Serverless"** Plan (Free).
    *   Region: Choose one closest to you (e.g., Mumbai or Singapore).
    *   Give it a name (e.g., `placement-db`) and click **Create**.

2.  **Get Credentials**:
    *   Once created, click **"Connect"**.
    *   Choose "Connect with Code" -> "Python" -> "SQLAlchemy".
    *   You will see a password generation popup. **Generate a Password** and copy it safely.
    *   Copy the options:
        *   **Host**: (e.g., `gateway01.ap-southeast-1.prod.aws.tidbcloud.com`)
        *   **User**: (e.g., `2.root`)
        *   **Port**: `4000`
        *   **Database**: `test` (You can rename this later to `placement_portal`).

3.  **Initialize the Database**:
    *   You can't run the `init_db.py` script easily on the cloud without connecting first.
    *   **Recommended**: Download a tool like **DBeaver** or **HeidiSQL**.
    *   Connect to your new TiDB Cloud database using the credentials above.
    *   Open your local file `database/schema.sql`.
    *   First, add `USE test;` (or whatever your cloud DB name is) at the top.
    *   Run the SQL script to create the tables (`users`, `drives`, etc.) on the cloud.

---

## ☁️ Step 2: Deploy the Backend to Render

1.  **New Web Service**:
    *   Go to your Render Dashboard.
    *   Click **New +** -> **Web Service**.
    *   Select "Build and deploy from a Git repository".
    *   Connect your GitHub repository (`Smart-Campus-Placement-Portal`).

2.  **Configure Settings**:
    *   **Name**: `smart-placement-portal`
    *   **Region**: Singapore (or nearest).
    *   **Branch**: `main`
    *   **Root Directory**: `backend` (⚠️ **Crucial**: This tells Render to look in the backend folder).
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`

3.  **Environment Variables**:
    *   Scroll down to "Environment Variables" and click "Add Environment Variable". Add the following:
    
    | Key | Value |
    | :--- | :--- |
    | `PYTHON_VERSION` | `3.10.0` |
    | `SECRET_KEY` | (Generate a random string) |
    | `GEMINI_API_KEY` | (Your Google Gemini API Key) |
    | `DB_HOST` | (Your TiDB Host) |
    | `DB_USER` | (Your TiDB User) |
    | `DB_PASSWORD` | (Your TiDB Password) |
    | `DB_NAME` | `test` (or your TiDB DB Name) |
    | `DB_PORT` | `4000` |
    | `RENDER` | `True` |

4.  **Deploy**:
    *   Click **"Create Web Service"**.
    *   Render will verify your files, install dependencies (Flask, etc.), and start the server.
    *   Watch the logs. If you see `[OK] Database initialized` or `Running on http://0.0.0.0:xxxx`, it worked!

---

## 🔗 Step 3: Access Your Project

Once the deployment finishes (green checkmark), Render will give you a URL like:
`https://smart-placement-portal.onrender.com`

**Open it, Log in, and Test!** 🚀

---

## ❓ Troubleshooting

*   **"Internal Server Error"**: Check the "Logs" tab in Render. It usually tells you if a library is missing or DB connection failed.
*   **"Table not found"**: Did you run the `schema.sql` on the TiDB cloud database?
*   **"ModuleNotFound"**: Ensure the missing library is listed in `backend/requirements.txt`.
