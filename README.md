# Dokumentace k programu Gomoku
**Jméno a příjmení:** Václav Janeček

Tento projekt vznikl jako zápočtový program k předmětu programování na MFF UK.

## Návod na použití programu
1. **Instalace:** Nejdříve si uživatel musí stáhnout nějaké uživatelské rozhraní, aby mohl daný program spustit. Pro spuštění programu bude stačit, když si stáhneme klasické IDLE pro spuštění programu: Stačí na stránce https://www.python.org/downloads/ stáhnout nejnovější verzi pro daný operační systém uživatele. Musíme si však stáhnout grafickou knihovnu PyGame, kterou si stáhneme pomocí konzolové aplikace - stačí, když do panelové lišty napíšeme **cmd**, čímž se nám zobrazí konzolová aplikace. Tu spustíme a na řádek napíšeme: **pip3 install pygame**. Tím se nám nainstaluje grafická knihovna PyGame do našeho IDLE a nyní už jsme schopni program spustit.
2. **Uživatelský návod:** Po otevření programu se nám zobrazí úvodní obrazovka. Na obrazovce máme na vstupu zadat, zda chceme hrát s kolečky (zadáme O na klávesnici), nebo s křížky (zadáme X na klávesnici) a po zmáčknutí klávesy Enter začíná hra. Hra probíhá jako klasické piškvorky - tedy se postupně hráči střídají v tazích a vyhrává ten, kdo jako první vytvoří posloupnost čtyř po sobě jdoucích znaků ve vertikálním směru, horizontálním svěru či v diagonále.
## Popis algoritmu, který řídí automatického protihráče: ##
Na vytvoření automatického protihráče jsem použil algoritmus Minimax. To je algoritmus z oblasti teorie her, což je matematická disciplína zkoumající různé rozhodovací procesy v mnoha oblastech lidského jednání. Základní princip tohoto algoritmu je, že postupně prochází strom hry (situace, které mohou na hrací desce nastat) do té doby, dokud nenarazí na listy v příslušném stromu hry. Pokud narazí na listy v příslušném stromu, tak pozici ohodnotí pomocí statické ohodnocovací funkce. Většinou ale není možné vygenerovat celý strom hry (to je i náš případ), neboť strom hry je příliš velký. Tedy místo vygenerování celého stromu hry (trvalo by příliš dlouho) algoritmus projde jen několik málo vrstev stromu (v našem případě 3-5) a pak danou pozici ohodnotí pomocí statické ohodnocovací funkce. Dále v algoritmu použím tzv. alfa-beta ořezávání, což je heuristika, která během výpočtu zahodí určité větve stromu hry, neboť nemají přímý vliv na výsledek hry. 

## Volba obtížnosti během hraní ##
Uživatel si může změnit obtížnost hry tím, že v přiloženém souboru final_version_gomoku bude postupně měnit parametr 
