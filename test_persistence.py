import sys
import os
import json
from datetime import datetime, timedelta

sys.path.append(os.getcwd())

from src.models import UserSession, Domain, Indicator
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator
from src.storage import StorageManager

def create_dummy_session(stress_val, days_ago=0):
    s = UserSession()
    s.timestamp = datetime.now() - timedelta(days=days_ago)
    s.data_completeness = 1.0 # Ensure valid
    
    bio = Domain(name="Biological")
    bio.add_indicator(Indicator(name="Stress Load", value=stress_val, description="Stress", domain="Biological"))
    s.add_domain(bio)
    return s

def test_persistence_logic():
    print("--- Testing Persistence & Longitudinal Analysis ---")
    
    filename = "test_history.json"
    if os.path.exists(filename):
        os.remove(filename)
        
    storage = StorageManager(filename=filename)
    
    # 1. Create History (Low Stress Baseline)
    print("1. Creating Baseline History (Stress ~0.3)...")
    base_1 = create_dummy_session(0.3, days_ago=3)
    base_2 = create_dummy_session(0.3, days_ago=2)
    base_3 = create_dummy_session(0.4, days_ago=1)
    
    storage.save_session(base_1)
    storage.save_session(base_2)
    storage.save_session(base_3)
    
    # 2. Load History
    loaded = storage.load_history()
    print(f"Loaded {len(loaded)} sessions.")
    if len(loaded) != 3:
        print("[FAIL] History load count mismatch.")
        return

    # 3. Create Current Session (High Stress Spike)
    print("2. Analyzing New Session (Stress 0.8)...")
    current = create_dummy_session(0.8)
    
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze(current, loaded)
    current.identified_patterns = patterns
    
    # 4. Verify Trend Detection
    escalation = next((p for p in patterns if "Escalating Stress Load" in p.name), None)
    
    if escalation:
        print(f"[PASS] Escalation Detected: {escalation.name}")
        print(f"      Desc: {escalation.description}")
    else:
        print("[FAIL] No Escalation Pattern Detected.")
        print(f"      Patterns Found: {[p.name for p in patterns]}")

    # 5. Generate Report
    generator = ResponseGenerator()
    report = generator.generate_report(current)
    
    if "Objective Deviation Detected" in report:
        print("[PASS] Report contains Objective Deviation Warning.")
    else:
        print("[FAIL] Report missing warning.")

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
        
if __name__ == "__main__":
    test_persistence_logic()
