from rdflib import Graph

g = Graph()

# 1. Load files with error checking
try:
    g.parse("energy.ttl", format="turtle")
    g.parse("household_case1.ttl", format="turtle")
    print("Files loaded successfully!")
except Exception as e:
    print(f"Error parsing Turtle files: {e}")

# 2. Execute Query
# Updated Query to catch more items and handle missing units gracefully
query = """
PREFIX energysource: <https://ugentbiomath.github.io/ontology/energy.ttl#>
PREFIX wf: <https://ugentbiomath.github.io/waterframe#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX qudt: <http://qudt.org/schema/qudt/>

SELECT ?compLabel ?energyReading ?unit
WHERE {
    ?component a ?wfClass .
    ?component rdfs:label ?compLabel .
    
    # Mapping Table
    VALUES (?wfClass ?energyClass) {
        (wf:BoosterPumpUnit energysource:BoosterPumping)
        (wf:MembraneBioreactorUnit energysource:MembraneBio_Reactors)
        (wf:ReverseOsmosisUnit energysource:ReverseOsmosis)
        (wf:CirculationPumpUnit energysource:DistributionPumping)
        # Add more mappings here as your energy.ttl grows
    }
    
    # Find the energy reading through the restriction
    ?energyClass rdfs:subClassOf ?restriction .
    ?restriction a owl:Restriction ;
                 owl:onProperty energysource:hasEnergyConsumption ;
                 owl:hasValue ?energyReading .
    
    # Unit is optional in case some readings don't have them yet
    OPTIONAL { ?energyReading qudt:unit ?unit . }
}
"""