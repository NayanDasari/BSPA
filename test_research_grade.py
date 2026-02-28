import sys
import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch

sys.path.append(os.getcwd())

from src.models import UserSession, Domain, Indicator
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator
from src.storage import StorageManager
from src.questionnaire import QuestionnaireSession

def create_history():
    print("Creating history...")
    storage = StorageManager(filename="research_test_history.json")
    if os.path.exists("research_test_history.json"):
        os.remove("research_test_history.json")
        
    # Baseline: Low Identity Stress (0.2)
    for i in range(3):
        s = UserSession()
        s.timestamp = datetime.now() - timedelta(days=i+1)
        dom = Domain(name="Developmental")
        dom.add_indicator(Indicator(name="Identity Stress", value=0.2, description="Base", domain="Devel"))
        s.add_domain(dom)
        # Add dummy domains to pass valid_history check (len > 2)
        s.add_domain(Domain(name="Bio")) 
        s.add_domain(Domain(name="Psych"))
        storage.save_session(s)

def run_research_test():
    print("\n--- Running Research-Grade Verification ---")
    
    # 1. Setup History
    create_history()
    
    # 2. Simulate User Input for Adaptive Session
    # Flow: 
    # Bio: Sleep Qual(1=Bad) -> [Adaptive: Pre-Sleep(3)], Sleep Var(3), Trend(Y), Fatigue(4)-Trend(Y), Stress(4)-Trend(Y) -> [Adaptive: Tension(3)]
    # Life: Diet(1), Hydr(1), Sedentary(4), Subst(N), Screen(4) -> [Adaptive: Doomscroll(3)]
    # Psych: Worry(4)-Trend(Y), Mood(4), [Adaptive: Ruminate(4)], Coping="Avoiding"
    # Coping(New): Avoidance(4), ProbSolv(1)
    # Social: Isol(4)-Trend(Y)
    # Env: Noise(1), Money(1)
    # Work: Press(1)
    # Dev(New): Trans(4), Identity(4)
    # Open: "Stressed about future"
    
    inputs = [
        "1", "3", "3", "y", "4", "y", "4", "y", "3", # Bio (Adaptive triggered)
        "1", "1", "4", "n", "4", "3", # Lifestyle (Adaptive triggered)
        "4", "y", "4", "4", "Avoidance", # Psych (Adaptive triggered)
        "4", "1", # Coping
        "4", "y", # Social
        "1", "1", # Env
        "1", # Work
        "4", "4", # Dev
        "Stressed about future" # Open
    ]
    
    input_iter = iter(inputs)
    def mock_input(prompt=""):
        try:
             val = next(input_iter)
             print(f"  Input: {val} (Prompt: {prompt[:30]}...)")
             return val
        except StopIteration:
             return "0"

    with patch('builtins.input', side_effect=mock_input):
        qs = QuestionnaireSession()
        session = qs.run()
        
        # Load History
        storage = StorageManager(filename="research_test_history.json")
        history = storage.load_history()
        
        # Analyze
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze(session, history)
        session.identified_patterns = patterns
        
        # Generate
        generator = ResponseGenerator()
        report = generator.generate_report(session)
        
        # Checks
        print("\n--- VERIFICATION CHECKS ---")
        
        if "Physical Manifestation" in str(session.domains["Biological"].indicators):
            print("[PASS] Adaptive Q: Somatic Stress captured.") # Name map check
        elif "Somatic Stress" in [i.name for i in session.domains["Biological"].indicators]:
             print("[PASS] Adaptive Q: Somatic Stress captured.")
        else:
             print("[FAIL] Adaptive Q: Somatic Stress MISSING.")

        if "Developmental" in session.domains:
            print("[PASS] New Domain: Developmental present.")
        else:
            print("[FAIL] New Domain: Developmental MISSING.")
            
        if "Transitional Identity Stress" in [p.name for p in patterns]:
            print("[PASS] New Pattern: Transitional Identity Stress detected.")
        else:
            print("[FAIL] New Pattern: Transitional Identity Stress MISSING.")
            
        if "Escalating Identity Stress" in [p.name for p in patterns]:
             print("[PASS] Longitudinal: Escalating Identity Stress detected (0.4 base -> 1.0 curr).")
        else:
             print(f"[FAIL] Longitudinal: Escalating Identity Stress MISSING. Found: {[p.name for p in patterns]}")
             
        if "# Mental Health Pattern Analysis Report (Research-Grade)" in report:
            print("[PASS] Report Header Correct.")
        else:
            print("[FAIL] Report Header Incorrect.")
            
        if "Arnett (2000)" in report:
            print("[PASS] Knowledge Base Citation Found (Arnett).")
        else:
            print("[FAIL] Knowledge Base Citation Missing.")

    # Cleanup
    if os.path.exists("research_test_history.json"):
        os.remove("research_test_history.json")

if __name__ == "__main__":
    run_research_test()
