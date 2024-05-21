from SPARQLWrapper import SPARQLWrapper, POST, JSON, RDFXML

sparql = SPARQLWrapper("http://localhost:7200/repositories/doencas")


namespace = "http://www.example.org/disease-ontology#"


query = f"""
PREFIX : <{namespace}>

CONSTRUCT {{
  ?patient :hasDisease ?disease .
}}
WHERE {{
  ?patient a :Patient .
  ?disease a :Disease .
  # Select diseases only if the patient exhibits all required symptoms
  FILTER NOT EXISTS {{
    ?disease :hasSymptom ?requiredSymptom .
    FILTER NOT EXISTS {{
      ?patient :exhibitsSymptom ?requiredSymptom .
    }}
  }}
}}
"""

# Set up the query
sparql.setQuery(query)
sparql.setMethod(POST)
sparql.setReturnFormat(RDFXML) 


results = sparql.query().convert()


update_sparql = SPARQLWrapper("http://localhost:7200/repositories/doencas/statements")
update_sparql.setMethod(POST)
update_sparql.setCredentials('username', 'password')  


update_query = f"""
PREFIX : <{namespace}>
INSERT DATA {{
  GRAPH <{namespace}> {{
    {results.serialize(format='nt')}
  }}
}}
"""


update_sparql.setQuery(update_query)
update_sparql.query()

print("Update completed successfully.")
