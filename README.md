# Fsub Bot - Force Subscribe

Bot Telegram Fsub sederhana untuk Heroku. Wajib join channel dulu baru bisa akses link.

## 1. Fitur
- Force Subscribe Channel
- Auto kirim file kalau sudah join
- Log ke channel
- Support MongoDB

## 2. Deploy ke Heroku 1-Klik

[![Deploy]<!DOCTYPE html>
<html>
  <div class="center-content">
    <a
    href="https://heroku.com/deploy?template=https://github.com/ciosukasuka/ciofsub">
      <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
    </a>
  </div>
</html>

## 3. Deploy Manual

### A. Persiapan
1.  Buat Bot di [@BotFather](https://t.me/BotFather) > `/newbot` > ambil `BOT_TOKEN`
2.  Ambil `API_ID` & `API_HASH` di [my.telegram.org](https://my.telegram.org)
3.  Buat Channel > Ambil `CHANNEL_ID`. Caranya: Add `@RawDataBot` ke channel > kirim pesan > copy `id`
4.  Opsional: Buat MongoDB di [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### B. Set Config Vars di Heroku
Buka `Settings > Reveal Config Vars` isi ini:

| Key | Contoh | Penjelasan |
| --- | --- | --- |
| `API_ID` | `123456` | Dari my.telegram.org |
| `API_HASH` | `a1b2c3d4e5f6` | Dari my.telegram.org |
| `BOT_TOKEN` | `12345:ABC` | Dari @BotFather |
| `CHANNEL_ID` | `-1003715933062` | ID Channel Wajib Join |
| `LOG_CHANNEL` | `-1003715933062` | ID Channel untuk Log. Bisa sama |
| `ADMINS` | `123456789` | ID Telegram kamu. Pisah spasi kalau >1 |
| `DB_URI` | `mongodb+srv://...` | Link MongoDB. Kosongin kalau gak pake |

### C. Langkah WAJIB biar gak error
Ini penyebab `ValueError: Peer id invalid`
1.  Add bot kamu ke `CHANNEL_ID` dan `LOG_CHANNEL`
2.  Jadikan bot sebagai `Admin` > centang `Post Messages`
3.  Kirim 1 pesan `test` di channel itu. Tujuannya biar bot "kenal" ID channel

### D. Deploy
```bash
git push heroku main
heroku ps:scale worker=1
heroku logs --tail
