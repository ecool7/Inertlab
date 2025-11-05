from flask import Flask, render_template, abort


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
        }
        
    ]

    app.config["PRODUCTS"] = PRODUCTS

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/products")
    def products():
        return render_template("products.html", products=app.config["PRODUCTS"])

    @app.get("/products/<slug>")
    def product_detail(slug: str):
        product = next((p for p in app.config["PRODUCTS"] if p["slug"] == slug), None)
        if not product:
            abort(404)
        return render_template("product_detail.html", product=product)

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/contact")
    def contact():
        return render_template("contact.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


