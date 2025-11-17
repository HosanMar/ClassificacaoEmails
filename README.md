# Classificação de Emails – NLP com Flask + Hugging Face

Aplicação web para **classificação automática de e-mails** usando um modelo hospedado no Hugging Face, com suporte a envio de texto manual, arquivos **TXT** e **PDF**, além do retorno de **respostas automáticas pré-definidas** conforme a categoria detectada.

---

## 🧠 Tecnologias utilizadas

* **Python 3**
* **Flask** (backend / API)
* **Transformers (Hugging Face)**
* **huggingface_hub** (autenticação via token)
* **PyPDF2** (extração de texto de PDFs)
* **Docker** (opcional)

---

## 📂 Estrutura do projeto

```
.
├─ app.py               # API Flask com rotas / e /classify
├─ classifier.py        # Pipeline Hugging Face + respostas automáticas
├─ requirements.txt     # Dependências do projeto
├─ Dockerfile           # Deploy em container
├─ templates/
│   └─ index.html       # Página inicial com upload de arquivo e formulário
└─ LICENSE              # GPL-3.0
```

---

## 🚀 Funcionalidades

* Classificação automática de e-mails em **Produtivo** ou **Improdutivo**.
* Upload de arquivos **.txt** e **.pdf**.
* Entrada direta de texto pelo formulário.
* Modelo carregado via **Hugging Face Hub**.
* Seleção aleatória de **3 respostas sugeridas** para cada categoria.
* Retorno em JSON via API.

---

## 🔧 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/HosanMar/ClassificacaoEmails.git
cd ClassificacaoEmails
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate      # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a variável de ambiente com seu token do Hugging Face

```bash
export HF_TOKEN="seu_token_aqui"
```

### 5. Execute o servidor

```bash
python app.py
```

A aplicação ficará acessível em:

```
http://127.0.0.1:8080
```

---

## 🧪 API – Como usar

### Endpoint: **POST /classify**

#### Envio de texto (form-data)

```bash
curl -X POST http://localhost:8080/classify \
  -F "texto=Olá, gostaria de atualizar o chamado #123"
```

#### Envio de arquivo TXT/PDF (form-data)

```bash
curl -X POST http://localhost:8080/classify \
  -F "arquivo=@meu_email.pdf"
```

### Resposta (JSON)

```json
{
  "categoria": "Produtivo",
  "respostas": [
    "Obrigado pelo envio! Iremos analisar sua solicitação e responder em breve.",
    "Recebido! Vamos verificar e dar um retorno assim que possível.",
    "Mensagem recebida. Em breve retornaremos com os próximos passos."
  ]
}
```

---

## 🧱 Como funciona internamente

### `classifier.py`

* Faz login automático no Hugging Face caso **HF_TOKEN** esteja configurado.
* Carrega o modelo:

```python
classifier = pipeline(
    "text-classification",
    model="NoahGalDRiel/meu-repo",
    devices=0
)
```

* Usa dicionários de respostas automáticas:

```python
RESPOSTAS["Produtivo"]
RESPOSTAS["Improdutivo"]
```

* Retorna a categoria + 3 respostas aleatórias.

---

### `app.py`

* Página principal: `GET /`
* API de classificação: `POST /classify`
* Extrai texto de:

  * Formulário
  * Arquivo `.txt`
  * Arquivo `.pdf` via `PyPDF2`
* Chama:

```python
categoria, detalhes = classify_text(texto)
```

* Retorna JSON com categoria e respostas.

---

## 🐳 Deploy com Docker

### Construir imagem

```bash
docker build -t classificacao-emails .
```

### Rodar container

```bash
docker run -d -p 8080:8080 \
  -e HF_TOKEN="seu_token" \
  classificacao-emails
```

---

## 🌐 Deploy no Hugging Face Spaces (opcional)

Você pode subir este projeto como:

### ✅ **Space tipo Docker**

* Basta enviar `Dockerfile`, `requirements.txt`, `app.py` e `classifier.py`.

OU

### 🔄 Adaptar para Gradio/Streamlit

* Caso deseje interface visual automática.

Se quiser, eu preparo a versão pronta para **Hugging Face Spaces** (Docker ou Gradio).

---

## 📜 Licença

Este projeto está licenciado sob **GPL-3.0**.
Confira o arquivo `LICENSE` para mais detalhes.

---

## 📩 Contato

Caso queira ajuda para melhorar a UI, criar logs, métricas, treinar seu próprio modelo ou integrar banco de dados, posso ajudar!



Só pedir!
