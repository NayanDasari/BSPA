from unittest.mock import patch
from src.questionnaire import QuestionnaireSession
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator

def run_test_scenario(scenario_name, inputs):
    print(f"\n--- Running Scenario: {scenario_name} ---")
    
    # inputs is a list of strings that will be fed to input()
    # We use an iterator to feed them one by one
    input_iter = iter(inputs)
    
    def mock_input(prompt=""):
        val = next(input_iter)
        print(f"[User Input]: {val}")
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
            
            print("\nResult Report:")
            print(report)
        except StopIteration:
            print("Error: Not enough inputs provided for the scenario path.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Scenario: The "Digital Overload" Student
    # Profile:
    # - Sleep: Rested(1/4), Variable(3/4)
    # - Fatigue: Often(3/4)
    # - Diet: Irregular(3/4), Hydration(2/4)
    # - Sedentary: Often(3/4)
    # - Substances: Yes -> Caffeine(3/4), Alcohol(1/4)
    # - Screens: High(4/4) -> Doomscrolling(3/4)
    # - Psych: Worry(3/4), MoodInstab(2/4), Coping("Avoidance")
    # - Social: Isolation(2/4)
    # - Env: Noise(2/4), Financial(3/4)
    # - Work: Pressure(4/4)
    
    inputs = [
        # Bio
        "1", # Rested? (Low)
        "3", # Variable? (High)
        "3", # Fatigue? (High)
        # Lifestyle
        "3", # Diet Irregular? (High)
        "2", # Hydration? (Mod)
        "3", # Sedentary? (High)
        "y", # Substances? (Branch)
        "3", # Caffeine? (High)
        "1", # Alcohol? (Low)
        "4", # Screens? (Very High)
        "3", # Doomscrolling? (Branch triggered by >=3)
        # Psych
        "3", # Worry? (High)
        "2", # Mood Instab? (Mod)
        "I tend to just scroll on my phone explicitly to avoid thinking.", # Coping Text
        # Social
        "2", # Isolation? (Mod)
        # Env
        "2", # Noise? (Mod)
        "3", # Financial? (High)
        # Work
        "4"  # Pressure? (High)
    ]
    
    run_test_scenario("Digital Overload Student", inputs)
