import os
from flask import Flask, request, render_template, jsonify
import PyPDF2
from classifier import classify_text

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    try:
        texto = ""
        # Verifica se enviou arquivo
        if "arquivo" in request.files and request.files["arquivo"].filename != "":
            arquivo = request.files["arquivo"]
            if arquivo.filename.endswith(".txt"):
                texto = arquivo.read().decode("utf-8")
            elif arquivo.filename.endswith(".pdf"):
                reader = PyPDF2.PdfReader(arquivo)
                texto = "\n".join([p.extract_text() or "" for p in reader.pages])
        else:
            texto = request.form.get("texto", "").strip()

        if not texto:
            return jsonify({"error": "Nenhum texto enviado"}), 400

        categoria, detalhes = classify_text(texto)

        # Retorna categoria e lista de respostas (mesmo que seja 1)
        return jsonify({
            "categoria": categoria,
            "respostas": [detalhes["resposta"]] if "resposta" in detalhes else []
        })

    except Exception as e:
        print("Erro no backend:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


