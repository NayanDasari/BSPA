from unittest.mock import patch
from src.questionnaire import QuestionnaireSession
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator

def run_phase3_test(scenario_name, inputs):
    print(f"\n--- Running Phase 3 Verification: {scenario_name} ---")
    
    input_iter = iter(inputs)
    
    def mock_input(prompt=""):
        val = next(input_iter)
        # print(f"[User Input]: {val}") # Uncomment for debugging
        return val

    with patch('builtins.input', side_effect=mock_input):
        try:
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
            
        except StopIteration:
            print("Error: Not enough inputs provided.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Scenario: "Chronic Burnout with Recent Worsening"
    # Logic path:
    # 1. Sleep: Poor (1) -> Worsening? Yes -> High Var (3)
    # 2. Fatigue: High (4) -> Worsening? Yes
    # 3. Diet: Irregular (3) -> Hydration (1)
    # 4. Sedentary (3) -> Substances (y) -> Caffeine (3) -> Alcohol (2)
    # 5. Screens (4) -> Doomscrolling (3)
    # 6. Psych: Worry (3) -> Mood (3) -> Coping ("Withdrawal")
    # 7. Social (3) -> Env Noise (2) -> Financial (3)
    # 8. Work (4)
    
    inputs = [
        # Bio
        "1", # Sleep Rested (Low) -> Triggers trend question
        "3", # Sleep Variable
        "y", # Sleep Trend: Worsening?
        
        "4", # Fatigue (High) -> Triggers trend question
        "y", # Fatigue Trend: Worsening?
        
        # Lifestyle
        "3", # Diet Irregular
        "1", # Hydration
        
        "3", # Sedentary
        "y", # Substances?
        "3", # Caffeine
        "2", # Alcohol
        
        "4", # Screens -> Triggers Doomscrolling
        "3", # Doomscrolling
        
        # Psych
        "3", # Worry
        "3", # Mood
        "I withdraw and sleep more.", # Coping
        
        # Social
        "3", # Isolation
        
        # Env
        "2", # Noise
        "3", # Financial
        
        # Work
        "4"  # Pressure
    ]
    
    run_phase3_test("Chronic Burnout (Worsening)", inputs)
