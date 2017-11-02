

"""Titel: Fotbollsserie
Författare: Patrik Bogren
Datum: 2017-09-27

Programmet hanterar serietabellen för Premier League. Programmet
läser först in filen 'table.csv' om den finns annars skapas den.
Filen skrivs på följande format:
Lagnamn,v,o,f,gm-im
där Lagnamn är lagets namn, v är vunna matcher, o är oavgjorda
matcher, f är förlorade matcher, gm är gjorde mål och im är
insläppta mål.
Filen är i .csv format varje och värde separeras med ett kommatecken
(notera dock att gm-im är ett och samma värde).

Data från en ny match läggs till från Game panelen.

Tabellen kan ändras via team panelen. Där användaren kan skapa ett
nytt lag eller ändra ett befintligt. Tabellvyn uppdateras när
användaren trycker på knappen 'submit'.

Autoifyllnad är aktiverat för fälten för att lägga till ny
matchdata samt för att ändra en rad i tabellen. Fältet för att
skapa en ny rad i tabellen har inte autoifyllnad.

"""
from fbseries.controller import Controller


def main():
    app = Controller()
    app.run()


if __name__ == '__main__':
    main()
