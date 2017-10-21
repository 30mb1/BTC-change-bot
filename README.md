# Change bot

Change bot is an universal exchange where you can buy and sell BTC, LTC, ETH and other popular currencies. Service use escrow mechanism to ensure the safety of your money.

## Getting started

### Requirements

- Python 3
- MySQL

### Installation

Clone repository

```
git clone https://github.com/30mb1/BTC-change-bot.git
cd Telegram-mailer
```

Create virtual environment and install requirements.

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Create database for bot

```bash
mysql -u <user> -p < database.sql
```

### Usage

Bot is still in development.

### How it is work

- Bot use [this](https://github.com/python-telegram-bot/python-telegram-bot) library for work.

- Bot supports localization via gettext. All texts that bot use are stored in texts.py file. To create new localization file, generate .po file using texts.py, moderate it and compile. Then place compiled .mo file in an appropriate folder in */locale*. Insert translation function in utils/decorators.py in LANGS variable, so @info decorator would provide it to all bot functions. (section for choosing language is not created yet)

- When inline button is pressed, bot get special callback update, which contains callback_data. It usually has next structure:

  ​	(level1) (level2) (additional info)

  App use this data for routing. At first, high level router send update(user's message) to section depending on level1 value; then, next section-router sends update to appropriate function-handler using level2. Every section has its own router in file, named same as directory.

### To do:

- develop trade process - at the moment nothing happens when pressing button 'start bargain'
- complete 'create new bargain' process
- develop mechanism of getting prices from exchanges - values are hardcoded now
- connect nodes to bot - there is no real work with currencies at the moment. Need to create wallets for clients and develop exchange mechanism

 

