# DFC — Schémas de handoff entre rôles

Contrat de données entre les skills `dfc-regime-analyst`,
`dfc-execution-trader` et `dfc-portfolio-manager`. Chaque passage de
rôle produit un artefact JSON conforme à l'un de ces schémas.

**Règle absolue** : un rôle ne consomme que des artefacts dont
`gate_status = "PASSED"`. Un artefact `PENDING` ou `REJECTED` ne
déclenche aucune action en aval.

---

## Enveloppe commune

Tout artefact porte cette enveloppe.

```json
{
  "artifact_type": "REGIME_READ | THESIS | SETUP | MANDATE | EXECUTION_REPORT | ALERT | DECISION",
  "artifact_id": "DFC-<TYPE>-<YYYYMMDD>-<seq>",
  "produced_by": "ANALYST | TRADER | PM",
  "produced_at": "ISO-8601",
  "session_id": "DFC-SESSION-<YYYYMMDD>",
  "gate": "G0 | G1 | G2 | G3 | G4 | G5 | G6 | G7",
  "gate_status": "PENDING | PASSED | AMENDED | REJECTED",
  "gate_signed_by": "PM ou null",
  "gate_signed_at": "ISO-8601 ou null",
  "payload": { }
}
```

---

## 1. `SESSION_OPEN` — Gate G0 (PM → tous)

```json
{
  "risk_budget_total": "montant ou % NAV",
  "risk_budget_by_strategy": {"<stratégie>": "montant"},
  "max_risk_per_position": "montant ou % NAV",
  "open_positions": [
    {"ticker": "", "side": "LONG|SHORT", "size": 0, "pnl": 0,
     "stop": 0, "distance_to_stop_pct": 0}
  ],
  "hard_limits": {"gross": 0, "net": 0, "leverage": 0,
                  "max_concentration_pct": 0, "drawdown_stop_pct": 0},
  "cash_available": 0,
  "margin_available": 0,
  "restrictions": ["tickers ou secteurs bloqués"],
  "regime_change_review_threshold_pp": 0,
  "session_open": true
}
```

`session_open: false` ⇒ aucune exécution autorisée, quel que soit le
reste du contexte.

---

## 2. `REGIME_READ` — Gate G1 (Analyste → PM)

```json
{
  "zones": {
    "<GLOBAL|US|EU|CN|EM|JP>": {
      "G": {"score": 0, "drivers": [{"indicator": "", "value": "",
             "weight": 0, "source": "", "as_of": ""}]},
      "I": {"score": 0, "drivers": []},
      "L": {"score": 0, "drivers": []}
    }
  },
  "model_output": {"R1": 0.0, "R2": 0.0, "R3": 0.0, "R4": 0.0},
  "overlays_proposed": [
    {"reason": "", "channel": "G|I|L", "magnitude": 0,
     "horizon": "", "confidence": "LOW|MED|HIGH",
     "requested_by": "ANALYST", "authorised_by": null}
  ],
  "final_probabilities": {"R1": 0.0, "R2": 0.0, "R3": 0.0, "R4": 0.0},
  "delta_vs_previous": {"R1": 0.0, "R2": 0.0, "R3": 0.0, "R4": 0.0},
  "policy_matrix": [
    {"event": "", "certainty": 0, "amplitude": 0, "horizon": 0,
     "channel": "G|I|L", "direction": 1, "delta_applied": 0,
     "already_priced": "NONE|PARTIAL|FULL", "evidence": ""}
  ],
  "cross_check": {
    "consistent": true,
    "divergences": [{"macro_says": "", "price_says": "",
                     "resolution": "", "resolved_by": ""}]
  },
  "scenarios": [
    {"label": "CENTRAL|UPSIDE|DOWNSIDE|TAIL", "probability": 0.0,
     "triggers": [], "cross_asset_impact": "", "early_signals": []}
  ]
}
```

**Validations bloquantes** : `sum(final_probabilities) == 1.0 ±0.01` ·
un scénario `TAIL` présent · `model_output` et `final_probabilities`
tous deux présents et distincts si overlay · chaque driver a `source`
et `as_of`.

---

## 3. `THESIS` — Gate G2 (Analyste (+ Trader) → PM)

Les douze blocs de la section 10 du playbook.

```json
{
  "ticker": "", "name": "", "side": "LONG|SHORT",
  "thesis": "", "regime_link": {"regime": "R1", "probability": 0.0},
  "catalyst": {"event": "", "expected_date": "", "observable": ""},
  "fundamentals": {"growth": "", "margins": "", "fcf": "",
                   "balance_sheet": "", "revisions": ""},
  "valuation": {"metric": "", "vs_history": "", "what_is_priced": ""},
  "positioning": {"consensus": "", "short_interest": "",
                  "options_skew": "", "flows": ""},
  "technical": null,
  "entry": null,
  "invalidation": null,
  "targets": null,
  "sizing_proposed": null,
  "hedge": {"instrument": "", "rationale": ""},
  "counter_argument": "",
  "score": {"expected_return": 0.0, "risk": 0.0, "ratio": 0.0}
}
```

