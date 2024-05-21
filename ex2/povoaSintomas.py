import csv
from rdflib import Graph, URIRef, Namespace, RDF, RDFS

# Load existing ontology from Turtle file
g = Graph()
g.parse('medical.ttl', format='turtle')

# Setting up namespaces
NS = Namespace("http://www.example.org/disease-ontology#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Define URI for the classes and properties
Disease = URIRef(NS.Disease)
Symptom = URIRef(NS.Symptom)
hasSymptom = URIRef(NS.hasSymptom)

# Read new data from the CSV file and populate the graph
with open('Disease_Syntoms.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease_name = row['Disease'].strip()
        if disease_name:
            disease_uri = URIRef(NS[disease_name.replace(" ", "")])
            if not (disease_uri, RDF.type, Disease) in g:
                g.add((disease_uri, RDF.type, Disease))
            for key, value in row.items():
                if key.startswith('Symptom') and value.strip():
                    symptom_name = value.strip()
                    symptom_uri = URIRef(NS[symptom_name.replace(" ", "_").replace("__", "_")])
                    if not (symptom_uri, RDF.type, Symptom) in g:
                        g.add((symptom_uri, RDF.type, Symptom))
                    g.add((disease_uri, hasSymptom, symptom_uri))

# Serialize the graph to Turtle format and save it back to file
with open('med_doencas.ttl', 'w', encoding='utf-8') as file:
    file.write(g.serialize(format='turtle'))

