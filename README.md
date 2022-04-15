# ITSol
V rámci projektu je vyvíjen systém pro podporu řízení rizik v projektech. Projekt vznikl v rámci předmětu Management projektů na FIT VUT. Bližší implementační detaily jsou popsány v souborech v adresáři `doc (TODO vytáhnout implementační detaily z těch dokumentů)`. Pro implementaci byl zvolen jazyk Python a framework Django. 

## popis použitých práv uživatelů
- `admin`: administrátor systému
- `project-manager`: projektový manažer
- `risk-manager`: manažer rizik
- `user`: standardní uživatel

## Administrátorský účet
Před vlastním používáním systému musí být v systému uložen  uživatel - administrátor. Administrátora je nutné vložit přes django shell (NOTE: oddělal jsem z gitignore sqlite, v kterém už je vložen, login a heslo je `admin`). 

## Členové týmu
TODO

## HOTOVO
- přihlašování, ověření práv, odhlašování
- zobrazení, vkládání, editace, mazání uživatelů
- zobrazení, vkládání, mazání projektů
- zobrazení detailů o projektu
- zobrazení bližších podrobností o projektu: seznam členů, seznam fází
- přiřazení zaměstnanců k projektům (během tvorby projektu i po vytvoření)
- přiřazení zaměstnanců do fází
- přidávání, editace, odstranění fází
- zobrazování podrobností o fází: seznam rizik

## TODO
- přidávání rizik
- editace, schvalování, odebírání rízik
- Kontrola nevalidních vstupů!!!
- vložit logo ITSol do složky `ITSol/RiskManagement/static`
- generování a zobrazování statistik
