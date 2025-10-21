from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = (
    "troque_essa_chave_por_uma_variavel_ambiente"  # em produção use ENV var
)

# Banco simples em memória só para teste
usuarios = {"teste": generate_password_hash("1234")}


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        p = request.form.get("password", "")
        if u in usuarios and check_password_hash(usuarios[u], p):
            session["user"] = u
            return redirect(url_for("painel"))
        else:
            error = "Usuário ou senha inválidos."
    return render_template("login.html", error=error)


@app.route("/painel")
def painel():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("painel.html", user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
