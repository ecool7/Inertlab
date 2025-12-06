from flask import Flask, render_template, abort, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Загружает переменные из .env файла (если доступен)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Если dotenv не установлен, используем только переменные окружения
    pass


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # Simple in-memory catalog
    PRODUCTS = [
        {
            "slug": "БЧЭ1",
            "name": "БЧЭ1",
            "series": "Series S",
            "tagline": "Малогабаритный инерцилальный модуль для БПЛА",
            "specs": {
                "Гироскоп, макс. диапазон": "±4000 °/s",
                "Нестабильность смещения нуля в запуске(гироскопа)": "≤ 3 °/ч",
                "Спектральная плотность шума гироскопа": "≤ 0.005 °/c/√Гц",
                "Акселерометр, макс. диапазон": "±16 g",
                "Нестабильность смещения нуля в запуске (акселерометра)": "≤ 0.01 mg",
                "Спектральная плотность шума акселерометра": "≤ 60 мкg/c/√Гц",
                "Интерфейсы": "UART",
                "Питание": "3.3 V",
                "Рабочая температура": "-40…+85 °C",
            },
            "images": [
                "/static/assets/BCHE1.jpg"
            ],
            "datasheet": "БЧЭ 1.pdf",
            "model3d": None,  # Например: "bche1.gltf" или "bche1.glb" - файл должен быть в static/models/
        }
        
    ]

    app.config["PRODUCTS"] = PRODUCTS
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Gmail SMTP настройки (из переменных окружения)
    app.config["MAIL_SMTP_SERVER"] = os.environ.get("MAIL_SMTP_SERVER", "smtp.gmail.com")
    app.config["MAIL_SMTP_PORT"] = int(os.environ.get("MAIL_SMTP_PORT", "587"))
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
    app.config["MAIL_TO"] = os.environ.get("MAIL_TO", "")  # Email куда приходят заявки

    def send_email(name, email, message):
        """Отправка письма через Gmail SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = app.config["MAIL_USERNAME"]
            msg['To'] = app.config["MAIL_TO"]
            msg['Subject'] = f"Новая заявка с сайта Inertlab от {name}"
            
            body = f"""
Имя: {name}
Email: {email}

Сообщение:
{message}
"""
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(app.config["MAIL_SMTP_SERVER"], app.config["MAIL_SMTP_PORT"])
            server.starttls()
            server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            text = msg.as_string()
            server.sendmail(app.config["MAIL_USERNAME"], app.config["MAIL_TO"], text)
            server.quit()
            return True
        except Exception as e:
            print(f"Ошибка отправки email: {e}")
            return False

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/products")
    def products():
        return render_template("products.html", products=app.config["PRODUCTS"])

    @app.get("/products/<path:slug>")
    def product_detail(slug: str):
        # Декодируем slug если нужно
        from urllib.parse import unquote
        slug = unquote(slug)
        product = next((p for p in app.config["PRODUCTS"] if p["slug"] == slug), None)
        if not product:
            abort(404)
        return render_template("product_detail.html", product=product)

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            message = request.form.get("message", "").strip()
            
            if not name or not email or not message:
                flash("Пожалуйста, заполните все поля", "error")
                return render_template("contact.html")
            
            if not app.config["MAIL_USERNAME"] or not app.config["MAIL_PASSWORD"]:
                flash("Форма временно недоступна. Пожалуйста, свяжитесь с нами по email: info.inertlab@gmail.com", "error")
                return render_template("contact.html")
            
            if send_email(name, email, message):
                flash("Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.", "success")
                return redirect(url_for("contact"))
            else:
                flash("Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже или напишите на info.inertlab@gmail.com", "error")
                return render_template("contact.html")
        
        return render_template("contact.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


