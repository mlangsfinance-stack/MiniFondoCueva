# ndx_ochenta_veinte — RESUMEN de validación

**Veredicto: DESCARTADA**  ·  params: `{'pct': 0.2, 'hold': 1, 'atr_mult_rango': 1.0}`

| métrica | IS | OOS | OOS darwinex |
|---|---|---|---|
| n_trades | 1153 | 276 | 361 |
| profit_factor | 0.743 | 1.153 | 1.161 |
| pf_sin_mejor | 0.735 | 1.120 | 1.118 |
| cagr | -0.017 | 0.007 | 0.009 |
| max_dd | -0.467 | -0.052 | -0.086 |
| sharpe | -0.546 | 0.274 | 0.331 |
| expectancia_R | -0.044 | 0.029 | 0.029 |
| win_rate | 0.453 | 0.522 | 0.512 |
| t_stat | -3.773 | 0.899 | 1.043 |

| fase | check | valor | umbral | ok |
|---|---|---|---|---|
| 1_is_oos | pf_oos | 1.153 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos | 276 | >= 30 | OK |
| 1_is_oos | maxdd_oos | 0.052 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos | 1.120 | > 1.000 | OK |
| 1_is_oos | pf_oos_darwinex | 1.161 | >= 1.300 | FALLA |
| 1_is_oos | trades_oos_darwinex | 361 | >= 30 | OK |
| 1_is_oos | maxdd_oos_darwinex | 0.086 | < 0.200 | OK |
| 1_is_oos | pf_sin_mejor_oos_darwinex | 1.118 | > 1.000 | OK |
| 2_walk_forward | wf_eficiencia | 0.000 | >= 0.500 | FALLA |
| 2_walk_forward | wf_ventanas_pos | 0.600 | >= 0.600 | OK |
| 3_meseta | meseta_es_3x3 | 9 | >= 9 | OK |
| 3_meseta | meseta_min_vecino | 0.651 | >= 1.200 | FALLA |
| 3_meseta | meseta_caida | 0.124 | <= 0.300 | OK |
| 4_monte_carlo | mc_p5_retorno | -0.064 | > 0.000 | FALLA |
| 4_monte_carlo | mc_p95_dd | 0.129 | < 0.250 | OK |
| 4_monte_carlo | mc_ruina | 0.000 | < 0.050 | OK |
| 5_stress | stress_costes_x2_pf_oos | 1.049 | >= 1.100 | FALLA |
| 5_stress | stress_sin_2_mejores_anios_pf | 0.769 | >= 1.100 | FALLA |
| 5_stress | stress_peor_tercio_pf | 0.548 | >= 1.100 | FALLA |

Walk-forward por ventana (cagr OOS): 0.016, -0.007, -0.013, 0.002, 0.009

Stress — PF por tercios: [0.55, 1.13, 1.07]
