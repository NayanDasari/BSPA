from typing import List, Dict
from .models import Pattern, UserSession

from .knowledge_base import KnowledgeBase

class ResponseGenerator:
    """
    Constructs the final report from the detected patterns and session data.
    Strict research-grade formatting with 10 required sections.
    """
    def __init__(self):
        self.kb = KnowledgeBase()

    def generate_report(self, session: UserSession) -> str:
        report = []
        
        # 1. Non-Diagnostic Disclaimer
        report.append("# Mental Health Pattern Analysis Report (Research-Grade)")
        report.append("---")
        report.append("> [!IMPORTANT]")
        report.append("> **Non-Diagnostic Tool**: This analysis is for informational and research purposes only. It assesses behavioral patterns and environmental interactions but does NOT constitute a medical diagnosis. If you are in distress, please contact a qualified healthcare professional.")
        report.append("")

        # 2. Data Coverage & Confidence
        completeness = session.data_completeness * 100
        if completeness == 0.0: # Fallback calc if not set
             completeness = (len(session.domains) / 7.0) * 100
        
        report.append("## 1. Data Coverage & Confidence")
        report.append(f"| Input Completeness | Confidence Level | Analysis Scope |")
        report.append(f"| :--- | :--- | :--- |")
        conf_label = "High" if completeness > 80 else "Moderate"
        report.append(f"| **~{int(completeness)}%** | **{conf_label}** | 7 Key Domains |")
        report.append("")
        report.append("*Note: Coverage assessment based on Bio, Lifestyle, Psych, Social, Env, Work, and Developmental domains.*")
        report.append("")

        # 3. Detected Patterns
        report.append("## 2. Detected Patterns")
        report.append("The following patterns were identified based on cross-domain interactions and behavioral signals.")
        report.append("")
        
        patterns = [p for p in session.identified_patterns if "Longitudinal" not in p.involved_domains]
        
        if not patterns:
            report.append("No specific elevated stress patterns were detected based on current inputs. Maintaining your current routines appears beneficial.")
        else:
            for i, p in enumerate(patterns, 1):
                report.append(f"### {i}. {p.name}")
                report.append(f"{p.description}")
                report.append(f"- **Associated Domains**: {', '.join(p.involved_domains)}")
                report.append(f"- **Confidence**: {p.confidence}")
                report.append(f"- **Research Context**: *{p.evidence_context}*")
                if p.protective_factors:
                    report.append(f"- **Buffering Strategy**: {p.protective_factors[0]}")
                report.append("")

        # 4. Visualized Reinforcing Loops (Visuals)
        cycles = [p for p in session.identified_patterns if "Cycle" in p.name]
        if cycles:
            report.append("## 3. Visualized Reinforcing Loops")
            report.append("Feedback loops detected in your data that may strongly influence self-regulation:")
            for c in cycles:
                 if "Stress-Sleep-Fatigue" in c.name:
                     report.append("```mermaid")
                     report.append("graph LR")
                     report.append("    A[High Stress] -->|Disrupts| B[Sleep]")
                     report.append("    B -->|Increases| C[Fatigue]")
                     report.append("    C -->|Reduces Resilience| A")
                     report.append("    style A fill:#f9f,stroke:#333")
                     report.append("    style B fill:#bbf,stroke:#333")
                     report.append("    style C fill:#bfb,stroke:#333")
                     report.append("```")
            report.append("")

        # 5. Domain Overview (Table)
        report.append("## 4. Domain Overview & Pattern Density")
        report.append("| Domain | Pattern Density | Signal/Trend |")
        report.append("| :--- | :--- | :--- |")
        
        for name, domain in session.domains.items():
            level = "Low"
            if domain.average_level > 0.3: level = "Moderate"
            if domain.average_level > 0.6: level = "**Elevated**"
            
            trend_str = "Stable"
            worsening = [i for i in domain.indicators if i.trend == "Worsening"]
            if worsening:
                trend_str = "⚠️ **Worsening**"
            
            report.append(f"| {name} | {level} | {trend_str} |")
        report.append("")
        report.append("*Summary: 'Elevated' density indicates a concentration of stress markers in that domain.*")
        report.append("")

        # 6. Cross-Domain Interaction Summary
        report.append("## 5. Cross-Domain Interaction Summary")
        interactions = [p for p in patterns if len(p.involved_domains) > 1]
        if interactions:
             report.append("Overview of how patterns in one domain may be reinforcing others:")
             for p in interactions:
                 report.append(f"- **{p.name}** illustrates the active link between **{p.involved_domains[0]}** and **{p.involved_domains[1]}**.")
        else:
             report.append("Patterns appear to be isolated within specific domains currently.")
        report.append("")

        # 7. Detected Protective Factors
        report.append("## 6. Detected Protective Factors")
        protective = []
        for name, domain in session.domains.items():
            if domain.average_level < 0.3:
                protective.append(name)
        
        if protective:
            report.append("The following domains appear to be functioning as stability buffers:\n")
            for p in protective:
                report.append(f"- **{p}**: Low stress load here provides resilience against challenges in other areas.")
        else:
            report.append("No strong protective domains detected. Building a 'safe harbor' routine is recommended.")
        report.append("")

        # 8. Temporal Context & Trend Analysis
        report.append("## 7. Temporal Context & Trend Analysis")
        
        # Longitudinal
        longitudinal = [p for p in session.identified_patterns if "Longitudinal" in p.involved_domains]
        if longitudinal:
            report.append("### Objective Longitudinal Trends")
            for p in longitudinal:
                report.append(f"> [!WARNING]")
                report.append(f"> **{p.name}**: {p.description}")
            report.append("")
        
        # Self-Reported
        worsening_count = sum(1 for d in session.domains.values() for i in d.indicators if i.trend == "Worsening")
        report.append("### Self-Reported Trajectory")
        if worsening_count > 0:
            report.append(f"**Status: Diverging**. {worsening_count} indicators show recent worsening.")
            report.append("Use Caution: Recent changes in habits or environment may be accumulating load.")
        else:
             report.append("**Status: Stable**. No acute worsening reported.")
        report.append("")

        # 9. What Could Change This Analysis
        report.append("## 8. What Could Change This Analysis")
        report.append("Dynamic possibilities for pattern alteration:")
        report.append("- **Improving Sleep Consistency**: Could reduce 'Compounding Sleep Volatility' within 7-14 days.")
        report.append("- **Active Coping**: Shifting from avoidance to problem-solving often correlates with reduced anxiety frequency.")
        report.append("")

        # 10. Evidence-Informed Research Context
        report.append("## 9. Evidence-Informed Research Context")
        unique_contexts = list(set(p.evidence_context for p in session.identified_patterns if p.evidence_context))
        if unique_contexts:
             for c in unique_contexts:
                 report.append(f"- {c}")
        else:
             report.append("- *No specific interaction research cited for current low-risk profile.*")
        report.append("")

        # 11. Ethical & Safety Considerations
        report.append("## 10. Ethical & Safety Considerations")
        report.append("This system identifies patterns to support **self-awareness**. It includes the following limitations:")
        report.append("1. **Safety**: If you feel unsafe, please seek professional support immediately.")
        report.append("2. **Interpretation**: 'Elevated' means worth attention, not necessarily pathological.")
        report.append("3. **Privacy**: Data is stored locally on this machine only.")
        
        report.append("---")
        report.append("*Generated by AI Research Assistant v4.5 (Research-Grade Pattern Analysis).*")
        
        return "\n".join(report)
