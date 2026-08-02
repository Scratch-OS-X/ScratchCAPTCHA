import webview

# Le code HTML/CSS/JS exact avec le design parfait
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: Arial, Roboto, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
            background-color: #f9f9f9; 
            user-select: none;
        }

        .captcha-wrapper {
            position: relative;
            width: 310px;
            height: 140px;
        }

        .recaptcha-box {
            width: 310px;
            height: 80px;
            background-color: #f9f9f9;
            border: 1px solid #d3d3d3;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            position: absolute;
            top: 0;
            left: 0;
            transition: opacity 0.3s ease, transform 0.3s ease;
        }

        .checkbox-container {
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
        }

        .checkbox {
            width: 28px;
            height: 28px;
            border: 3px solid #b2b2b2;
            border-radius: 3px;
            background-color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .spinner {
            width: 14px;
            height: 14px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #4a70d6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: none;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .status-icon {
            width: 20px;
            height: 20px;
            display: none;
        }

        .checkbox-label {
            font-size: 15px;
            color: #111;
            font-weight: 500;
        }

        .brand-image {
            height: 56px;
            width: auto;
            object-fit: contain;
        }

        .popup-captcha {
            display: none;
            opacity: 0;
            position: absolute;
            top: 0;
            left: 0;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            width: 310px;
            text-align: center;
            background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }

        .hidden { opacity: 0 !important; pointer-events: none; transform: scale(0.95); }
        .visible { display: block !important; opacity: 1 !important; transform: scale(1); }

        canvas { border-radius: 6px; margin-bottom: 8px; image-rendering: pixelated; }
        input { width: 80%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 15px; margin-bottom: 8px; text-align: center; }
        button { padding: 8px 16px; background-color: #7042c4; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #5b34a8; }
    </style>
</head>
<body>

<div class="captcha-wrapper">
    <div class="recaptcha-box" id="recaptchaBox">
        <div class="checkbox-container" onclick="lancerChargement()">
            <div class="checkbox">
                <div class="spinner" id="captchaSpinner"></div>
                
                <svg id="iconCheck" class="status-icon" viewBox="0 0 24 24" fill="none" stroke="#4bc158" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>

                <svg id="iconCross" class="status-icon" viewBox="0 0 24 24" fill="none" stroke="#d92525" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </div>
            <span class="checkbox-label">Je ne suis pas un robot.</span>
        </div>

        <img src="https://u.cubeupload.com/Scratch_2_0_2_4/IMG4788.jpeg" alt="Logo" class="brand-image">
    </div>

    <div class="popup-captcha" id="popupCaptcha">
        <canvas id="captchaCanvas" width="280" height="130"></canvas>
        <input type="text" id="userInput" placeholder="Entrez les 4 chiffres" maxlength="4" autocomplete="off" inputmode="numeric" oninput="this.value=this.value.replace(/[^0-9]/g,'')" onkeyup="if(event.key==='Enter') validerCaptcha()">
        <br>
        <button onclick="validerCaptcha()">Valider</button>
    </div>
</div>

<script>
let codeSecret = "", estValide = false, enChargement = false;

function lancerChargement() {
    if (estValide || enChargement) return;
    enChargement = true;

    document.getElementById("iconCheck").style.display = "none";
    document.getElementById("iconCross").style.display = "none";
    document.getElementById("captchaSpinner").style.display = "block";

    setTimeout(() => {
        document.getElementById("captchaSpinner").style.display = "none";
        enChargement = false;
        document.getElementById("recaptchaBox").classList.add("hidden");

        setTimeout(() => {
            const popup = document.getElementById("popupCaptcha");
            genererCaptcha();
            popup.classList.add("visible");
            document.getElementById("userInput").focus();
        }, 200);
    }, 1000);
}

function genererCaptcha() {
    const canvas = document.getElementById("captchaCanvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    codeSecret = Math.floor(1000 + Math.random() * 9000).toString();

    for (let x = -100; x < canvas.width + 100; x += 0.5) {
        ctx.strokeStyle = `hsl(${Math.random() * 360}, 95%, 50%)`;
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(x, -10);
        ctx.lineTo(x + 90, canvas.height + 10);
        ctx.stroke();
    }

    const lowRes = document.createElement("canvas");
    lowRes.width = 140; lowRes.height = 70;
    const lowCtx = lowRes.getContext("2d");
    lowCtx.font = "900 30px sans-serif";
    lowCtx.fillStyle = "#ffaa00"; lowCtx.strokeStyle = "#000000"; lowCtx.lineWidth = 2.5;

    for (let i = 0; i < codeSecret.length; i++) {
        lowCtx.save();
        lowCtx.translate(18 + i * 27, 45 + (Math.random() * 6 - 3));
        lowCtx.rotate((Math.random() - 0.5) * 0.15);
        lowCtx.strokeText(codeSecret[i], 0, 0);
        lowCtx.fillText(codeSecret[i], 0, 0);
        lowCtx.restore();
    }

    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(lowRes, 0, 0, canvas.width, canvas.height);
}

function validerCaptcha() {
    const saisie = document.getElementById("userInput").value;
    document.getElementById("popupCaptcha").classList.remove("visible");

    setTimeout(() => {
        document.getElementById("recaptchaBox").classList.remove("hidden");

        if (saisie === codeSecret) {
            estValide = true;
            document.getElementById("iconCheck").style.display = "block";
        } else {
            document.getElementById("iconCross").style.display = "block";
        }
        document.getElementById("userInput").value = "";
    }, 300);
}
</script>

</body>
</html>
"""

if __name__ == '__main__':
    # Ouvre une vraie fenêtre de bureau avec le rendu web parfait
    window = webview.create_window("Scratch CAPTCHA", html=HTML_PAGE, width=360, height=260, resizable=False)
    webview.start()
