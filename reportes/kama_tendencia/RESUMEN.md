# kama_tendencia — RESUMEN de validación

**Veredicto: DESCARTADA**  ·  params: `{'n': 10, 'er_min': 0.3}`

| métrica | IS | OOS |
|---|---|---|
| n_trades | 365 | 153 |
| profit_factor | 1.377 | 1.148 |
| pf_sin_mejor | 1.333 | 1.053 |
| cagr | 0.024 | 0.011 |
| max_dd | -0.054 | -0.070 |
| sharpe | 0.663 | 0.304 |
| expectancia_R | 0.076 | 0.035 |
| win_rate | 0.411 | 0.425 |
| t_stat | 2.084 | 0.584 |

| fase | check | valor | umbral | ok |
|---|---|---|---|---|
| 1_is_oos | pf_oos | 1.148 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos | 153 | >= 30 | OK |
| 1_is_oos | maxdd_oos | 0.070 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos | 1.053 | > 1.000 | OK |
| 2_walk_forward | wf_eficiencia | 0.712 | >= 0.500 | OK |
| 2_walk_forward | wf_ventanas_pos | 1.000 | >= 0.600 | OK |
| 3_meseta | meseta_es_3x3 | 9 | >= 9 | OK |
| 3_meseta | meseta_min_vecino | 1.138 | >= 1.200 | FALLA |
| 3_meseta | meseta_caida | 0.174 | <= 0.300 | OK |
| 4_monte_carlo | mc_p5_retorno | 0.052 | > 0.000 | OK |
| 4_monte_carlo | mc_p95_dd | 0.095 | < 0.250 | OK |
| 4_monte_carlo | mc_ruina | 0.000 | < 0.050 | OK |
| 5_stress | stress_costes_x2_pf_oos | 1.029 | >= 1.100 | FALLA |
| 5_stress | stress_sin_2_mejores_anios_pf | 1.150 | >= 1.100 | OK |
| 5_stress | stress_peor_tercio_pf | 1.067 | >= 1.100 | FALLA |

Walk-forward por ventana (cagr OOS): 0.037, 0.007, 0.059, 0.036, 0.007

Stress — PF por tercios: [1.31, 1.57, 1.07]
