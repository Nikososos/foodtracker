import requests

# App word opgebouwd in verschillende handige functies

# functie 1 Maaltijd of ingredient opzoeken
# Gebruiker typt in bijvoorbeeld kipfilet of banaan
# Gebruiker krijgt voedingswaarden terug per 100g opgedeeld in KCAL, EIWITTEN, VETTEN EN KOOLHYDRATEN

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

opgeslagen_voeding = []

def zoekfunctie(zoekterm):
    #probleem met programma dat er soms ook franse en duitse producten doorheen komen op keywords als ei en patat, countries param lost dit op
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

        calories = float(macros.get("energy-kcal_100g"))
        eiwit = float(macros.get("proteins_100g"))
        koolhydraten = float(macros.get("carbohydrates_100g"))
        vetten = float(macros.get("fat_100g"))
        print(f"{x}. {naam}\n{calories} kcal per 100g\n{eiwit} eiwit per 100g\n{koolhydraten} koolhydraten per 100g\n{vetten} vetten per 100g\n-----")

        keuzes.append({
            "naam": naam,
            "kcal_per_100g": calories,
            "eiwit_per_100g": eiwit,
            "kh_per_100g": koolhydraten,
            "vet_per_100g": vetten,
        })

    
    # Keuze van gebruiker krijgen om op te slaan 
    keuze = input("Kies een nummer om op te slaan (of druk op enter om te annuleren): ")
    # Hier zit een probleem dat nog gefixed moet worden
    if keuze.isdigit() and 1 <= int(keuze) <= len(keuzes):
        gekozen = keuzes[int(keuze)-1]
        try:
            gram = float(input("Hoeveel gram heb je gegeten?: "))
        except ValueError:
            print("Ongeldige invoer")
            return
    
        #Voeding berekenen op basis van ingevoerde gegevens
        
        factor = gram / 100
        opgeslagen_voeding.append({
            "naam": gekozen["naam"],
            "gram": gram,
            "kcal": round(gekozen["kcal_per_100g"] * factor, 1),
            "eiwit": round(gekozen["eiwit_per_100g"] * factor, 1),
            "kh": round(gekozen["kh_per_100g"] * factor, 1),
            "vet": round(gekozen["vet_per_100g"] * factor, 1),
        })
        print(f"{gram}g gekozen {naam} opgeslagen!")
    else:
        print("Geen selectie opgeslagen")

def toon_dagoverzicht():
    print("\nDagoverzicht: ")

while True:
    keuze = int(input("\n Kies een optie:\n1. zoeken en opslaan voeding\n2. Toon dagoverzicht\n3. Stop\n"))
    if keuze == 1:
        zoekterm = input("Voer een productnaam in: ")
        zoekfunctie(zoekterm)
    elif keuze ==2:
        toon_dagoverzicht()
    elif keuze == 3:
        print("Tot de volgende keer!")
        break
    else:
        print("voer een geldige keuze in")
    