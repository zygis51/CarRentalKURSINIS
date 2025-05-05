class Klientas:
    def __init__(self, vardas):
        self.vardas = vardas
        self.nuomos = []
        self.nuomos_laikai = {}

    def prideti_nuoma(self, transporto_priemone, laikotarpis=None):
        self.nuomos.append(transporto_priemone)
        if laikotarpis:
            self.nuomos_laikai[transporto_priemone._numeris] = laikotarpis
        transporto_priemone._is_nuomota = True

    def parodyti_nuomas(self):
        if not self.nuomos:
            print(f"Klientas {self.vardas} neturi nuomų.")
            return
        
        print(f"\nKliento {self.vardas} nuomos:")
        for i, nuoma in enumerate(self.nuomos, 1):
            laikas = self.nuomos_laikai.get(nuoma._numeris, "Nenurodyta")
            print(f"{i}. {nuoma.gauti_info()} | Būsena: {nuoma.ar_isnuomota()} | Nuomos laikas: {laikas}")