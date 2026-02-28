from src.models import UserSession
from src.questionnaire import QuestionnaireSession
from src.analyzer import PatternAnalyzer
from src.generator import ResponseGenerator
from src.storage import StorageManager

def main():
    # 0. Load History
    storage = StorageManager()
    history = storage.load_history()
    print(f"Loaded {len(history)} past sessions.")

    # 1. Interactive Data Collection
    questionnaire = QuestionnaireSession()
    session = questionnaire.run()
    
    # 2. Analysis
    print("\nAnalyzing patterns based on your inputs & history...")
    analyzer = PatternAnalyzer()
    patterns = analyzer.analyze(session, history) 
    session.identified_patterns = patterns
    
    # 3. Generation
    print("Generating personalized research report...")
    generator = ResponseGenerator()
    report = generator.generate_report(session)
    
    print("\n" + "="*50)
    print(report)
    print("="*50 + "\n")

    # 4. Save Session
    save = input("Save this session to history? (y/n): ").strip().lower()
    if save in ['y', 'yes']:
        storage.save_session(session)

if __name__ == "__main__":
    main()
