# ndx_breakout_er — RESUMEN de validación

**Veredicto: DESCARTADA**  ·  params: `{'n_entrada': 40, 'n_salida': 20, 'er_n': 10, 'er_min': 0.3}`

| métrica | IS | OOS | OOS darwinex |
|---|---|---|---|
| n_trades | 93 | 24 | 23 |
| profit_factor | 2.218 | 5.701 | 4.864 |
| pf_sin_mejor | 1.995 | 4.889 | 4.175 |
| cagr | 0.016 | 0.024 | 0.017 |
| max_dd | -0.073 | -0.048 | -0.038 |
| sharpe | 0.531 | 0.856 | 0.693 |
| expectancia_R | 0.546 | 1.063 | 0.811 |
| win_rate | 0.430 | 0.708 | 0.609 |
| t_stat | 2.411 | 3.031 | 2.823 |

| fase | check | valor | umbral | ok |
|---|---|---|---|---|
| 1_is_oos | pf_oos | 5.701 | >= 1.300 | OK |
| 1_is_oos | trades_oos | 24 | >= 30 | FALLA |
| 1_is_oos | maxdd_oos | 0.048 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos | 4.889 | > 1.000 | OK |
| 1_is_oos | pf_oos_darwinex | 4.864 | >= 1.300 | OK |
| 1_is_oos | trades_oos_darwinex | 23 | >= 30 | FALLA |
| 1_is_oos | maxdd_oos_darwinex | 0.038 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos_darwinex | 4.175 | > 1.000 | OK |
| 2_walk_forward | wf_eficiencia | 0.767 | >= 0.500 | OK |
| 2_walk_forward | wf_ventanas_pos | 0.800 | >= 0.600 | OK |
| 3_meseta | meseta_es_3x3 | 9 | >= 9 | OK |
| 3_meseta | meseta_min_vecino | 1.913 | >= 1.200 | OK |
| 3_meseta | meseta_caida | 0.138 | <= 0.300 | OK |
| 4_monte_carlo | mc_p5_retorno | 0.133 | > 0.000 | OK |
| 4_monte_carlo | mc_p95_dd | 0.038 | < 0.250 | OK |
| 4_monte_carlo | mc_ruina | 0.000 | < 0.050 | OK |
| 5_stress | stress_costes_x2_pf_oos | 5.618 | >= 1.100 | OK |
| 5_stress | stress_sin_2_mejores_anios_pf | 2.415 | >= 1.100 | OK |
| 5_stress | stress_peor_tercio_pf | 1.900 | >= 1.100 | OK |

Walk-forward por ventana (cagr OOS): 0.024, -0.002, 0.027, 0.018, 0.020

Stress — PF por tercios: [2.52, 1.9, 3.81]
