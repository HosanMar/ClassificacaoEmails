from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import evaluate

# 1. Carregar dataset
dataset = load_dataset("csv", data_files="dataset.csv")

# 2. Converter labels para números
label2id = {"Produtivo": 0, "Improdutivo": 1}
id2label = {0: "Produtivo", 1: "Improdutivo"}

def encode_labels(example):
    example["label"] = label2id[example["categoria"]]
    return example

dataset = dataset.map(encode_labels)

# 3. Tokenizador
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(example):
    return tokenizer(example["texto"], padding="max_length", truncation=True)

tokenized = dataset.map(tokenize, batched=True)

# 4. Modelo
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    id2label=id2label,
    label2id=label2id
)

# 5. Métrica
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = logits.argmax(axis=-1)
    return accuracy.compute(predictions=predictions, references=labels)

# 6. Configuração do treinamento
training_args = TrainingArguments(
    output_dir="./modeloTreinado",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch"
)

# 7. Treinador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["train"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# 8. Treinar
trainer.train()

# 9. Salvar
trainer.save_model("./modeloTreinado")
tokenizer.save_pretrained("./modeloTreinado")
