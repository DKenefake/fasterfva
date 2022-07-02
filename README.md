# FasterFVA

A demonstration of a new Variable Flux Analysis (FVA) algorithm based on properties of LP solutions. This insight allows for subproblems found in FVA analysis to be entirely removed. The idea of this refinement is based on the number of active constraint that must be 'active' at any solution of a linear program (LP). This reduction in the number of LPs reduces the total amount of computational effort required for FVA.

## Benchmark against CobraPY software

Here is a broad summary of the benchmark results of this algorithm in 
Run serially on a 12700K CPU

| Model Name         | Proposed Algorithm Time(sec) | CobraPy Time(sec) | Ratio       |
|--------------------|------------------------------|-------------------|-------------|
| iAB_RBC_283        | 0.353                        | 0.46              | 1.303116147 |
| iAF1260b           | 8.618                        | 11.3319           | 1.314910652 |
| iAT_PLT_636        | 1.284                        | 3.17              | 2.468847352 |
| iEC1356_Bl21DE3    | 10.83                        | 12.655            | 1.168513389 |
| iEC1364_W          | 11.54                        | 13.59             | 1.177642981 |
| iECSP_1301         | 10.54                        | 12.55             | 1.190702087 |
| iIS312_Amastigote  | 0.422                        | 0.567             | 1.343601896 |
| iJN1463            | 12.275                       | 13.921            | 1.134093686 |
| iJO1366            | 10.14                        | 12.125            | 1.195759369 |
| iLB1027_lipid      | 27.642                       | 33.835            | 1.224043123 |
| iLJ478             | 0.846                        | 1.0339            | 1.222104019 |
| iMM904             | 4.108                        | 5.089             | 1.238802337 |
| iNJ661             | 1.849                        | 2.144             |   1.1595457 |
| Recon3D            | 80.66                        | 213.246           | 2.643763947 |


## Algorithm Details