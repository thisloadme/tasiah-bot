# tasiah_bot
Tasiah adalah rule-based chatbot pada Telegram yang akan memberikan artikel islami sesuai dengan pertanyaan yang diberikan oleh user

# instalasi
1. install package/library berikut dulu
```
pip install numpy
pip install scikit-learn
pip install tensorflow
pip install keras
pip install matplotlib
pip install python-telegram-bot
pip install nltk
```

2. rename .env.example menjadi .env

3. isi TELEGRAM_API_KEY pada env dengan API KEY dari telegram bot Anda

4. run chatbot service di background process
```
nohup python(3) telegram_bot.py >/dev/null 2>&1 &
```

5. katakan halo pada bot tasiah :)