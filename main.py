import requests

# App word opgebouwd in verschillende handige functies

# functie 1 Maaltijd of ingredient opzoeken
# Gebruiker typt in bijvoorbeeld kipfilet of banaan
# Gebruiker krijgt voedingswaarden terug per 100g opgedeeld in KCAL, EIWITTEN, VETTEN EN KOOLHYDRATEN

def zoekfunctie(zoekterm):
    url = f"https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": zoekterm,
        "search_simple": 1,
        "action": "process",
        "json": 1,
    }
    response = requests.get(url, params=params)
    data = response.json()

    producten = data.get("products", [])
    for product in producten[:1]:
        naam = product.get("product_name")
        merken = product.get("brands")
        macros = product.get("nutriments")
        print(f"{naam}, ({merken})")
        print(f"Calorieën: {macros.get("energy-kcal_100g")} kcal per 100g")
        print(f"Eiwit: {macros.get("proteins_100g")}g")
        print(f"Koolhydraten {macros.get("carbohydrates_100g")}g")
        print(f"Vetten: {macros.get("fat_100g")}g")

zoekfunctie("kipfilet")

# functie 2 dagelijkse totaalwaarden berekenen
# Voeg meerdere maaltijden toe en houd dagtotaal bij
# Wederom opgedeeld in KCAL, EIWITTEN, VETTEN EN KOOLHYDRATEN

# functie 3 Opslaan van dagelijkse voeding in een lokaal bestaand
# bijhouden wat je vandaag en op eerdere dagen heb gegeten

# functie 4 persoonlijke macrodoelen instellen
# De app vergelijkt je huidige dagtotaal en berekend hoeveel je nog moet eten

# Daarnaast moet er ook een command line menu komen om de functies aan te roepen en terug te keren naar het menu!

# Wellicht leuke functionaliteit bij het opstarten van de app een 