import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_personalized_email(times):
    # Prihlásenie k iCloud účtu
    icloud_smtp = "smtp.mail.me.com"
    icloud_port = 587
    icloud_email = "miroslav@mtvrdon.com"
    icloud_password = "wkuk-cjzr-sgji-eiad"

    recipient_email = "matkotvrdon@gmail.com"

    subject = "Miroslav Tvrdoň - IT Génius a Tím budúcnosti"

    # Pridajte svoju fotku v Base64 formáte
    with open("miro.jpg", "rb") as img_file:
        photo_base64_miro = base64.b64encode(img_file.read()).decode('utf-8')

    # Pridajte fotku ženy v Base64 formáte
    with open("zena.jpg", "rb") as img_file:
        photo_base64_zena = base64.b64encode(img_file.read()).decode('utf-8')

    # HTML obsah e-mailu
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333333;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background-color: #4caf50;
                color: #ffffff;
                padding: 15px;
                text-align: center;
                font-size: 24px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            .email-body {{
                padding: 20px;
                line-height: 1.6;
                text-align: center;
            }}
            .email-footer {{
                background-color: #f4f4f9;
                text-align: center;
                padding: 10px;
                font-size: 12px;
                color: #888888;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            .cta-button {{
                display: inline-block;
                background-color: #4caf50;
                color: #ffffff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            .profile-images {{
                margin: 20px 0;
            }}
            .profile-images img {{
                max-width: 100%;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .text-block {{
                margin: 20px 0;
                text-align: center;
                font-size: 16px;
                color: #555555;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                Miroslav Tvrdoň - IT Génius
            </div>
            <div class="email-body">
                <div class="profile-images">
                    <img src="data:image/jpeg;base64,{photo_base64_miro}" alt="Miroslav Tvrdoň" />
                </div>
                <div class="text-block">
                    <p>Som Miroslav Tvrdoň, IT génius a rozhodca, ktorý hľadá vždy najlepšie riešenia.</p>
                </div>
                <div class="profile-images">
                    <img src="data:image/jpeg;base64,{photo_base64_zena}" alt="Moja krásna žena" />
                </div>
                <div class="text-block">
                    <p>Toto je moja krásna polovička - spolu tvoríme skutočný tím snov.</p>
                </div>
                <div class="text-block">
                    <p>Spolu budeme meniť budúcnosť, jeden projekt za druhým!</p>
                </div>
                <p>
                    <a href="https://platforma.example.com" class="cta-button">Pozri našu platformu</a>
                </p>
            </div>
            <div class="email-footer">
                © 2024 Miroslav Tvrdoň | Všetky práva vyhradené.
            </div>
        </div>
    </body>
    </html>
    """

    try:
        # Nastavenie servera
        server = smtplib.SMTP(icloud_smtp, icloud_port)
        server.starttls()
        server.login(icloud_email, icloud_password)

        for i in range(times):
            # Vytvorenie e-mailu
            msg = MIMEMultipart("alternative")
            msg['From'] = icloud_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Pripojenie HTML obsahu
            msg.attach(MIMEText(body, 'html'))

            # Odoslanie e-mailu
            server.sendmail(icloud_email, recipient_email, msg.as_string())
            print(f"E-mail {i + 1}/{times} bol úspešne odoslaný!")

        server.quit()

    except Exception as e:
        print(f"Nastala chyba pri odosielaní e-mailov: {e}")


# Zavolanie funkcie so zadaným počtom opakovaní
send_personalized_email(1)  # Pošle e-mail 5-krát