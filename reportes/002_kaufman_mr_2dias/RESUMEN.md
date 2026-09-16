# ndx_mr_2dias — RESUMEN de validación

**Veredicto: DESCARTADA**  ·  params: `{'sma_n': 200, 'hold': 2}`

| métrica | IS | OOS | OOS darwinex |
|---|---|---|---|
| n_trades | 948 | 282 | 286 |
| profit_factor | 1.055 | 1.354 | 1.233 |
| pf_sin_mejor | 1.043 | 1.311 | 1.210 |
| cagr | 0.004 | 0.020 | 0.011 |
| max_dd | -0.179 | -0.089 | -0.070 |
| sharpe | 0.130 | 0.591 | 0.386 |
| expectancia_R | 0.014 | 0.075 | 0.044 |
| win_rate | 0.546 | 0.589 | 0.608 |
| t_stat | 0.672 | 2.019 | 1.418 |

| fase | check | valor | umbral | ok |
|---|---|---|---|---|
| 1_is_oos | pf_oos | 1.354 | >= 1.300 | OK |
| 1_is_oos | trades_oos | 282 | >= 30 | OK |
| 1_is_oos | maxdd_oos | 0.089 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos | 1.311 | > 1.000 | OK |
| 1_is_oos | pf_oos_darwinex | 1.233 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos_darwinex | 286 | >= 30 | OK |
| 1_is_oos | maxdd_oos_darwinex | 0.070 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos_darwinex | 1.210 | > 1.000 | OK |
| 2_walk_forward | wf_eficiencia | 0.648 | >= 0.500 | OK |
| 2_walk_forward | wf_ventanas_pos | 0.600 | >= 0.600 | OK |
| 3_meseta | meseta_es_3x3 | 9 | >= 9 | OK |
| 3_meseta | meseta_min_vecino | 0.860 | >= 1.200 | FALLA |
| 3_meseta | meseta_caida | 0.184 | <= 0.300 | OK |
| 4_monte_carlo | mc_p5_retorno | 0.040 | > 0.000 | OK |
| 4_monte_carlo | mc_p95_dd | 0.114 | < 0.250 | OK |
| 4_monte_carlo | mc_ruina | 0.000 | < 0.050 | OK |
| 5_stress | stress_costes_x2_pf_oos | 1.279 | >= 1.100 | OK |
| 5_stress | stress_sin_2_mejores_anios_pf | 1.086 | >= 1.100 | FALLA |
| 5_stress | stress_peor_tercio_pf | 0.947 | >= 1.100 | FALLA |

Walk-forward por ventana (cagr OOS): 0.025, -0.007, 0.001, -0.007, 0.020

Stress — PF por tercios: [0.95, 1.16, 1.33]
