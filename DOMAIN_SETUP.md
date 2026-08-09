# 🌐 Setting Up a Custom Enterprise Domain for ReguAI

Follow these steps to connect your custom domain (e.g., `app.reguai.ai` or `reguai.com`) to your Streamlit Cloud production deployment:

### Step 1: Purchase Domain & Access DNS Settings
1. Purchase your custom domain from **Namecheap**, **GoDaddy**, or **Cloudflare**.
2. Open your Domain Management Dashboard -> **DNS Settings / Zone Editor**.

### Step 2: Add CNAME Record
Add a new CNAME record pointing to your Streamlit Cloud application instance:
- **Type:** CNAME
- **Name / Host:** `app` (for `app.yourdomain.com`) or `@` (for apex domain)
- **Target / Value:** `domains.streamlit.app`
- **TTL:** Automatic or 300 seconds

### Step 3: Configure Streamlit Community Cloud
1. Go to your [Streamlit Cloud Workspace](https://share.streamlit.io).
2. Find the app `reguai-global-platform` and click **Settings (⚙️)**.
3. Navigate to **Custom Domain**.
4. Enter your custom domain: `app.reguai.ai`.
5. Click **Save**. SSL Certificate (HTTPS) will be automatically provisioned via Let's Encrypt within 15-30 minutes.