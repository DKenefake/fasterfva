# FasterFVA

This repository demonstrates a new Variable Flux Analysis (FVA) algorithm based on the properties of linear programming (LP) solutions. This simple insight allows for subproblems found in FVA analysis to be entirely removed. The idea of this refinement is based on the number of active constraints that must be 'active' at any solution of an LP. This reduction in the number of LPs reduces the total amount of computational effort required for FVA.

The results and case studies are summarized in the following preprint, [An Improved Algorithm for Flux Variability Analysis](https://www.researchsquare.com/article/rs-2109496/v1).

## Algorithm Details

### The Intuition

It is a well-known property of LPs that when solved with a vertex-based algorithm (such as the simplex algorithm), if there are $n$ variables, then there must be at least $n$ active constraints, meaning that $n$ constraints are heald at equality if there are $m$ equality constraints and $m < n$ that must mean that some of the inequality constraints are active and thus at equality. 

This means for FVA analysis, many times when we are trying to determine the bounds of a certain flux $v_i$; we also have insight into the max (or min) range of other flux variables ($v_k$)! Instead of simply solving $2n$ LPs to determine the max( and min) of each flux, we can inspect the solution of the intermediate problems to see if any other flux has attained a maximum (or minimum). This is the same as the flux bounds becoming active in the previous paragraph. In simple terms, when solving for the bounds of a flux variable $v_i$ we also get bounds information on other variables $v_k$ for free. This insight allows us to skip some flux bounds checks, meaning we are solving fewer LPs.

### The Actual Algorithm

Firstly, the optimal fluxes are solved to find the best maximizer for the biological imperative $Z = c^Tv$. This bound is the best that is achievable for this particular system.

$$
\Huge
\begin{align}
        Z = \min_v \quad &c^Tv\\
        \text{s.t. } Sv & = 0\\
        v_l \leq v &\leq v_u\\
        v &\in R^n
\end{align}
$$

We then add the constraint $c^Tv\geq\mu Z$ as an additional constraint on the system. This additional constraint enforces that when finding the flux bounds, we are within a certain factor of optimality. As we solve the following problem iteratively, we find active constraints at the upper and lower bounds of the variable and skip those optimization problems.

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


## Benchmark

![image](https://github.com/DKenefake/fasterfva/blob/main/benchmark/LPcompare.png)
![image](https://github.com/DKenefake/fasterfva/blob/main/benchmark/time_ratio.png)

## Citation

Since a lot of time and effort has gone into FasterFVA's development, it would be greatly appreciated if you cite the following publication if you use this in your work.

```
@article{kenefake2022improved,
  title={An Improved Algorithm for Flux Variability Analysis},
  author={Kenefake, Dustin and Armingol, Erick and Lewis, Nathan E and Pistikopoulos, Efstratios N},
  year={2022}
}
```
