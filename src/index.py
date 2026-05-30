#!/usr/bin/env python3
"""
carbon-footprint-api — company activity data → CO2e footprint
Scope 1/2/3 breakdown, reduction suggestions, Science Based Targets alignment,
comparison to industry benchmarks, carbon budget tracking
"""
import anthropic, json, re, sys
from dataclasses import dataclass, field, asdict
from typing import Optional

SYSTEM = """You are a corporate sustainability specialist and carbon accounting expert
certified in GHG Protocol methodology.

Calculate the carbon footprint and provide actionable reduction guidance.

Return ONLY valid JSON — no markdown, no explanation.

{
  "company_name": "string or 'Company'",
  "reporting_year": "YYYY",
  "methodology": "GHG Protocol Corporate Standard",
  "summary": {
    "scope_1_tco2e": number,
    "scope_2_market_based_tco2e": number,
    "scope_2_location_based_tco2e": number,
    "scope_3_tco2e": number_or_null,
    "total_tco2e": number,
    "revenue_intensity": "tCO2e per $M revenue or null",
    "employee_intensity": "tCO2e per employee or null",
    "yoy_change_pct": number_or_null
  },
  "scope_1_breakdown": [
    {"source":"stationary combustion|mobile combustion|process|fugitive","tco2e":number,"notes":"string"}
  ],
  "scope_2_breakdown": [
    {"source":"electricity|heat|steam|cooling","tco2e_market":number,"tco2e_location":number,"location":"string or null"}
  ],
  "scope_3_breakdown": [
    {
      "category": "1-15 GHG Protocol category number",
      "name": "Purchased goods|Capital goods|Fuel and energy|...",
      "tco2e": number,
      "estimation_method": "spend_based|activity_based|hybrid",
      "confidence": "high|medium|low"
    }
  ],
  "emission_factors_used": [
    {"source":"string","factor":"string","year":"string"}
  ],
  "reduction_opportunities": [
    {
      "action": "specific action",
      "scope": "1|2|3",
      "potential_reduction_tco2e": number,
      "cost_estimate": "low|medium|high|revenue_generating",
      "timeline": "immediate|1_year|2_3_years|5_plus_years",
      "co_benefits": ["cost savings","employee satisfaction","brand value"],
      "implementation_steps": ["step 1","step 2"]
    }
  ],
  "science_based_targets": {
    "1_5c_pathway_reduction_needed_pct": number,
    "current_trajectory": "on_track|needs_acceleration|off_track",
    "recommended_target": "X% absolute reduction by 20XX",
    "notes": "string"
  },
  "industry_benchmarks": {
    "industry": "string",
    "your_intensity": number,
    "industry_median_intensity": number_or_null,
    "percentile": "top_25|median|bottom_25|unknown",
    "benchmark_source": "string"
  },
  "quick_wins": ["3-5 immediate actions with highest impact-to-effort ratio"],
  "data_quality_notes": ["gaps or assumptions made in the calculation"],
  "disclaimer": "This estimate is based on provided data. Formal reporting requires third-party verification.",
  "confidence": 0.0
}"""

def calculate(activity_data: str, company_name: str = "", year: str = "", revenue_m: float = 0, employees: int = 0) -> dict:
    client = anthropic.Anthropic()
    context_parts = [
        f"Company: {company_name}" if company_name else "",
        f"Reporting year: {year}" if year else "",
        f"Annual revenue: ${revenue_m}M" if revenue_m else "",
        f"Employees: {employees:,}" if employees else "",
        f"\nActivity data:\n{activity_data}"
    ]
    prompt = "\n".join(p for p in context_parts if p)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Calculate carbon footprint:\n\n{prompt}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def calculate_file(path: str, **kwargs) -> dict:
    from pathlib import Path
    return calculate(Path(path).read_text(encoding="utf-8",errors="replace")[:30000], **kwargs)

TRAJ_ICON = {"on_track":"🟢","needs_acceleration":"🟡","off_track":"🔴"}

