import sys
import os

# Ensure we can import from src
sys.path.append(os.getcwd())

from src.models import UserSession, Domain, Indicator
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator

def test_cycle_detection():
    print("Starting verification...")
    session = UserSession()
    
    # 1. Biological Domain with High Stress, Sleep Var, Fatigue + Trends
    bio = Domain(name="Biological")
    # Stress Load > 0.6 triggers cycle check
    bio.add_indicator(Indicator(name="Stress Load", value=0.8, description="High Stress", domain="Biological", trend="Worsening"))
    # Sleep Var > 0.6 triggers cycle check
    bio.add_indicator(Indicator(name="Sleep Variability", value=0.9, description="High Var", domain="Biological"))
    # Fatigue > 0.6 triggers cycle check
    bio.add_indicator(Indicator(name="Fatigue", value=0.7, description="High Fatigue", domain="Biological", trend="Worsening"))
    session.add_domain(bio)
    
    # Analyze
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze(session)
    session.identified_patterns = patterns
    
    # Generate
    generator = ResponseGenerator()
    report = generator.generate_report(session)
    
    # Checks
    print(f"Detected Patterns: {[p.name for p in patterns]}")
    
    cycle_found = "Reinforcing Stress-Sleep-Fatigue Cycle" in [p.name for p in patterns]
    if cycle_found:
        print("[PASS] Cycle Detected")
    else:
        print("[FAIL] Cycle NOT Detected")
        
    trend_found = "Diverging/Concerning" in report
    if trend_found:
         print("[PASS] Trend Worsening Detected")
    else:
         print(f"[FAIL] Trend Analysis Incorrect. Report excerpt:\n{report[report.find('Temporal Context'):report.find('Temporal Context')+200]}")

    graph_found = "graph LR" in report
    if graph_found:
        print("[PASS] Mermaid Graph Generated")
    else:
        print("[FAIL] No Mermaid Graph")
        
    if cycle_found and trend_found and graph_found:
        print("\nALL CHECKS PASSED")
    else:
        print("\nSOME CHECKS FAILED")

if __name__ == "__main__":
    test_cycle_detection()
