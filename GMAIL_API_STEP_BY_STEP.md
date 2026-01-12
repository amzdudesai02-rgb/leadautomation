# 📧 Gmail API Setup - Step by Step

## 🎯 Simple Method: Use App Passwords (Recommended)

**You don't need Google Cloud Console for Gmail!** Use App Passwords instead - it's much easier!

---

## 📋 Step-by-Step Instructions

### **Step 1: Go to Google Account Security**

1. **Open new tab** (keep Google Cloud Console open)
2. Go to: https://myaccount.google.com/security
3. Or click your profile icon → **"Manage your Google Account"** → **"Security"**

---

### **Step 2: Enable 2-Step Verification**

1. On Security page, find **"2-Step Verification"**
2. If it says **"Off"**, click it
3. Click **"Get Started"**
4. Follow the setup:
   - Enter your password
   - Add phone number
   - Verify with code sent to phone
   - Click **"Turn On"**

**✅ Done when:** "2-Step Verification" shows **"On"**

---

### **Step 3: Create App Password**

1. Still on Security page: https://myaccount.google.com/security
2. Scroll down to find **"App Passwords"**
   - It's below "2-Step Verification"
   - If you don't see it, make sure 2-Step Verification is ON first
3. Click **"App Passwords"**
4. You may need to sign in again
5. Select app: **"Mail"**
6. Select device: **"Other (Custom name)"**
7. Type name: **"Lead Generation Tool"**
8. Click **"Generate"**

---

### **Step 4: Copy the Password**

You'll see a **16-character password** like:
```
abcd efgh ijkl mnop
```

**⚠️ IMPORTANT:** Copy this password NOW! You won't see it again!

**Format:** It might show as `abcd efgh ijkl mnop` or `abcdefghijklmnop`

---

### **Step 5: Add to Your `.env` File**

1. Go back to your project folder
2. Open `backend/.env` file
3. Add these lines:

```env
# Gmail Configuration
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=abcdefghijklmnop
MANAGER_EMAILS=manager1@email.com,manager2@email.com
```

**Replace:**
- `your_email@gmail.com` → Your Gmail address
- `abcdefghijklmnop` → The 16-character app password (remove spaces if any)
- `manager1@email.com` → Email(s) to receive reports (optional, can add later)

**Example:**
```env
GMAIL_USER=no-reply@amzdudes.io
GMAIL_PASSWORD=abcd efgh ijkl mnop
MANAGER_EMAILS=admin@amzdudes.io
```

**Note:** You can keep spaces in password or remove them - both work!

---

### **Step 6: Test It (Optional)**

**Test if it works:**

```python
# In Python console (backend folder)
import smtplib
from email.mime.text import MIMEText

sender = "your_email@gmail.com"
password = "your_app_password"  # The 16-char password
receiver = "test@email.com"

msg = MIMEText("Test email from Lead Generation Tool")
msg['Subject'] = "Test"
msg['From'] = sender
msg['To'] = receiver

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## ✅ Quick Checklist

- [ ] Went to https://myaccount.google.com/security
- [ ] Enabled 2-Step Verification
- [ ] Created App Password
- [ ] Copied 16-character password
- [ ] Added GMAIL_USER to `.env`
- [ ] Added GMAIL_PASSWORD to `.env`
- [ ] Added MANAGER_EMAILS to `.env` (optional)
- [ ] Tested (optional)

---

## 🆘 Troubleshooting

### **"App Passwords" option not showing:**
- ✅ Make sure 2-Step Verification is **ON** first
- ✅ Refresh the page
- ✅ Try different browser
- ✅ Make sure you're on Security page

### **"Invalid credentials" error:**
- ✅ Check password is correct (all 16 characters)
- ✅ Remove spaces from password (or keep them - both work)
- ✅ Make sure you're using App Password, not regular password
- ✅ Regenerate App Password if needed

### **"Less secure app" error:**
- ✅ Use App Password (not regular password)
- ✅ App Passwords are more secure than "less secure apps"

---

## 🎯 What This Enables

After setup, your app can:
- ✅ Send automated email reports
- ✅ Send daily/weekly summaries
- ✅ Send lead notifications
- ✅ Email managers with updates

---

## 📝 Next Steps

After Gmail API setup:
1. ✅ Gmail API - DONE
2. ⏳ Google Sheets API - Next (10 minutes)
3. ⏳ Amazon PA-API - Last (you'll sign up)

---

## ✅ Summary

**Gmail API Setup:**
1. Enable 2-Step Verification
2. Create App Password
3. Add to `.env` file
4. Done!

**No Google Cloud Console needed for Gmail!** App Passwords are simpler and work perfectly for sending emails.

---

## 🚀 You're Done!

**Your Gmail API is configured!**

**Next:** Set up Google Sheets API (see `GOOGLE_SHEETS_API_SETUP.md`)

