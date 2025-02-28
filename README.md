# 🗑️ Automatic Spam Email Deletion Script

## 📌 Overview  
This Python script automates the process of detecting and deleting spam or unwanted emails from your Gmail inbox. It uses **IMAP** to access emails, checks their **subject** and **sender**, and moves matching emails to the trash. After deleting, it logs the details in an **Excel file** and sends an **alert email** with a summary of deleted emails.

---

## 🚀 Features
✅ **Automatically deletes spam emails** based on predefined keywords  
✅ **Logs deleted emails** (date, sender, subject) in an Excel file  
✅ **Sends an alert email** after deletion, attaching the log file  
✅ **Provides a summary** of emails deleted per sender  
✅ **Secure authentication** using IMAP and SMTP  
✅ **Works with Gmail** (requires IMAP access and an app password)

---

## 🛠️ Setup & Installation

### 1️⃣ Enable IMAP in Gmail  
1. Go to **Gmail Settings** → **See all settings**  
2. Navigate to **Forwarding and POP/IMAP**  
3. Enable **IMAP Access**  

### 2️⃣ Generate an App Password  
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)  
2. Select **Mail** and **Device** (e.g., "Windows Computer")  
3. Copy the generated **app password** (replace it in the script)

### 3️⃣ Install Required Libraries  
Make sure you have Python installed, then install the dependencies:

```sh
pip install openpyxl
```

---

## 🔧 Configuration

Edit the script to set up your **email credentials**:

```python
EMAIL = "your-email@gmail.com"
PASSWORD = "your-app-password"
ALERT_RECEIVER1 = "your-email@gmail.com"
ALERT_RECEIVER2 = "another-email@example.com"
```

You can also **customize spam detection criteria** by modifying the `DELETE_CRITERIA` set:

```python
DELETE_CRITERIA = {
    "sale", "discount", "offer", "limited-time", "subscribe now", "urgent action required",
    "claim your prize", "lottery winner", "free trial", "update your preferences", "unsubscribe now"
}
```

---

## 🔄 How It Works
1️⃣ The script connects to your Gmail inbox using **IMAP**  
2️⃣ It **fetches all emails** and checks if the subject or sender contains spam keywords  
3️⃣ If a match is found, the email is **moved to Trash** and logged in an **Excel file**  
4️⃣ After deletion, the script **sends an alert email** with:  
   - The **log file** as an attachment  
   - A **summary** of deleted emails by sender  

---

## 📊 Example Summary in Alert Email  
```
The following are the number of mails deleted from each sender:
Facebook: 5 mails
Instagram: 7 mails
Coding Ninjas: 3 mails
```

---

## ▶️ Running the Script  
You can run the script manually:

```sh
python delete_spam.py
```

Or schedule it to run automatically using **Task Scheduler (Windows) / Cron Jobs (Linux & Mac).**

---

## 🛑 Warnings  
- **Use at your own risk!** The script permanently deletes emails.  
- **Test with a limited number of emails first** before using it in production.  
- **Do not share your app password publicly** or upload it to GitHub.

---

## 📌 Future Improvements  
✔ Add **GUI for customization**  
✔ Implement **machine learning for smarter spam detection**  
✔ Extend support to **multiple email providers**  

---

## 📧 Contact & Support  
If you have any issues, feel free to **open an issue** or contact me at `your-email@gmail.com`. 🚀
