# graphs-1
Prost program za vizuelizaciju algoritama na kreiranim grafovima 

## Upotreba
Kreiranje grafova:
1. Levi klik
	* Postavlja novu tacku
	* Povezuje tacke
2. Desni klik
	* Sklanja tacke
	* Razvezuje tacke
3. Srednji klik
	* Pomera tacke

## Algoritmi
Trenutno je na mestu samo BFS pretraga. Radi u dva moda, u zavisnosti od toga da li cekirate "Search full graph" ili ne.
1. Search full graph **nije** cekiran:
	- Algoritam ce pronaci najkraci put od polazne tacke do cilja
2. Search full graph **jeste** cekiran:
	- Cilj se ne moze postaviti, samo polazna tacka. Algoritam ce pretraziti ceo graf, a zatim ce oznaciti pronadjene petlje. **NIJE STABILNO**

