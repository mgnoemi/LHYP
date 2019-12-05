#Hypertrófia

##Bevezetés
A mélytanulás az elmúlt időben nagy figyelemnek örvend, kimagasló eredményeket ér el az orvostudományban is. A mélytanulási algoritmusok nagyon jók a különféle képalkotó diagnosztikai berendezések (MRI, CT) által létrehozott, vizuális információt tartalmazó leletek kiértékelésében.
  
##Mi volt a projekt? 
A projekt a Városmajori Szív- és Érgyógyászati Klinika és a BME együtműködésében született meg, célja olyan mélytanuló algoritmuson alapuló szoftver megalkotása, ami a szívről készített MRI felvételek alapján segít felismerni a balkamrai hypertrófiát, azaz a balkamra falának kóros asszimetriáját, megvastagodását.  Jelenleg nincs ezt az elváltozást vizsgáló automatikus folyamat, szűrése minden esetben időigényes, és szakmai hozzáértő személyt igényel. A program szerepe a döntéstámogatás, így jelentősen felgyorsítja a kiértékelés folyamatát. A projekt számára a klinika 5400 páciens adatait bocsájtotta rendelkezésre, ami az ebben a témában korábban megvalósult kutatásokban alkalmazott adathalmaznál jóval nagyobb.

A projekt keretein belül két fő irányvonal szerint indult meg a kutatás:
    1.	sportos életmódot folytató egyének esetén a szívkamra fala megvastagodhat, ami nem feltétlen jelent kóros elváltozást, de nem is zárja ki azt.
    2.	a szív teljes ciklusát MR képekben rögzítve, a képeket kiértékelve megállapítani, hogy fennáll-e a kóros elváltozás, és ha igen, annak az ún. HCM-es változatába tartozik-e. 

Ezek közül az utóbbiban vettem részt.

Kiindulás
Az MR felvételek a szív több síkja mentén készültek, ezek a síkok egymástól 7 mm-re követték egymást, irányonként általában 12 metszősíkban. Minden síkban egy teljes szívcikluson keresztül készültek a képek, azaz szeletenként általában 25 db. Az MR felvételek mellett a páciensek egyéb adatai is rendelkezésre álltak. Ezeken az adatokon felül kaptam már a képek kiértékeléséből származó adatokat, amik a kamrák határát leíró ponthalmazok. 

Feladatom
A sok páciens sok adata miatt az első feladatom az adathalmaz csökkentése volt, amit a számomra szükséges adatok összegyűjtésével valósítottam meg. Ezek az adatok a szív rövid tenelyének (SA) síkjában, a bal kamra belső és külső kontúrját leíró ponthalmazok, amikor a szív ciklusa során a balkamra a legnagyobb (diastole), valamint a páciens meta adatai.
Az előzetes kiértékelés már megállapította a kamra méretének szélsőértékeit (sistole és diastole), ezekből a diastole megállapítása már az én feladatom volt.
Az így kigyűjtött adatokat úgynevezett pickle fájlban tároltam, páciensenként. A program ezeket a fájlokat hívja meg a kontúr kiértékelések elvégzéséhez. A kiértékelés 3 féle paraméter kiszámítását foglalta magában a balkamra falának külső és belső kontúrjainak segítségével. Vizsgáltam a kontúrok hosszának az arányát, a 2 kontúr által határolt területek arányát és a két kontúr Haussdorf távolságát.

A kontúrok hosszát úgy vizsgáltam, hogy a kontúr mentén összegeztem az egymás után jövő pontok közötti távolságot, amit Pitagorasz tétel segítségével határoztam meg.
A kontúrok területét a poligonok területeinek számítása alapján végeztem el.
