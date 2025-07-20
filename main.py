import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
base_url = "https://api.api-ninjas.com/v1/caloriesburned"

# Lege lijst voor het opslaan van voeding buiten de scope van de functie
opgeslagen_voeding = []
# Zoeken en opslaan
def zoekfunctie(zoekterm):
    # probleem met programma dat er soms ook franse en duitse producten doorheen komen op keywords als ei en patat, countries param lost dit op
    url = "https://world.openfoodfacts.org/cgi/search.pl"
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
    #Filteren van alleen de eerste 3 resultaten, anders laat api alle resultaten zien wat een enorme waslijst aan keuze geeft voor de gebruiker
    keuzes = []
    for x, product in enumerate(producten[:3], start=1):
        naam = product.get("product_name")
        macros = product.get("nutriments")

        kcal = float(macros.get("energy-kcal_100g", 0))
        eiwit = float(macros.get("proteins_100g", 0))
        koolhydraten = float(macros.get("carbohydrates_100g", 0))
        vetten = float(macros.get("fat_100g", 0))
        print(f"{x}. {naam}\n{kcal} kcal per 100g\n{eiwit} eiwit per 100g\n{koolhydraten} koolhydraten per 100g\n{vetten} vetten per 100g\n-----")

        keuzes.append({
            "naam": naam,
            "kcal_per_100g": kcal,
            "eiwit_per_100g": eiwit,
            "kh_per_100g": koolhydraten,
            "vet_per_100g": vetten,
        })

    
    # Keuze van gebruiker krijgen om op te slaan 
    keuze = input("Kies een nummer om op te slaan (of druk op enter om te annuleren): ")
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


# Dagoverzicht functie 
def toon_dagoverzicht():
    print("\nDagoverzicht: ")
    totaal_kcal = 0
    totaal_eiwit = 0
    totaal_kh = 0
    totaal_vet = 0

    for item in opgeslagen_voeding:
        print(f"{item["naam"]} ({item["gram"]}g): {item["kcal"]}kcal, {item["eiwit"]}g eiwit, {item["kh"]}g koolhydraten, {item["vet"]}g vet")
        # Het optellen van het aantal nutrients aan dagoverzicht
        totaal_kcal += item["kcal"]
        totaal_eiwit += item["eiwit"]
        totaal_kh += item["kh"]
        totaal_vet += item["vet"]

    print(f"\nTotaal: {round(totaal_kcal,1)} kcal | {round(totaal_eiwit,1)}g eiwit | {round(totaal_kh,1)}g kh | {round(totaal_vet,1)}g vet\n")

    return totaal_kcal #Geeft het totaal door aan de berekenen beweging functie

#Functie om kcal per uur op te halen
def get_kcal_per_uur(activiteit, gewicht, duur):
    response = requests.get(
            base_url,
            headers={"X-Api-Key": API_KEY},
            params={"activity": activiteit,
                    "weight": gewicht,
                    "duration": duur,
                }
        )
    
    data = response.json()
    if not data:
        return None
    
    item = data[0]
    # Het ophalen van calorieén per uur
    if "calories_per_hour" in item:
        try:
            return float(item["calories_per_hour"])
        except (TypeError, ValueError):
            pass
    # Het ophalen van totale calorieén 
    if "total_calories" in item:
        try:
            totaal = float(item["total_calories"])
            return (totaal / duur) * 60
        except (TypeError, ValueError):
            pass

#Berekenen hoeveelheid beweging functie
def berekenen_beweging(kcal):
    if kcal == 0:
        print("Geen calorieën om te verbranden")
        return
    
    try:
        gewicht = float(input("Wat is je gewicht in kg?: "))
    except ValueError:
        print("Ongeldige invoer!!!")
        return
    
    activiteiten = ["running", "cycling", "walking"]

    print("\nbeweging om je calorieën te verbranden")
    for activiteit in activiteiten:
        kcal_per_uur = get_kcal_per_uur(activiteit, gewicht, duur=60)
        if not kcal_per_uur or kcal_per_uur <= 0:
            print(f"- {activiteit.title()}: geen data.")
    
        minuten = round((float(kcal) / float(kcal_per_uur)) * 60)
        print(f"- {activiteit.title()}: {minuten} min")
        

#Hoofdmenu met ValueError
while True:
    try:
        keuze = int(input("\nKies een optie:\n1. Zoeken en opslaan voeding\n2. Toon dagoverzicht\n3. Bereken beweging voor vandaag\n4. Stop\n"))
        if keuze == 1:
            zoekterm = input("Voer een productnaam in: ")
            zoekfunctie(zoekterm)
        elif keuze ==2:
            toon_dagoverzicht()
        elif keuze == 3:
            totaal_kcal = toon_dagoverzicht()
            berekenen_beweging(totaal_kcal)
        elif keuze == 4:
            print("Tot de volgende keer!")
            break
        else:
            print("\nvoer een geldige keuze in")
    except ValueError:
        print("\nGebruik een cijfer!!!")
    