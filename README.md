# CSVPlotter
Python script pro plotování CSV výsledků Testbedu



### Požadavky:
Python (například z https://www.microsoft.com/en-us/search?q=python)

### Požadovaný vstup pro jednotlivé grafy:
CSV výstupy z testbedu pro zvolený počet dimenzí (například 10D)
- první sloupec jsou čísla iterací

### Požadovaný vstup pro dvojgrafy:
cesta ke složce která obsahuje:
1. složku CSV výstupy z testbedu pro zvolený počet dimenzí (například 10D) jednoho algoritmu
2. složku CSV výstupy z testbedu pro zvolený počet dimenzí (například 10D) druhého algoritmu
3. ...

```
10D
└── SOMA10D
    └── csvčka
└── JDE10D
    └── csvčka  
```

```
20D
└── SOMA20D
    └── csvčka
└── JDE20D
    └── csvčka            
```
pro vstup vyber jednu ze složek! (10D nebo 20D)

### Spuštění:
python CSVPlotter.py

Patrik:
```
  ▲__
 [ ]
 -|-
 | |
 ```
