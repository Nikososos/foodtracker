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
        "countries": "Netherlands"
    }
    response = requests.get(url, params=params)
    data = response.json()
    producten = data.get("products", [])

    if not producten:
        print("Resultaat niet gevonden")
        return

    print("Resultaten!")
    keuzes = []
    for x, product in enumerate(producten[:3], start=1):
        naam = product.get("product_name")
        macros = product.get("nutriments")
        calories = macros.get("energy-kcal_100g")
        eiwit = macros.get("proteins_100g")
        koolhydraten = macros.get("carbohydrates_100g")
        vetten = macros.get("fat_100g")
        print(f"{x}. {naam}\n{calories} kcal per 100g\n{eiwit} eiwit per 100g\n{koolhydraten} koolhydraten per 100g\n{vetten} vetten per 100g\n-----")
        
zoekfunctie("eieren")

#probleem met programma dat er soms ook franse en duitse producten doorheen komen op keywords als ei en patat

# functie 2 Opslaan van dagelijkse voeding in een lokaal bestaand
# bijhouden wat je vandaag en op eerdere dagen heb gegeten
# Dit ga ik bouwen in de zoekfunctie zodat er direct opgeslagen kan worden

# functie 2 dagelijkse totaalwaarden berekenen
# Voeg meerdere maaltijden toe en houd dagtotaal bij
# Wederom opgedeeld in KCAL, EIWITTEN, VETTEN EN KOOLHYDRATEN

# functie 3 Opslaan van dagelijkse voeding in een lokaal bestaand
# bijhouden wat je vandaag en op eerdere dagen heb gegeten

# functie 4 persoonlijke macrodoelen instellen
# De app vergelijkt je huidige dagtotaal en berekend hoeveel je nog moet eten

# Daarnaast moet er ook een command line menu komen om de functies aan te roepen en terug te keren naar het menu!

# Wellicht leuke functionaliteit bij het opstarten van de app een 