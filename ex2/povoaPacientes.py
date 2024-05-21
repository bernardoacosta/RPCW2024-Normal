import json
from rdflib import Graph, URIRef, Literal, Namespace

EX = Namespace("http://www.example.org/disease-ontology#")


g = Graph()
g.parse("med_doencas.ttl", format="turtle")


def sanitize_for_uri(value):
    return value.replace(" ", "_").replace("(", "").replace(")", "").replace(",", "_").lower()


with open('pg53699.json', 'r') as file:
    patients = json.load(file)


for idx, patient in enumerate(patients):
    patient_node = URIRef(f"http://www.example.org/disease-ontology#Patient{idx+1}")
    g.add((patient_node, EX.name, Literal(patient["nome"])))
    for symptom in patient["sintomas"]:
        sanitized_symptom = sanitize_for_uri(symptom)
        g.add((patient_node, EX.exhibitsSymptom, EX[sanitized_symptom]))


with open("med_doente.ttl", "w") as output_file:
    output_file.write(g.serialize(format="turtle"))
