# 📧 Gmail API Quick Setup (5 Minutes)

## 🎯 Goal: Get Gmail App Password

**Time:** 5 minutes  
**Difficulty:** Easy  
**Cost:** FREE

---

## 📋 Step-by-Step

### **Step 1: Enable 2-Step Verification**

1. Go to: https://myaccount.google.com/security
2. Find **"2-Step Verification"**
3. Click **"Get Started"** (if not enabled)
4. Follow setup wizard
5. Verify with phone number

**✅ Done when:** "2-Step Verification" shows as "On"

---

### **Step 2: Create App Password**

1. Still on Security page: https://myaccount.google.com/security
2. Find **"App Passwords"** (below 2-Step Verification)
3. Click **"App Passwords"**
4. Select app: **"Mail"**
5. Select device: **"Other (Custom name)"**
6. Enter name: **"Lead Generation Tool"**
7. Click **"Generate"**

---

### **Step 3: Copy Password**

You'll see a 16-character password like:
```
xxxx xxxx xxxx xxxx
```

**Copy this password!** (You won't see it again)

---

### **Step 4: Save to `.env`**

Edit `backend/.env` and add:

```env
# Gmail Configuration
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=xxxx xxxx xxxx xxxx
MANAGER_EMAILS=manager1@email.com,manager2@email.com
```

**Replace:**
- `your_email@gmail.com` with your Gmail address
- `xxxx xxxx xxxx xxxx` with the app password (remove spaces or keep them)
- `manager1@email.com` with email(s) to receive reports

---

## ✅ Verification

**Test it:**

```python
# In Python console
import smtplib
from email.mime.text import MIMEText

sender = "your_email@gmail.com"
password = "your_app_password"
receiver = "test@email.com"

msg = MIMEText("Test email")
msg['Subject'] = "Test"
msg['From'] = sender
msg['To'] = receiver

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()

print("Email sent!")
```

---

## 🎯 Quick Checklist

- [ ] Enabled 2-Step Verification
- [ ] Created App Password
- [ ] Copied 16-character password
- [ ] Added to `backend/.env`
- [ ] Tested (optional)

---

## 🆘 Troubleshooting

### **"App Passwords" not showing:**
- Make sure 2-Step Verification is enabled first
- Refresh the page
- Try different browser

### **"Invalid credentials":**
- Check password is correct (no extra spaces)
- Make sure you copied the full 16 characters
- Regenerate if needed

### **"Less secure app" error:**
- Use App Password (not regular password)
- App Passwords are more secure

---

## ✅ Done!

**Your Gmail API is now configured!**

**Next:** Collect Google Sheets API (10 minutes)

**See:** `COLLECT_ALL_APIS.md` for complete guide

