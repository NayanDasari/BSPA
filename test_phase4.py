from unittest.mock import patch
from src.questionnaire import QuestionnaireSession
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator

def run_phase4_test(scenario_name, inputs):
    print(f"\n--- Running Phase 4 Verification: {scenario_name} ---")
    
    input_iter = iter(inputs)
    
    def mock_input(prompt=""):
        try:
            val = next(input_iter)
            return val
        except StopIteration:
            return "0" # Default safe fallback

    with patch('builtins.input', side_effect=mock_input):
        qs = QuestionnaireSession()
        session = qs.run()
        
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze(session)
        session.identified_patterns = patterns
        
        generator = ResponseGenerator()
        report = generator.generate_report(session)
        
        print("\n" + "="*50)
        print(report)
        print("="*50 + "\n")

if __name__ == "__main__":
    # Scenario: "The Vicious Cycle"
    # Stress (Work) -> Sleep Issues -> Fatigue -> Stress
    
    inputs = [
        # Bio
        "1", "y", "3", # Sleep: Poor, Worse, Variable (Risk)
        "4", "y",      # Fatigue: High, Worse (Risk)
        
        # Lifestyle
        "1", "1",      # Diet/Hydr
        "1", "n",      # Activity, Substances
        "1",           # Screens
        
        # Psych
        "1", "1", "Coping...", 
        
        # Social
        "1", 
        
        # Env
        "1", "1",
        
        # Work
        "4"  # Workload: High (Risk)
    ]
    
    run_phase4_test("Reinforcing Stress Cycle", inputs)
