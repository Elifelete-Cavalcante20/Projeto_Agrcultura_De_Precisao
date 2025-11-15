import json


with open("dicas.json", "r", encoding="utf-8") as f:
    dicas = json.load(f)

classe_predita = "Maçã - Sarna da maçã"
print(dicas[classe_predita])