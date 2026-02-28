from src.models import UserSession, Domain, Indicator
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator

def create_session(scenario_name, stress_load, sleep_var, support, financial):
    session = UserSession()
    
    bio = Domain(name="Biological")
    bio.add_indicator(Indicator(name="Stress Load", value=stress_load, description="stress", domain="Biological"))
    # Assume 1.0 - stress_load is recovery for simplicity in this quick test builder
    bio.add_indicator(Indicator(name="Recovery", value=1.0 - stress_load, description="recovery", domain="Biological"))
    session.add_domain(bio)
    
    lifestyle = Domain(name="Lifestyle")
    lifestyle.add_indicator(Indicator(name="Sleep Variability", value=sleep_var, description="sleep var", domain="Lifestyle"))
    session.add_domain(lifestyle)
    
    social = Domain(name="Social")
    # Low support means high isolation
    isolation = 1.0 - support
    social.add_indicator(Indicator(name="Isolation", value=isolation, description="isolation", domain="Social"))
    session.add_domain(social)
    
    env = Domain(name="Environmental")
    env.add_indicator(Indicator(name="Financial Pressure", value=financial, description="financial", domain="Environmental"))
    session.add_domain(env)
    
    return session

def run_test():
    print("Running Test Scenarios...\n")
    
    scenarios = [
        ("High Risk", 0.8, 0.9, 0.2, 0.8), # High stress, high sleep var, low support, high financial
        ("Low Risk", 0.2, 0.1, 0.9, 0.1),  # Low stress, stable sleep, high support, low financial
        ("Resilient (Mixed)", 0.8, 0.3, 0.9, 0.7), # High stress & financial, but stable sleep & high support
    ]
    
    analyzer = PatternAnalyzer()
    generator = ResponseGenerator()
    
    for name, stress, sleep, support, finan in scenarios:
        print(f"--- Scenario: {name} ---")
        session = create_session(name, stress, sleep, support, finan)
        patterns = analyzer.analyze(session)
        session.identified_patterns = patterns
        report = generator.generate_report(session)
        print(report)
        print("\n" + "="*30 + "\n")

if __name__ == "__main__":
    run_test()
