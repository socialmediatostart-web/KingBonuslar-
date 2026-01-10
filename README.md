# 🧠 MarkUniversal v0.0.2
### Iteration: II

Modular Telegram bot for **Bonus Management**, **Scheduled Messaging**, and **Referrals Tracking**. Built on **Aiogram**, uses **PostgreSQL**.

---

## 🚀 Features

### 💸 Bonus System
- Create, edit, activate/deactivate bonuses  
- Cancel Bonus Request Answer Options ✅  
- Filter Bonus Requests by status ✅  
- Bonus requests status logic refactored with double-checks ✅  

### 📢 Message Broadcasting
- Send messages to:
  - All users ✅
  - Specific user ✅
  - User groups ✅
- Confirm before sending ✅
- Schedule messages for future time ✅
- Optional:
  - URL button ✅
  - Image ✅

### 📊 Reporting
- Google Sheets `.xlsx` reports
- Added **Users statistics** tab with referral ranking ✅
- Bonus request statistics summary ✅

### 👤 User & Group Management
- Change user group logic ✅
- Subscription fixes & enhancements ✅

### 💬 UI Improvements
- Added "Bonus" button to main menu ✅
- Confirmation UI before sending messages ✅
- Updated CTA on URL buttons ✅

### 🧾 Referral System
- Invite users and earn rewards ✅
- Tracked and reflected in reports ✅

---

## ⚙️ Prerequisites

- Docker + Docker Compose  
- Python 3.9+  
- Telegram Bot Token  
- Google Service Account JSON  

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://your-repo-url
cd MarkUniversal
```

### 2. Create `.env` file

```ini
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres

# Telegram bot
CHANNEL_USERNAME=@your_channel
CHANNEL_ID=-1001234567890
BOT_TOKEN=your_bot_token
BOT_ADMINS=comma_separated_user_ids

# Admin panel
ADMIN_DEBUG=True
ADMIN_SECRET=your_secret
ADMIN_HOST=localhost
ADMIN_PORT=5002

# Logging
BOT_LOG_FILENAME=bot.log
ADMIN_LOG_FILENAME=admin.log

# PGAdmin (optional)
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password

# UI/Links
COMMUNITY_URL=https://t.me/your_community
BONUS_TRANSFER_URL=https://your_bonus_landing_url.com
WEBAPP_URL=https://your_web_app.com
SUPPORT_URL=https://t.me/your_support
REGISTRATION_URL=https://t.me/your_registration
RESOURCE_NAME=YourBotName

# Google Drive API
GOOGLE_DRIVE_ROOT_FOLDER_ID=drive_folder_id
TOP_REFERRAL_SOURCES_N=10

# Scheduler
SCHEDULED_MESSAGE_CHECK_FREQUENCY_MIN=5
SEND_SCHEDULED_CHUNK_SIZE=50
```

---

## 📂 Project Structure

```
MarkUniversal/
├── bot/                     # Aiogram handlers, FSM states, filters
├── common/                  # Constants, enums
├── keyboards/               # Inline/reply keyboards
├── logics/                  # Business logic layer (bonus, user, message, etc)
├── models/                  # Peewee ORM models
├── utils/                   # Reports, scheduler, commands
├── .env                     # Environment config
├── docker-compose.yml       # Docker config
└── README.md                # This file
```

---

## 🧪 Running the Project

```bash
docker-compose up --build -d
```

Bot will run in background and logs will be written to `bot.log`.

---

## 🧰 Admin Tools

- PGAdmin: http://localhost:5050  
- Admin logs: `admin.log`  
- Telegram bot logs: `bot.log`  

---

## 📌 Notes

- Make sure your Google Service Account has upload permission to the target Drive folder.  
- Never commit `.env` or `google_client_secret.json` files.  
- Make sure to schedule messages responsibly — only admins can use scheduling features.
