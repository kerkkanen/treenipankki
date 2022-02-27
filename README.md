# Treenipankki

Sovellus on pankki lihaskuntoliikkeille ja treeniseteille. Sovelluksessa voi hakea eri lihasryhmiä harjoittavia kuntoiluliikkeitä ja koostaa haluamanlaisensa harjoituksen. Kaikki käyttäjät voivat selata harjoitusliikkeitä ja treenisettejä sekä arpoa itselleen satunnaisen treenin. Kirjautunut käyttäjä voi lisätä harjoitusliikkeitä ja settejä sekä koota suosikkiharjoituksiaan omalle sivulle.

Sovellus toimii [Herokussa](https://treenipankki.herokuapp.com/).

## Sovelluksen toiminnallisuudet

* Ilman kirjautumista on mahdollista
   * selata kirjautuneiden käyttäjien lisäämiä yksittäisiä treeniliikkeitä ja niistä koostettuja settejä.
   * hakea treenisettejä treenattavan alueen mukaan.
   * arpoa satunnaisen harjoitussetin.
* Sovellukseen voi luoda tunnuksen ja kirjautua sisään ja ulos. Kirjautuminen tuo mukanaan lisää toiminnallisuutta.
* Kirjautunut käyttäjä voi
      * lisätä pankkiin yksittäisiä treeniliikkeitä
      * lisätä pankkiin yksittäisistä liikkeistä koostuvia treenisettejä
      * tallettaa omalle sivulleen suosikkisettinsä.
      * poistaa suosikeiksi asettamiaan settejä suosikkilistalta.
      * arvioida minkä tahansa treenisetin.
* Sovellukseen on olemassa myös admin-oikeudet. Admin pystyy poistamaan pankista yksittäisiä harjoituksia, settejä, käyttäjiä ja arvosteluja.

## Jatkokehitysideoita

* Käyttäjä voi muokata luomansa liikkeen sisältöä, esimerkiksi päivittämällä kuvausta.
* Käyttä voi muokata luomansa setin sisältöä, esimerkiksi päivittämällä kuvausta tai vaihtamalla setin liikkeitä.
* Käyttä voi poistaa luomansa treeniliikkeen.
* Käyttäjä voi poistaa luomansa treenisestin.
* Käyttäjä voi poistaa kirjoittamansa arvostelun.
