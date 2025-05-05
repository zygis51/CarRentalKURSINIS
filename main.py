from failo_apdorojimas import DuomenuTvarkytuvas
from klientas import Klientas

def rodyti_pagrindini_menu():
    print("\n=== AUTOMOBILIŲ NUOMOS SISTEMA ===")
    print("1. Peržiūrėti visas transporto priemones")
    print("2. Peržiūrėti laisvas transporto priemones")
    print("3. Išnuomoti transporto priemonę")
    print("4. Peržiūrėti klientų nuomas")
    print("5. Išsaugoti duomenis ir išeiti")

def main():
    tvarkytuvas = DuomenuTvarkytuvas()
    
    # Užkrauname transporto priemones
    transporto_priemones = tvarkytuvas.sukurti_transporto_priemones_is_csv('transporto_priemones.csv')
    print(f"\nUžkrautos {len(transporto_priemones)} transporto priemonės")
    
    # Užkrauname klientus
    klientai = tvarkytuvas.sukurti_klientus_is_csv('klientu_nuomos.csv', transporto_priemones)
    print(f"Užkrauti {len(klientai)} klientai su nuomomis")
    
    while True:
        rodyti_pagrindini_menu()
        pasirinkimas = input("Pasirinkite veiksmą (1-5): ")
        
        if pasirinkimas == '1':
            print("\nVisos transporto priemonės:")
            for i, priemone in enumerate(transporto_priemones, 1):
                print(f"{i}. {priemone.gauti_info()} | Būsena: {priemone.ar_isnuomota()}")
        
        elif pasirinkimas == '2':
            print("\nLaisvos transporto priemonės:")
            laisvos = [p for p in transporto_priemones if not p._is_nuomota]
            for i, priemone in enumerate(laisvos, 1):
                print(f"{i}. {priemone.gauti_info()}")
        
        elif pasirinkimas == '3':
            print("\nNauja nuoma:")
            vardas = input("Įveskite savo vardą: ")
            klientas = next((k for k in klientai if k.vardas == vardas), None)
            
            if not klientas:
                klientas = Klientas(vardas)
                klientai.append(klientas)
                print(f"Naujas klientas {vardas} sukurtas.")
            
        
            visos_markes = tvarkytuvas.gauti_visas_markes(transporto_priemones)
            print("\nGalimos markės:")
            for i, marke in enumerate(visos_markes, 1):
                print(f"{i}. {marke}")
            
            try:
                markes_pasirinkimas = int(input("Pasirinkite markės numerį: ")) - 1
                if markes_pasirinkimas < 0 or markes_pasirinkimas >= len(visos_markes):
                    print("Netinkamas pasirinkimas!")
                    continue
                    
                pasirinkta_marke = visos_markes[markes_pasirinkimas]
                filtruotos_priemones = tvarkytuvas.filtruoti_priemones_pagal_marke(transporto_priemones, pasirinkta_marke)
                
                if not filtruotos_priemones:
                    print(f"Nėra laisvų {pasirinkta_marke} markės transporto priemonių.")
                    continue
                    
                rezultatas = tvarkytuvas.interaktyvi_nuoma(filtruotos_priemones)
                if rezultatas:
                    priemone, laikotarpis = rezultatas
                    klientas.prideti_nuoma(priemone, laikotarpis)
                    print(f"\nSėkmingai išnuomota: {priemone.gauti_info()}")
                    print(f"Nuomos laikotarpis: {laikotarpis}")
                    
            except ValueError:
                print("Įveskite skaičių!")
        
        elif pasirinkimas == '4':
            print("\nKlientų nuomos:")
            for klientas in klientai:
                klientas.parodyti_nuomas()
        
        elif pasirinkimas == '5':
            tvarkytuvas.issaugoti_klientus_i_csv(klientai, 'visos_nuomos.csv')
            print("Duomenys išsaugoti. Programa baigia darbą.")
            break
        
        else:
            print("Netinkamas pasirinkimas. Bandykite dar kartą.")

if __name__ == "__main__":
    main()