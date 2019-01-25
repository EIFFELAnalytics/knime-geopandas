# Documentatie geopandas in KNIME
> HOWTO Gebruik van de in-house ontwikkelde [geopandas](http://geopandas.org/) blokjes in [KNIME](https://www.knime.com/).

## Welke Python-blokjes (*nodes*) zijn beschikbaar?

* *Source node:* Inladen van [shapefiles](https://nl.wikipedia.org/wiki/Shapefile).
* *View node*: Bekijk de shape(s).
* *WKT to AC node*: Converteert WKT ([well-known text](https://en.wikipedia.org/wiki/Well-known_text)) naar AC format.
* *Simplify node*: [Simplificeren](http://toblerity.org/shapely/manual.html#object.simplify) van polygonen.
* <span style="color:red">TODO: Toevoegen de rest van de nodes<span>

<span style="color:red">TODO: Toevoegen welke KNIME python node (source, script 1>1, etc) hoort bij welke node hierboven<span>

## Hoe wordt de data tussen de nodes doorgegeven?
De standaard "Python Script (1$\Rightarrow$1)" node neemt `input_table` in en geeft `output_table` uit. Beide zijn pandas [DataFrames](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

De geografische informatie in elke node wordt niet verwerkt met *pandas*, maar met *geopandas*. Een GeoDataFrame heeft naast normale kolommen, standaard een `geometry`-kolom voor de geometrie (polygon, multipolygon, point, etc). Om een GeoDataFrame om te zetten in een DataFrame, zodat deze doorgegeven kan worden tussen nodes, wordt de `geometry`-kolom telkens vervangen door een `wkt`-kolom. WKT (well-known text) is een tekstuele representatie van geometrische objecten.

## Hoe werkt zo'n node?
Elke node is geschreven in Python en bestaat uit de volgende secties:

* *User defined*: Hier dient de gebruiker bepaalde variabelen te specificeren.
* *Header*: Standaard preparatie-code, zoals `import`s en functiedefinities.
* *Node*: De functionaliteit van de specifieke node van input t/m output.
* *Footer*: Standaard afsluiting met gedetaileerde informatie over het proces en de `output_table`.

Door de code heen wordt informatie ge`print`. Dit is na te lezen in KNIME met *View: Standard Output*.

## Python setup in KNIME
1. Download en installeer [Anaconda](https://www.anaconda.com/download/).
2. Open een Anaconda Prompt.
3. Maak een nieuwe virtual environment voor Python en de packages `pandas` en `jedi`, zoals [beschreven in een blog van KNIME](https://www.knime.com/blog/setting-up-the-knime-python-extension-revisited-for-python-30-and-20). Voeg hier ook `geopandas` aan toe.
```
(base) I:\>conda create -y -n py36_knime python=3.6 pandas geopandas jedi
```
Dit zal ook een aantal extra packages (dependencies) installeren en kan redelijk lang duren.
4. Check of dit gelukt is.
```
(base) I:\>conda info --envs
# conda environments:
#
base                  *  C:\ProgramData\Anaconda3
py36_knime               C:\ProgramData\Anaconda3\envs\py36_knime
```
5. In de environment moeten nog extra packages handmatig geinstalleerd worden die niet op conda channels staan.
    * Activeer de environment.
    ```
    (base) I:\>activate py36_knime
    
    (py36_knime) I:\>
    ```
    * Installeer de Python package manager `pip`.
    ```
    (py36_knime) I:\>conda install pip
    ...
    Executing transaction: done
    ```
    * Installeer `openrouteservice` met `pip`.
    ```
    (py36_knime) I:\>pip install openrouteservice
    ```
    Hier kan een foutmelding tussendoor komen. Volgens mij is dat geen probleem zolang afgesloten wordt met een succesmelding.
6. Check met `conda list` of de packages (`pandas`, `geopandas` en `openrouteservice`) geinstalleerd zijn.
7. Deactiveer de virtual environment met het commanda `deactivate`. En sluit de prompt met `exit`.
8. Volg vanaf hier de procedure verder zoals [beschreven in de KNIME blog](https://www.knime.com/blog/setting-up-the-knime-python-extension-revisited-for-python-30-and-20) vanaf het aanmaken van de bat file ("If you are using Windows...").

## Inladen templates in KNIME
Op Teams/SharePoint staat een [folder met de templates](https://eiffelnl.sharepoint.com/sites/afd-analysecentrum/Shared Documents/General/Tooling/KNIME). Hierin zijn alle beschikbare geopandas nodes opgeslagen.

Om ze in KNIME te gebruiken, kopieër je de map "sourcecode-templates" naar je workspace folder (voorbeeld "C:\Users\abos\knime-workspace\.metadata\knime\sourcecode-templates"). In die workspace kun je de templates gebruiken door:

* een Python node in een workflow te slepen
* dubbelklik om te bewerken
* in de tab Templates de gewenste node te selecteren
* en op Apply selected te klikken.

## Extra technische info
### Over projecties
Introductie over projecties: http://geopandas.org/projections.html

Beschrijvende eigenschappen van twee vaak voorkomende projecties:
* *WGS84*
    * https://epsg.io/4326
    * Amersfoort = `(52.1561110, 5.3878270)`
    * In graden
    * ~ 110km/degree longitude (horizontaal)
    * ~ 70km/degree latitude (verticaal)
* *RD New Amersfoort*
    * https://epsg.io/28992
    * Amersfoort = `(142892.19, 470783.87)`
    * In meters