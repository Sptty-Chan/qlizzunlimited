# Copyright (c) 2023 Sptty-Chan
# Author: Sptty Chan / Fanda, 18 Juni 2023 (Open Source Project)

# INCLUDE LIBRARIES
import requests, re, time
from datetime import datetime
from flask_executor import Executor
from flask import Flask

# DATA USER
coki = ""  # isi dengan cookies qlizz
username = ""  # isi dengan username instagram (wajib akun yang sama dengan yang digunakan di web qlizz)

# APPLICATION
app = Flask("BOT FOLLOW INSTAGRAM UNLIMITED 24/7")
executor = Executor(app)

# STATISTIC
stat = True
followers_terkirim = 0
failed = 0
success = 0
last_sent = {"time": "-"}

# BACKGROUND TASK
def bacground():
    global success, failed, followers_terkirim
    while True:
        dg = requests.get(
            "https://qlizz.com/instagram/autofollowers", cookies={"cookie": coki}
        ).text
        token = re.search('name="_token" value="(.*?)"', dg).group(1)
        zs = requests.post(
            "https://qlizz.com/instagram/send",
            data={"_token": token, "link": username, "tool": "autofollowers"},
            cookies={"cookie": coki},
        ).text
        if "You have already used your free demo" in zs:
            failed += 1
        else:
            success += 1
            followers_terkirim += 10
            fhour = (
                f"0{str(datetime.now().hour)}"
                if len(str(datetime.now().hour)) == 1
                else str(datetime.now().hour)
            )
            fminute = (
                f"0{str(datetime.now().minute)}"
                if len(str(datetime.now().minute)) == 1
                else str(datetime.now().minute)
            )
            last_sent["time"] = f"{fhour}.{fminute} Waktu Server"
        time.sleep(7260)


# MAIN APP
@app.route("/")
def index():
    global stat
    if stat:
        stat = False
        executor.submit(bacground)
    html_template = f"""<h3>Selamat datang {username}, refresh halaman untuk memperbarui statistik</h3><br><br>Total Followers Terkirim : {followers_terkirim}<br>Berhasil : {success}<br>Gagal : {failed}<br>Terakhir Terkirim : Pukul {last_sent['time']}"""
    return html_template


# START
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
