from transformers import pipeline
import random
import os
from huggingface_hub import login

# Login no HuggingFace via variável de ambiente
hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(token=hf_token)

classifier = pipeline(
    "text-classification",
    model="NoahGalDRiel/meu-repo",
    devices=0
)


# Respostas pré-definidas para cada categoria
RESPOSTAS = {
    "Produtivo": [
        "Obrigado pelo envio! Iremos analisar sua solicitação e responder em breve.",
        "Recebido! Vamos verificar e dar um retorno assim que possível.",
        "Sua mensagem foi recebida. Entraremos em contato com a solução ou esclarecimento necessário.",
        "Agradecemos o envio. Nossa equipe vai tomar as providências necessárias.",
        "Mensagem recebida. Em breve retornaremos com os próximos passos."
    ],
    "Improdutivo": [
        "Obrigado pela mensagem! Apreciamos seu contato.",
        "Recebido! Ficamos felizes com seu retorno.",
        "Agradecemos a mensagem e ficamos à disposição.",
        "Obrigado pelo envio! Que bom saber disso.",
        "Mensagem recebida! Agradecemos a gentileza."
    ]
}

def classify_text(text):
    result = classifier(text)

    # Garante que result seja um único dicionário
    if isinstance(result, list):
        if isinstance(result[0], list):   # caso raro: lista de listas
            result = result[0][0]
        else:
            result = result[0]
    else:
        result = result

    categoria = result["label"]  # "Produtivo" ou "Improdutivo"
    score = result["score"]

    respostas = random.sample(RESPOSTAS[categoria], k=3)

    return categoria, {"score": score, "resposta": respostas}




