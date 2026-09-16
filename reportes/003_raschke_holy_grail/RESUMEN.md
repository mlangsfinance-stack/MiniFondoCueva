# ndx_holy_grail — RESUMEN de validación

**Veredicto: DESCARTADA**  ·  params: `{'adx_min': 30, 'ema_n': 20, 'hold': 5}`

| métrica | IS | OOS | OOS darwinex |
|---|---|---|---|
| n_trades | 64 | 13 | 23 |
| profit_factor | 1.399 | 1.049 | 0.561 |
| pf_sin_mejor | 1.287 | 0.748 | 0.439 |
| cagr | 0.002 | 0.000 | -0.004 |
| max_dd | -0.042 | -0.045 | -0.078 |
| sharpe | 0.190 | 0.031 | -0.331 |
| expectancia_R | 0.103 | 0.023 | -0.191 |
| win_rate | 0.562 | 0.385 | 0.478 |
| t_stat | 1.086 | 0.074 | -1.212 |

| fase | check | valor | umbral | ok |
|---|---|---|---|---|
| 1_is_oos | pf_oos | 1.049 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos | 13 | >= 30 | FALLA |
| 1_is_oos | maxdd_oos | 0.045 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos | 0.748 | > 1.000 | FALLA |
| 1_is_oos | pf_oos_darwinex | 0.561 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos_darwinex | 23 | >= 30 | FALLA |
| 1_is_oos | maxdd_oos_darwinex | 0.078 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos_darwinex | 0.439 | > 1.000 | FALLA |
| 2_walk_forward | wf_eficiencia | 0.369 | >= 0.500 | FALLA |
| 2_walk_forward | wf_ventanas_pos | 0.600 | >= 0.600 | OK |
| 3_meseta | meseta_es_3x3 | 9 | >= 9 | OK |
| 3_meseta | meseta_min_vecino | 1.181 | >= 1.200 | FALLA |
| 3_meseta | meseta_caida | 0.156 | <= 0.300 | OK |
| 4_monte_carlo | mc_p5_retorno | -0.048 | > 0.000 | FALLA |
| 4_monte_carlo | mc_p95_dd | 0.056 | < 0.250 | OK |
| 4_monte_carlo | mc_ruina | 0.000 | < 0.050 | OK |
| 5_stress | stress_costes_x2_pf_oos | 1.004 | >= 1.100 | FALLA |
| 5_stress | stress_sin_2_mejores_anios_pf | 1.066 | >= 1.100 | FALLA |
| 5_stress | stress_peor_tercio_pf | 0.788 | >= 1.100 | FALLA |

Walk-forward por ventana (cagr OOS): 0.003, -0.009, 0.011, -0.002, 0.003

Stress — PF por tercios: [0.79, 2.53, 1.15]