Les champs `technical`, `entry`, `invalidation`, `targets`,
`sizing_proposed` sont `null` à la sortie de l'analyste. Le trader les
renseigne en phase 9.

**Validation bloquante** : `invalidation` non nul et
`counter_argument` non vide avant présentation en G2.

---

## 4. `SETUP` — Phase 9 (Trader → PM)

```json
{
  "thesis_id": "",
  "structure": {"monthly": "", "weekly": "", "daily": "", "h4": ""},
  "entry": {"zone_low": 0, "zone_high": 0, "condition": "",
            "quality": "PRIME|ACCEPTABLE|STRETCHED"},
  "invalidation": {"level": 0, "rationale": "",
                   "type": "STRUCTURAL|VOLATILITY"},
  "targets": [{"label": "T1", "level": 0, "rationale": ""},
              {"label": "T2", "level": 0, "rationale": ""}],
  "risk_per_unit": 0,
  "implied_size": 0,
  "size_basis": "risk_budget_allocated / distance_to_stop",
  "liquidity": {"adv": 0, "pct_of_adv": 0,
                "exit_days_stressed": 0},
  "execution_cost_bps": 0,
  "cancel_conditions": [],
  "asymmetry": {"reward_risk": 0.0, "verdict": "GO|NO-GO"}
}
```

**Validation bloquante** : `implied_size` calculé, jamais choisi ·
si `reward_risk < seuil DFC` ⇒ `verdict: NO-GO`, le setup n'est pas
présenté.

---

## 5. `MANDATE` — Gate G4 (PM → Trader)

```json
{
  "thesis_id": "", "decision_id": "",
  "instrument": "", "side": "BUY|SELL|SHORT|COVER",
  "target_size": 0,
  "price_bounds": {"limit": 0, "type": "LIMIT|RANGE|VWAP|TWAP"},
  "time_window": {"start": "", "end": ""},
  "slicing_allowed": true,
  "max_pct_adv": 0,
  "initial_stop": 0,
  "cancel_conditions": [],
  "venue_constraints": [],
  "signed_by": "PM", "signed_at": ""
}
```

Sans `MANDATE` signé, aucun ordre. Un mandat expiré n'est pas prolongé
tacitement : il faut un nouveau mandat.

---

## 6. `EXECUTION_REPORT` — Gate G5 (Trader → PM)

```json
{
  "mandate_id": "",
  "filled_size": 0, "fill_rate_pct": 0,
  "avg_price": 0,
  "benchmark": {"type": "ARRIVAL|VWAP|CLOSE", "price": 0},
  "slippage_bps": 0, "cost_bps": 0,
  "deviations": [{"type": "", "description": "",
                  "authorised_in_advance": false, "authorised_by": ""}],
  "unfilled_action": "EXPIRED|REQUESTED_NEW_MANDATE|NA",
  "position_after": {"size": 0, "avg_cost": 0, "stop": 0}
}
```

Toute `deviation` avec `authorised_in_advance: false` est un incident :
signalement immédiat au PM, avant fin de séance.

---

## 7. `ALERT` — Phase 11 (Analyste ou Trader → PM)

```json
{
  "position_id": "",
  "trigger": "INVALIDATION_HIT | CATALYST_CHANGED | REGIME_SHIFT |
              CORRELATION_DRIFT | LIQUIDITY_DEGRADATION |
              LIMIT_APPROACH | THESIS_BROKEN",
  "severity": "INFO | WARNING | CRITICAL",
  "evidence": "",
  "recommendation": "HOLD|REDUCE|EXIT|ADD|ADJUST_STOP|HEDGE",
  "requires_pm_decision": true
}
```

`CRITICAL` ⇒ escalade immédiate, pas d'attente de la revue programmée.

---

## 8. `DECISION` — Gates G3, G6, G7 (PM)

```json
{
  "scope": "POSITION | PORTFOLIO | METHOD",
  "reference_id": "",
  "decision": "INITIATE|ADD|HOLD|REDUCE|EXIT|WAIT|DEROGATE|DE-RISK",
  "rationale": "",
  "regime_context": {"dominant": "R1", "probability": 0.0},
  "risk_impact": {"gross_after": 0, "net_after": 0,
                  "concentration_after": 0, "worst_case_loss": 0},
  "review_conditions": [],
  "human_signature_required": true,
  "signed_by": "", "signed_at": ""
}
```

Une décision `WAIT` est consignée au même titre qu'une décision
d'agir. L'absence de décision n'est pas une décision.

---

## Machine d'état du workflow

```
G0 ──► [Analyste: ph.1-5] ──► G1 ──► [ph.6-7 allocation PM]
                                        │
                              [Analyste: ph.8 fiches]
                                        │
                                       G2 ──► [Trader: ph.9 setups]
                                        │
                                       G3 (décision PM)
                                        │
                                       G4 (mandat) ──► [Trader: ph.10]
                                        │
                                       G5 (contrôle exécution)
                                        │
                              [ph.11 monitoring A+T] ──► ALERT
                                        │
                                       G6 (revue) ──► G7 (clôture)
```

Aucun saut de gate. Un `REJECTED` renvoie à la phase amont, jamais
en aval.
