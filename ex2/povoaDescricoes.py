import csv
from rdflib import Graph, URIRef, Namespace, Literal, RDF, RDFS

# Load the ontology that includes the latest changes
g = Graph()
g.parse('med_doencas.ttl', format='turtle')

# Define the namespace
NS = Namespace("http://www.example.org/disease-ontology#")

# Define new property
hasDescription = URIRef(NS.hasDescription)

# Read the disease descriptions from CSV and update the ontology
with open('Disease_Description.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        disease_name = row['Disease'].strip()
        description = row['Description'].strip() if 'Description' in row else ''
        disease_uri = URIRef(NS[disease_name.replace(" ", "")])

        # Only add the description if the disease exists in the ontology
        if (disease_uri, RDF.type, URIRef(NS.Disease)) in g:
            g.add((disease_uri, hasDescription, Literal(description)))

# Serialize and save the updated ontology
with open('med_doencas.ttl', 'w', encoding='utf-8') as file:
    file.write(g.serialize(format='turtle'))
