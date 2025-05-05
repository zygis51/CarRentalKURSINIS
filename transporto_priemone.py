from abc import ABC, abstractmethod

class TransportoPriemone(ABC):
    def __init__(self, numeris, marke, metai, is_nuomota=True):
        self._numeris = numeris
        self._marke = marke
        self._metai = metai
        self._is_nuomota = is_nuomota

    def ar_isnuomota(self):
        return "Taip" if self._is_nuomota else "Ne"

    @abstractmethod
    def gauti_info(self):
        pass

class Automobilis(TransportoPriemone):
    def __init__(self, numeris, marke, metai, durys, is_nuomota=True):
        super().__init__(numeris, marke, metai, is_nuomota)
        self._durys = durys

    def gauti_info(self):
        return f"Automobilis: {self._marke} ({self._metai}), numeris: {self._numeris}, durys: {self._durys}"

class Mikroautobusas(TransportoPriemone):
    def __init__(self, numeris, marke, metai, vietos, is_nuomota=True):
        super().__init__(numeris, marke, metai, is_nuomota)
        self._vietos = vietos

    def gauti_info(self):
        return f"Mikroautobusas: {self._marke} ({self._metai}), numeris: {self._numeris}, vietų skaičius: {self._vietos}"

class TransportoPriemoniuGamykla:
    @staticmethod
    def sukurti_transporto_priemone(tipas, **kwargs):
        if tipas == "automobilis":
            return Automobilis(**kwargs)
        elif tipas == "mikroautobusas":
            return Mikroautobusas(**kwargs)
        else:
            raise ValueError("Nežinomas transporto priemonės tipas.")