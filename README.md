# FasterFVA

A demonstration of a new Variable Flux Analysis (FVA) algorithm based on properties of LP solutions. This simple insight allows for subproblems found in FVA analysis to be entirely removed. The idea of this refinement is based on the number of active constraint that must be 'active' at any solution of a linear program (LP). This reduction in the number of LPs reduces the total amount of computational effort required for FVA.

## Benchmark against CobraPY software

Here is a broad summary of the benchmark results of the proposed algorithm and CobraPY a leading sodtware in for this type of analysis. Run serially on a 12700K CPU

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

### The Intuition

It is a well known property of LPs that when solved with a vertex based algorithm (such as the simplex algorithm) that if there are $n$ variables then there must have at least $n$ active constraints, meaning that $n$ constraints are heald at equality. If there are $m$ equality constraints and $m < n$ that must mean that some of the inequality constraints are active and thus at equality. 

This means for FVA analasysis, many times when we are trying to determine the bounds of a certain flux $v_i$; we also have insight on the max (or min) range of other flux veriables ($v_k$)! Instead of simply solving $2n$ LPs to determine the max( and min) of each flux; we can inspect the solution of the intermediate problems to see if any other flux has attained a maximum (or minimum). This is exactly the same as the flux bounds becoming active in the sense of the previous paragraph. In simple terms, when solving for the bounds of a flux variable $v_i$ we also get bounds information on other variables $v_k$ for free. This allows us to skip some flux bounds checks meaning we are solving less LPs.

### The Actual Algorithm

Firstly, the fluxes are solved to find the best maximuizer for the biological imerative $Z = c^Tv$. This is the best we can do, for this system. 

$$
\Huge
\begin{align}
        Z = \min_v \quad &c^Tv\\
        \text{s.t. } Sv & = 0\\
        v_l \leq v &\leq v_u\\
        v &\in R^n
\end{align}
$$

We then add the constraint $c^Tv\geq\mu Z$ as an additional constraint on the system. This is enforces that when finding the flux bounds we are within a certain factor of optimiality. As we solve the followin problem iterativley we find active constraints at the upper and lower bounds of the variable and skip those optimization problems.

$$
\Huge
\begin{align}
        \min_v \quad &\pm v_i\\
        \text{s.t. } Sv & = 0\\
        v_l \leq v &\leq v_u\\
        c^Tv &\geq \mu Z\\
        v &\in R^n
\end{align}
$$
