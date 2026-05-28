# ☁️ AWS (Amazon Web Services) Production Deployment Guide

Deploying your KSCST project on **Amazon Web Services (AWS)** represents the highest level of industry standard and cloud architecture. It will highly impress any project review panel or institutional evaluator!

This guide covers the two best ways to host your Flask + TiDB Cloud Campus Placement Portal on AWS:
1. **Option A: AWS App Runner (Recommended & Easiest)**: Modern, fully-managed serverless hosting with automatic Git synchronization and auto-scaling.
2. **Option B: AWS EC2 (Traditional Linux Server)**: Renting a virtual Ubuntu server and setting up **Nginx + Gunicorn** manually. *Excellent for demonstrating advanced systems and networking skills.*

---

## 🛠️ Prep Step: Prepare Your Environment Settings
Before deploying on AWS, make sure you have:
1. **Your GitHub Repo:** Placed online (already completed: `ChandanAN2003/Smart-Campus-Placement-Portal`).
2. **Your TiDB Cloud Serverless Connection:** Host, User, Password, Port (4000).
3. **Your Gemini/Groq API Keys.**

---

## 🚀 Option A: Deploying with AWS App Runner (Serverless & Easiest)
AWS App Runner is a fully managed service that takes your Flask code directly from GitHub, builds it, and runs it with automated auto-scaling and zero server administration.

### Step 1: Create an AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com/) and click **Create an AWS Account**.
2. Complete the registration (you will get 12 Months of Free Tier services).

### Step 2: Navigate to App Runner
1. In the AWS Console search bar, search for **App Runner** and click it.
2. Click **Create an App Runner service**.

### Step 3: Connect Your GitHub Repository
1. For **Repository type**, select **Source code repository**.
2. Under **Connect to GitHub**, click **Add new** and sign in to link your GitHub account.
3. Select your repository: `ChandanAN2003/Smart-Campus-Placement-Portal`.
4. Choose the **Branch**: `main`.
5. Under **Deployment settings**, select **Automatic** (so that whenever you push code to GitHub, AWS redeploys your site automatically!). Click **Next**.

### Step 4: Configure the Build
1. Select **Configure all settings here**.
2. **Runtime:** `Python 3`
3. **Build Command:** 
   ```bash
   pip install -r backend/requirements.txt
   ```
4. **Start Command:** 
   ```bash
   cd backend && gunicorn --bind 0.0.0.0:8080 app:app
   ```
5. **Port:** `8080` (AWS App Runner defaults to exposing port 8080).
6. Click **Next**.

### Step 5: Configure Environment Variables
Scroll down to the **Environment variables** section and click **Add environment variable** for each key:

| Key | Value | Description |
| :--- | :--- | :--- |
| **`DB_HOST`** | `gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com` | Your live TiDB Host |
| **`DB_USER`** | `48mZbxucLdV55MM.root` | Your TiDB Username |
| **`DB_PASS`** | `Gj8Oq4L6u5cAmiQ1` | Your TiDB Password |
| **`DB_NAME`** | `test` | Database schema name |
| **`DB_PORT`** | `4000` | TiDB connection port |
| **`GEMINI_API_KEY`** | *`Your-Gemini-Key`* | Google Generative AI key |
| **`GROQ_API_KEY`** | *`Your-Groq-Key`* | Groq fallback LLM key |
| **`SECRET_KEY`** | *`Generate-a-random-long-string`* | Flask session security key |

### Step 6: Review & Deploy!
1. Under **Virtual CPU & Memory**, select the default **1 vCPU and 2 GB memory** (fully sufficient to serve 1,000+ active students!).
2. Click **Next**, review the settings, and click **Create & Deploy**.
3. AWS will spend 3-5 minutes building the environment and will issue a beautiful secure URL (e.g., `https://xxxxxx.us-east-1.awsapprunner.com`). 
4. **Your app is now live on AWS! 🎉**

---

## 🐧 Option B: Manually Deploying on AWS EC2 (Full Linux Server)
Deploying on an **EC2 (Ubuntu Server)** lets you show the evaluators that you know how to configure production web environments using **Gunicorn, Nginx, and systemd**.

### Step 1: Launch an EC2 Instance
1. Go to the AWS Console, search for **EC2**, and click **Launch Instance**.
2. **Name:** `placement-portal-server`
3. **OS Image (AMI):** Select **Ubuntu 22.04 LTS** (eligible for Free Tier).
4. **Instance Type:** Select **t2.micro** (Free Tier eligible).
5. **Key pair:** Select **Create new key pair**, download the `.pem` file (keep it safe on your laptop), and name it `placement-key`.
6. **Network Settings (CRITICAL):**
   * Check **Allow SSH traffic** (to log in from your computer).
   * Check **Allow HTTP traffic from the internet** (port 80).
   * Check **Allow HTTPS traffic from the internet** (port 443).
7. Click **Launch Instance**.

### Step 2: Log into your Linux Server (via SSH)
1. Open PowerShell or Terminal on your laptop and navigate to where you saved the `.pem` file.
2. Connect to the EC2 server (replace with your server's Public IP):
   ```powershell
   ssh -i "placement-key.pem" ubuntu@your-ec2-public-ip
   ```

### Step 3: Update Server & Install Prerequisites
Once logged inside your AWS Ubuntu terminal:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
```

### Step 4: Clone the Repository
```bash
git clone https://github.com/ChandanAN2003/Smart-Campus-Placement-Portal.git
cd Smart-Campus-Placement-Portal
```

### Step 5: Configure Virtual Environment & Dependencies
```bash
# Navigate to backend
cd backend

# Create & activate environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 6: Setup your Production `.env` File
Create a `.env` file in the `backend` folder:
```bash
nano .env
```
Paste the following values, making sure to configure them with your active credentials:
```env
DB_HOST=gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com
DB_USER=48mZbxucLdV55MM.root
DB_PASS=Gj8Oq4L6u5cAmiQ1
DB_NAME=test
DB_PORT=4000
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
SECRET_KEY=generate-a-random-secure-key
```
Press `CTRL+O` then `Enter` to save, and `CTRL+X` to exit.

---

### Step 7: Create a systemd Background Service (Continuous Running)
We need the Flask app to run forever in the background, even if we close the SSH window.
```bash
sudo nano /etc/systemd/system/placement.service
```
Paste this configuration inside:
```ini
[Unit]
Description=Gunicorn instance to serve Smart Campus Placement Portal
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Smart-Campus-Placement-Portal/backend
Environment="PATH=/home/ubuntu/Smart-Campus-Placement-Portal/backend/venv/bin"
ExecStart=/home/ubuntu/Smart-Campus-Placement-Portal/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5001 app:app

[Install]
WantedBy=multi-user.target
```
Save and exit (`CTRL+O`, `Enter`, `CTRL+X`), then start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start placement
sudo systemctl enable placement
```

---

### Step 8: Configure Nginx as a Reverse Proxy
Nginx will listen on standard Port 80 (HTTP) and securely forward the traffic to our Gunicorn server running internally on port 5001.

```bash
sudo nano /etc/nginx/sites-available/placement
```
Paste this block:
```nginx
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Max upload limit for student resumes
    client_max_body_size 16M;
}
```
Link and enable the Nginx block:
```bash
sudo ln -s /etc/nginx/sites-available/placement /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
```
**You are complete! 🎉** Go to `http://your-ec2-public-ip` in your browser and watch the portal run live on AWS EC2!
