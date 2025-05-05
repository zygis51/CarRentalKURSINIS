import csv
from datetime import datetime
from transporto_priemone import TransportoPriemoniuGamykla, Automobilis, Mikroautobusas

class DuomenuTvarkytuvas:
    def __init__(self):
        self.gamykla = TransportoPriemoniuGamykla()
        self.LAIKOTARPIAI = {
            '1': '1 diena (50€)',
            '2': '3 dienos (120€)',
            '3': '1 savaitė (250€)',
            '4': '2 savaitės (450€)',
            '5': '1 mėnuo (800€)'
        }
    
    def sukurti_transporto_priemones_is_csv(self, failo_pavadinimas):
        priemones = []
        
        try:
            with open(failo_pavadinimas, 'r', encoding='utf-8') as failas:
                skaityti = csv.DictReader(failas)
                
                for eilute in skaityti:
                    try:
                        tipas = eilute['tipas']
                        marke = eilute['marke']
                        numeris = eilute['numeris']
                        metai = int(eilute['metai'])
                        is_nuomota = eilute['is_nuomota'].strip().lower() == 'taip'
                        
                        if tipas == 'automobilis':
                            durys = int(eilute['durys'])
                            priemone = self.gamykla.sukurti_transporto_priemone(
                                tipas, numeris=numeris, marke=marke, metai=metai,
                                durys=durys, is_nuomota=is_nuomota)
                        elif tipas == 'mikroautobusas':
                            vietos = int(eilute['vietos'])
                            priemone = self.gamykla.sukurti_transporto_priemone(
                                tipas, numeris=numeris, marke=marke, metai=metai,
                                vietos=vietos, is_nuomota=is_nuomota)
                        
                        priemones.append(priemone)
                    
                    except (ValueError, KeyError) as e:
                        print(f"Klaida apdorojant eilutę: {eilute}. Klaida: {e}")
                        continue
        
        except FileNotFoundError:
            print(f"Failas {failo_pavadinimas} nerastas!")
        
        return priemones
    
    def sukurti_klientus_is_csv(self, failo_pavadinimas, transporto_priemones):
        klientai = {}
        
        try:
            with open(failo_pavadinimas, 'r', encoding='utf-8') as failas:
                skaityti = csv.DictReader(failas)
                
                for eilute in skaityti:
                    try:
                        vardas = eilute['vardas']
                        numeris = eilute['numeris']
                        
                        priemone = next((p for p in transporto_priemones if p._numeris == numeris), None)
                        
                        if priemone:
                            if vardas not in klientai:
                                klientai[vardas] = Klientas(vardas)
                            klientai[vardas].prideti_nuoma(priemone)
                        else:
                            print(f"Transporto priemonė su numeriu {numeris} nerasta")
                    
                    except (KeyError, ValueError) as e:
                        print(f"Klaida apdorojant eilutę: {eilute}. Klaida: {e}")
                        continue
        
        except FileNotFoundError:
            print(f"Failas {failo_pavadinimas} nerastas!")
        
        return list(klientai.values())
    
    def issaugoti_klientus_i_csv(self, klientai, failo_pavadinimas):
        with open(failo_pavadinimas, 'w', newline='', encoding='utf-8') as failas:
            rasyti = csv.writer(failas)
            rasyti.writerow(['vardas', 'tipas', 'marke', 'numeris', 'metai', 'spec', 'is_nuomota', 'data'])
            
            for klientas in klientai:
                for nuoma in klientas.nuomos:
                    if isinstance(nuoma, Automobilis):
                        rasyti.writerow([
                            klientas.vardas,
                            'Automobilis',
                            nuoma._marke,
                            nuoma._numeris,
                            nuoma._metai,
                            nuoma._durys,
                            nuoma.ar_isnuomota(),
                            datetime.now().strftime('%Y-%m-%d')
                        ])
                    elif isinstance(nuoma, Mikroautobusas):
                        rasyti.writerow([
                            klientas.vardas,
                            'Mikroautobusas',
                            nuoma._marke,
                            nuoma._numeris,
                            nuoma._metai,
                            nuoma._vietos,
                            nuoma.ar_isnuomota(),
                            datetime.now().strftime('%Y-%m-%d')
                        ])
    
    def gauti_visas_markes(self, transporto_priemones):
        return sorted(list({p._marke for p in transporto_priemones}))
    
    def filtruoti_priemones_pagal_marke(self, transporto_priemones, marke):
        return [p for p in transporto_priemones if p._marke == marke and not p._is_nuomota]
    
    def interaktyvi_nuoma(self, transporto_priemones):
        if not transporto_priemones:
            print("Nėra transporto priemonių pasirinkimui.")
            return None
        
        print("\n=== Galimos transporto priemonės nuomai ===")
        for i, priemone in enumerate(transporto_priemones, 1):
            print(f"{i}. {priemone.gauti_info()}")
        
        try:
            pasirinkimas = int(input("\nPasirinkite transporto priemonę: ")) - 1
            if pasirinkimas < 0 or pasirinkimas >= len(transporto_priemones):
                print("Netinkamas pasirinkimas!")
                return None
            
            pasirinkta_priemone = transporto_priemones[pasirinkimas]
            
            print("\n=== Pasirinkite nuomos laikotarpį ===")
            for key, value in self.LAIKOTARPIAI.items():
                print(f"{key}. {value}")
            
            laiko_pasirinkimas = input("Pasirinkite laikotarpį (1-5): ")
            if laiko_pasirinkimas not in self.LAIKOTARPIAI:
                print("Netinkamas pasirinkimas!")
                return None
            
            laikotarpis = self.LAIKOTARPIAI[laiko_pasirinkimas]
            
            print(f"\nJūs pasirinkote: {pasirinkta_priemone.gauti_info()}")
            print(f"Nuomos laikotarpis: {laikotarpis}")
            
            patvirtinimas = input("Patvirtinti pasirinkimą? (t/n): ").lower()
            if patvirtinimas == 't':
                return pasirinkta_priemone, laikotarpis
            else:
                print("Nuoma atšaukta.")
                return None
            
        except ValueError:
            print("Įveskite skaičių!")
            return None