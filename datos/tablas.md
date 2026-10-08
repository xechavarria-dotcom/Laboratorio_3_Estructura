# Tablas de resultados

## Tiempo de una búsqueda con ids ALEATORIOS (en µs — menos es más rápido)

Promedio ± desviación estándar de 10 repeticiones. Lista es O(N); el ABB y el B+ son O(log N). La última columna: cuántas veces más lenta es la Lista que el B+.

|       N |       Lista |         ABB |          B+ | Lista/B+ |
|--------:|------------:|------------:|------------:|---------:|
|   1.000 | 22,2 ± 1,63 | 1,31 ± 0,08 | 1,25 ± 0,10 |      18× |
|   5.000 |  116 ± 11,0 | 1,98 ± 0,17 | 1,69 ± 0,06 |      69× |
|  10.000 |  231 ± 6,39 | 2,41 ± 0,16 | 2,01 ± 0,07 |     115× |
|  20.000 |  566 ± 38,9 | 3,13 ± 0,25 | 2,55 ± 0,20 |     222× |
|  35.000 | 1.353 ± 108 | 3,80 ± 0,17 | 3,15 ± 0,18 |     430× |
|  50.000 | 2.615 ± 279 | 4,36 ± 0,31 | 3,57 ± 0,19 |     732× |
|  75.000 | 4.762 ± 172 | 5,00 ± 0,10 | 4,09 ± 0,14 |   1.164× |
| 100.000 | 7.042 ± 397 | 5,50 ± 0,43 | 4,53 ± 0,28 |   1.555× |

*La Lista se vuelve miles de veces más lenta cuando N crece; los árboles casi no cambian.*

## Tiempo de una búsqueda con ids ORDENADOS (en µs — menos es más rápido)

Promedio ± desviación estándar de 10 repeticiones. Aquí el ABB se degrada a O(N). La última columna: cuántas veces más lento es el ABB que el B+.

|      N |       Lista |          ABB |          B+ | ABB/B+ |
|-------:|------------:|-------------:|------------:|-------:|
|  1.000 | 19,0 ± 0,70 |  50,0 ± 1,49 | 1,26 ± 0,04 |    40× |
|  5.000 | 99,3 ± 3,87 |   275 ± 13,6 | 1,76 ± 0,17 |   156× |
| 10.000 |  203 ± 7,33 |   527 ± 9,36 | 2,13 ± 0,04 |   248× |
| 20.000 |  432 ± 37,7 | 1.102 ± 23,7 | 2,79 ± 0,13 |   395× |

*Con ids ordenados el ABB se vuelve tan lento como la Lista (o más); solo el B+ se mantiene rápido.*

