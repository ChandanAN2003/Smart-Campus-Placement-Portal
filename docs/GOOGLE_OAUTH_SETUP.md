# 🔐 Google OAuth Production Integration Guide

This guide explains how to transition your application from **Demo/Mock Authentication** to **Live, Production-Grade Google Sign-In**.

---

## 💡 Why am I seeing "Demo Google User"?

By design, if the Google OAuth credentials (`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`) are missing or empty in your `backend/.env` configuration, the backend automatically falls back to **Mock / Demo OAuth Mode**. 

This allows developers to inspect the registration forms and dashboard pages instantly with a simulated `demo.google@example.com` profile without being blocked by network requests.

To activate **live Google authentication** for the college, you need to configure your own Google Developer Credentials.

---

## 🛠️ Step-by-Step Google Cloud Console Setup

Follow these exact steps to register your project with Google and obtain your live client credentials:

### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google / Institutional account.
3. Click the project dropdown at the top of the page and select **New Project**.
4. Name the project (e.g., `Smart-Campus-Placement-Portal`) and click **Create**.

---

### Step 2: Configure the OAuth Consent Screen
Before Google can issue credentials, you must define the user-facing consent screen:
1. In the left navigation menu, go to **APIs & Services** ➔ **OAuth consent screen**.
2. For **User Type**, select:
   * **Internal**: If your college uses Google Workspace (e.g., `@yourcollege.edu.in`) and you only want your college students to log in.
   * **External**: If you want anyone (including external reviewers or students with personal `@gmail.com` accounts) to be able to sign up and test the platform.
3. Click **Create**.
4. Fill in the **App Information**:
   * **App name**: `AI Smart Placement Portal`
   * **User support email**: *Select your email address*
   * **Developer contact email**: *Select your email address*
5. Click **Save and Continue** (skip Scopes and Test Users for now).

---

### Step 3: Create OAuth 2.0 Credentials
1. Go to the **Credentials** tab in the left sidebar.
2. Click **+ Create Credentials** at the top and select **OAuth client ID**.
3. Under **Application type**, select **Web application**.
4. In the **Name** field, enter `Placement Portal Client`.

---

### Step 4: Add Authorized Redirect URIs (CRITICAL)
Google will only send authentication tokens to explicitly whitelisted URLs.

1. Under the **Authorized JavaScript origins** section, click **+ Add URI** and add:
   * `http://localhost:5001` (For local development testing)

2. Under the **Authorized redirect URIs** section, click **+ Add URI** and add:
   * **Local Testing Redirect URI**:
     ```text
     http://localhost:5001/auth/callback/google
     ```
   * **Production / Render Redirect URI** (Replace with your actual Render URL when deployed):
     ```text
     https://smart-placement-portal.onrender.com/auth/callback/google
     ```

3. Click **Create** at the bottom.
4. A popup will display your **Client ID** and **Client Secret**. Copy these values!

---

## ⚙️ How to Update Your Settings

Now that you have your credentials, you must update the application to use them.

### 1. Local Configuration (`backend/.env`)
Open your `backend/.env` file and replace the empty Google fields:

```env
# OAuth Configuration
GOOGLE_CLIENT_ID=your_actual_google_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_actual_client_secret_here
```

> [!WARNING]
> Keep your `.env` file secret! It is already added to `.gitignore` so it won't be pushed to GitHub.

---

### 2. Production Configuration (Render.com Web Service)
When you deploy your application to Render:
1. Open the [Render Dashboard](https://dashboard.render.com).
2. Go to your **Web Service** ➔ **Environment** tab.
3. Add the following environment variables:
   * Key: `GOOGLE_CLIENT_ID` ➔ Value: `your_actual_google_client_id_here...`
   * Key: `GOOGLE_CLIENT_SECRET` ➔ Value: `GOCSPX-your_actual_client_secret_here`
4. Save the changes. Render will automatically redeploy the application with real Google login active!

---

## ⚡ Verifying Your Google Login
1. Start your Flask application locally:
   ```powershell
   cd backend
   python app.py
   ```
2. Navigate to `http://localhost:5001` in your browser.
3. Click **Sign up with Google** or **Sign in with Google**.
4. You will be redirected to the secure Google login screen.
5. After authenticating, you will return to the placement portal with your real name and email prefilled, ready to complete your profile!