def print_report(r: dict):
    s = r.get("summary",{})
    sbt = r.get("science_based_targets",{})
    bench = r.get("industry_benchmarks",{})

    print(f"\n{'═'*60}")
    print(f"  CARBON FOOTPRINT — {r.get('company_name','?')} ({r.get('reporting_year','?')})")
    print(f"  Methodology: {r.get('methodology','GHG Protocol')}")
    print(f"{'═'*60}")

    total = s.get("total_tco2e",0)
    print(f"\n  TOTAL: {total:,.1f} tCO2e")
    print(f"\n  Scope 1 (direct):          {s.get('scope_1_tco2e',0):>10,.1f} tCO2e")
    print(f"  Scope 2 (energy, market):  {s.get('scope_2_market_based_tco2e',0):>10,.1f} tCO2e")
    if s.get("scope_3_tco2e"): print(f"  Scope 3 (value chain):     {s.get('scope_3_tco2e',0):>10,.1f} tCO2e")
    if s.get("revenue_intensity"): print(f"\n  Intensity: {s['revenue_intensity']}")
    if s.get("yoy_change_pct") is not None:
        arrow = "📈" if s["yoy_change_pct"] > 0 else "📉"
        print(f"  YoY change: {arrow} {s['yoy_change_pct']:+.1f}%")

    s3 = r.get("scope_3_breakdown",[])
    if s3:
        print(f"\n  SCOPE 3 BREAKDOWN (top sources)")
        sorted_s3 = sorted(s3, key=lambda x: x.get("tco2e",0), reverse=True)
        for cat in sorted_s3[:5]:
            pct = cat.get("tco2e",0)/total*100 if total else 0
            print(f"  Cat {cat.get('category','?'):>2}  {cat.get('name','?'):<35} {cat.get('tco2e',0):>8,.1f} tCO2e ({pct:.1f}%)")

    reductions = r.get("reduction_opportunities",[])
    if reductions:
        total_potential = sum(r2.get("potential_reduction_tco2e",0) for r2 in reductions)
        print(f"\n  REDUCTION OPPORTUNITIES ({len(reductions)}, {total_potential:,.0f} tCO2e potential)")
        sorted_r = sorted(reductions, key=lambda x: x.get("potential_reduction_tco2e",0), reverse=True)
        cost_icon = {"low":"💚","medium":"🟡","high":"🔴","revenue_generating":"💰"}
        time_icon = {"immediate":"⚡","1_year":"📅","2_3_years":"🗓","5_plus_years":"🔮"}
        for opp in sorted_r[:5]:
            cost = cost_icon.get(opp.get("cost_estimate","medium"),"•")
            time = time_icon.get(opp.get("timeline","1_year"),"•")
            print(f"\n  {cost}{time} [{opp.get('scope','?')}] {opp.get('action','')}")
            print(f"     Potential: {opp.get('potential_reduction_tco2e',0):,.0f} tCO2e | Timeline: {opp.get('timeline','?')}")
            steps = opp.get("implementation_steps",[])
            if steps: print(f"     Step 1: {steps[0]}")

    if sbt:
        traj = sbt.get("current_trajectory","off_track")
        print(f"\n  SCIENCE-BASED TARGETS")
        print(f"  Trajectory: {TRAJ_ICON.get(traj,'')} {traj.replace('_',' ')}")
        print(f"  Need to reduce: {sbt.get('1_5c_pathway_reduction_needed_pct','?')}%")
        print(f"  Recommended: {sbt.get('recommended_target','')}")

    qw = r.get("quick_wins",[])
    if qw:
        print(f"\n  QUICK WINS")
        for w in qw: print(f"  ⚡ {w}")

    if bench.get("percentile") and bench["percentile"] != "unknown":
        print(f"\n  vs Industry ({bench.get('industry','?')}): {bench.get('percentile','?').replace('_',' ')}")

    print(f"\n  Confidence: {int(r.get('confidence',0)*100)}%")
    print(f"  ⚠ {r.get('disclaimer','')}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Calculate carbon footprint from activity data")
    p.add_argument("source", help="Activity data file or '-' for stdin")
    p.add_argument("--company","-c",default="")
    p.add_argument("--year","-y",default="")
    p.add_argument("--revenue","-r",type=float,default=0,help="Annual revenue in $M")
    p.add_argument("--employees","-e",type=int,default=0)
    p.add_argument("--json",action="store_true")
    a = p.parse_args()
    from pathlib import Path
    src = sys.stdin.read() if a.source=="-" else (Path(a.source).read_text(errors="replace") if Path(a.source).exists() else a.source)
    r = calculate(src, a.company, a.year, a.revenue, a.employees)
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_report(r)
