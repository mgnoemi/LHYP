1.	Systole és diastole elkülönítése
A patient dictionary-hez csak akkor rendel slice-ot, ha a slice-ban van olyan frame, amely frame  számának abszolút értékben vett különbsége közelebb van a 24-hez, mint 9-hez, vagy a frame 0. Ezt egy if-es szerkezettel oldottam meg.

2.	Egyik slice-nak nem volt diastole-ja
Egy adott páciensél amikor a slice-okat és frame-eket vizsgáltam, merült fel a probléma, hogy a kiértékelésnél volt olyan slice amihez nem talált diastole-t. Ennek oka az volt, hogy az adott slice-on a jobbkamrára jellemző kontúr volt berajzolva.  Ezt úgy oldottam meg, hogy az adatk kiíráse alőtt ellenőriztem, hogy minden szükséges adat rendelkezére áll-e azaz ha  cnts mode lp vagy ln.
Ekkor tölti csak fel a cntrs-t slice-al, frame-el és mode-al.
(Ez a probléma a páciens utolsó slice-án merült fel)


3.	Nincs minden páciensnek meta adata, vagy kontúrja, esetleg egyik sem
A páciensek pickle fájlainak létrehozásakor merült fel a probléma, hogy bizonyos pácienseknek nem lehetett olyan pickle fájl-t létrehozni, ami tartalmazza a meta adatait, valamint a szív kontúrjait, ugyanis a kettő közül valamelyik, vagy egyik sem létezett. 
Ennek következtében mikor olyan pácienshez ért, akinek nem voltak ilyen jellegű adatai megakadt a program. Ezt a problémát egy try-except kóddal sikerült kiküszöbölnöm. A try alatt megnézi, hogy a vizsgált páciensnek léteznek-e a kiértékeléshez szükséges adatai. Amennyiben létezik,létrehozza a pickle fájlt.
