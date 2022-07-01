# FasterFVA

A demonstration of a new Variable Flux Analysis (FVA) algorithm based on utilizing active set information to remove the number of optimization calls that must be used.

The idea of this is that the active set of an LP of an FVA calculation will have the 'm' equalities from the S matrix and an additional 'n' active inequalities. These 'n' active inequalities are fluxes being set to bounds, thus up to 'n' problems can be removed from consideration for every FVA subproblem.

## Example Systems Applied

Here we apply it do different well known biological systems, with a mu factor of .9. This shows a reduction in the number of optimization calls by approximatly 25% to 75% depending on problem size.

|             | Nominal Algorithm | Improved Algorithm |
|:-----------:|:-----------------:|:------------------:|
| e_coli_core |        191        |         147        |
| iLJ478      |        1305       |         958        |
| iAF1260b    |        4777       |        3097        |
| Recon3D     |       21201       |        5100        |
