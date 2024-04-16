# Magic: The Gathering -korttitietokanta

Sovelluksessa näkyy kaikki käyttäjän kansiot (korttien säilytyspaikat),
joissa on lista niiden sisältämistä korteista. Käyttäjä voi myös lisätä ja 
hakea kortteja ja lisätä niitä omaan kirjastoonsa.

**Ominaisuuksia:**

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. (toimii)
- Käyttäjä näkee listan kansioistaan ja niiden sisällä listan kansion pelikorteista (osittain toimii, kansioiden sisäiset vielä tekemättä)
- Käyttäjä voi lisätä pelikortteja tietokantaan ja muokata niiden ominaisuuksia (lisääminen ja muokkaaminen toimii)
- Pelikorteilla on useita ominaisuuksia, kuten kuva, korttityyppi, sen "hinta" ja voimia (lisätty tietokantaan tarvittavat)
- Käyttäjän lisätessä kortin tietokantaan sovellus hakee kortin kuvan netistä (scryfall.com) (ehkä)
- Käyttäjä voi hakea korttia nimellä tai rajatusta valikoimasta ominaisuuksia
- Käyttäjä voi poistaa kortin tietokannastaan, jos se on siellä
- Jokaisen listan kohdalla on valikoidut tiedot listan korttien ominaisuuksista


# Paikallinen käyttö

Kloonaa repositorio omalle koneellesi:
`git@github.com:kaltionkasvatti/magic-library.git`

Siirry komentorivillä kyseiseen kirjastoon.

Luo `.env` -tiedosto seuraavilla muuttujilla:
`DATABASE_URL=<local-postgres-address>`
`SECRET_KEY=<your-secret-key>`

Käynnistä virtuaaliympäristö:
`python3 -m venv venv`
`source venv/bin/activate`

Asenna riippuvuudet:
`pip install -r requirements.txt`

Määritä tietokanta:
`psql < schema.sql`

Käynnistä sovellus:
`flask run`