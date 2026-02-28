from typing import List, Dict, Any, Optional
from src.models import UserSession, Domain, Indicator

class QuestionnaireSession:
    """
    Manages the interactive data collection process.
    """
    def __init__(self):
        self.session = UserSession()

    def ask_rating(self, prompt: str) -> int:
        """Asks for a 0-4 rating."""
        print(f"\n{prompt}")
        print("0 = Not at all | 1 = Rarely | 2 = Sometimes | 3 = Often | 4 = Almost always")
        while True:
            try:
                val = input("Your answer (0-4): ").strip()
                n = int(val)
                if 0 <= n <= 4:
                    return n
            except ValueError:
                pass
            print("Please enter a number between 0 and 4.")

    def ask_yes_no(self, prompt: str) -> bool:
        """Asks a Yes/No question."""
        print(f"\n{prompt} (y/n)")
        while True:
            val = input().strip().lower()
            if val in ['y', 'yes']:
                return True
            if val in ['n', 'no']:
                return False
            print("Please answer y or n.")

    def ask_text(self, prompt: str) -> str:
        """Asks for an open-ended text response."""
        print(f"\n{prompt}")
        return input("Your thoughts: ").strip()

    def run(self) -> UserSession:
        print("\n=== AI Mental Health Pattern Analysis (Research-Grade) ===")
        print("This is a tool for awareness and pattern recognition, NOT diagnosis.")
        print("I will ask about various aspects of your life to identify patterns.")
        print("You can skip any open-ended question by pressing Enter.\n")

        # --- 1. Bio & Phys ---
        bio = Domain(name="Biological")
        
        # Sleep
        sleep_qual = self.ask_rating("I feel rested after sleeping.")
        bio.add_indicator(Indicator(name="Sleep Quality", value=(4-sleep_qual)/4, description="Lack of restful sleep", domain="Biological")) 
        
        # Adaptive: Sleep Quality
        if sleep_qual <= 2:
            print("   > Adaptive Check: Low sleep quality detected.")
            pre_sleep = self.ask_rating("My pre-sleep routine involves high screen use or stimulation.")
            bio.add_indicator(Indicator(name="Pre-Sleep Stimulation", value=pre_sleep/4, description="Disruptive pre-sleep routine", domain="Biological"))

        sleep_var = self.ask_rating("My sleep schedule changes significantly day-to-day.")
        
        trend = "Stable"
        if sleep_qual <= 2: 
             if self.ask_yes_no("Has your sleep quality gotten worse in the last month?"):
                 trend = "Worsening"
        
        bio.add_indicator(Indicator(name="Sleep Variability", value=sleep_var/4, description="Inconsistent sleep timing", domain="Biological", trend=trend))

        # Physical Health
        fatigue = self.ask_rating("I experience unexplained physical fatigue or low energy.")
        f_trend = "Stable"
        if fatigue >= 3:
             if self.ask_yes_no("Is this fatigue a new or worsening development?"):
                 f_trend = "Worsening"
        bio.add_indicator(Indicator(name="Fatigue", value=fatigue/4, description="Physical exhaustion", domain="Biological", trend=f_trend))
        
        # Stress (New)
        stress = self.ask_rating("I feel under high stress or pressure in my daily life.")
        s_trend = "Stable"
        if stress >= 3:
             if self.ask_yes_no("Has this pressure increased recently?"):
                 s_trend = "Worsening"
             
             # Adaptive: Physical Manifestations
             print("   > Adaptive Check: High stress reported.")
             tension = self.ask_rating("I notice physical signs of stress (headaches, muscle tension, stomach issues).")
             bio.add_indicator(Indicator(name="Somatic Stress", value=tension/4, description="Physical stress manifestation", domain="Biological"))

        bio.add_indicator(Indicator(name="Stress Load", value=stress/4, description="General stress level", domain="Biological", trend=s_trend))

        self.session.add_domain(bio)

        # --- 2. Lifestyle ---
        life = Domain(name="Lifestyle")
        
        # Nutrition
        diet_irr = self.ask_rating("My eating habits are irregular or skipped often.")
        life.add_indicator(Indicator(name="Diet Irregularity", value=diet_irr/4, description="Inconsistent nutrition", domain="Lifestyle"))
        
        hydration = self.ask_rating("I drink enough water throughout the day.")
        life.add_indicator(Indicator(name="Dehydration", value=(4-hydration)/4, description="Poor hydration", domain="Lifestyle"))

        # Activity
        sedentary = self.ask_rating("I spend most of my day sitting (excluding sleep).")
        life.add_indicator(Indicator(name="Sedentary Time", value=sedentary/4, description="Lack of movement", domain="Lifestyle"))
        
        # Substance Use (Branching)
        use_substances = self.ask_yes_no("Do you use caffeine, alcohol, or nicotine regularly?")
        if use_substances:
            caffeine = self.ask_rating("I consume high amounts of caffeine (coffee, energy drinks).")
            life.add_indicator(Indicator(name="Caffeine Intake", value=caffeine/4, description="Stimulant use", domain="Lifestyle"))
            
            alcohol = self.ask_rating("I use alcohol or substances to cope with stress or sleep.")
            life.add_indicator(Indicator(name="Substance Coping", value=alcohol/4, description="Substance-based coping", domain="Lifestyle"))
        
        # Screen Time
        screen_time = self.ask_rating("I spend a significant amount of free time on screens/social media.")
        life.add_indicator(Indicator(name="Screen Time", value=screen_time/4, description="Digital consumption", domain="Lifestyle"))
        
        if screen_time >= 3:
             doomscrolling = self.ask_rating("I find myself scrolling negatively affecting my mood.")
             life.add_indicator(Indicator(name="Doomscrolling", value=doomscrolling/4, description="Negative digital engagement", domain="Lifestyle"))

        self.session.add_domain(life)

        # --- 3. Psych ---
        psych = Domain(name="Psychological")
        
        worry = self.ask_rating("I struggle to stop worrying about the future.")
        w_trend = "Stable"
        if worry >= 3:
            if self.ask_yes_no("Have these worries become more frequent recently?"):
                w_trend = "Worsening"
        psych.add_indicator(Indicator(name="Anxiety/Worry", value=worry/4, description="Future-oriented anxiety", domain="Psychological", trend=w_trend))
        
        mood_stab = self.ask_rating("My mood shifts rapidly or feels intense.")
        psych.add_indicator(Indicator(name="Mood Instability", value=mood_stab/4, description="Emotional lability", domain="Psychological"))

        # Adaptive: Rumination
        if worry >= 3 or mood_stab >= 3:
             rumination = self.ask_rating("I tend to dwell on past mistakes or awkward interactions.")
             psych.add_indicator(Indicator(name="Rumination", value=rumination/4, description="Repetitive negative thinking", domain="Psychological"))

        self.session.add_domain(psych)

        # --- 4. Coping Strategies (NEW) ---
        coping_dom = Domain(name="Coping Strategies")
        avoidance = self.ask_rating("I tend to avoid problems rather than facing them immediately.")
        coping_dom.add_indicator(Indicator(name="Avoidance Coping", value=avoidance/4, description="Avoiding stressors", domain="Coping Strategies"))
        
        problem_solving = self.ask_rating("I usually have a plan to handle difficulties.")
        coping_dom.add_indicator(Indicator(name="Problem Solving", value=(4-problem_solving)/4, description="Lack of active planning", domain="Coping Strategies"))
        self.session.add_domain(coping_dom)

        # --- 5. Social & Env ---
        social = Domain(name="Social")
        isolation = self.ask_rating("I feel isolated or disconnected from others.")
        i_trend = "Stable"
        if isolation >= 3:
             if self.ask_yes_no("Do you feel more isolated now than a month ago?"):
                 i_trend = "Worsening"
        social.add_indicator(Indicator(name="Isolation", value=isolation/4, description="Social disconnection", domain="Social", trend=i_trend))
        self.session.add_domain(social)

        env = Domain(name="Environmental")
        noise = self.ask_rating("My living or work environment is noisy or chaotic.")
        env.add_indicator(Indicator(name="Environmental Noise", value=noise/4, description="Chaotic environment", domain="Environmental"))
        
        financial = self.ask_rating("Financial stress is a constant worry.")
        env.add_indicator(Indicator(name="Financial Pressure", value=financial/4, description="Economic Strain", domain="Environmental"))
        self.session.add_domain(env)

        # --- 6. Work/Dev ---
        work = Domain(name="Work/Academic")
        pressure = self.ask_rating("I feel overwhelmed by deadlines or expectations.")
        work.add_indicator(Indicator(name="Workload Pressure", value=pressure/4, description="Performance pressure", domain="Work/Academic"))
        self.session.add_domain(work)

        # --- 7. Developmental / Life Transitions (NEW) ---
        dev = Domain(name="Developmental")
        transition = self.ask_rating("I am currently going through a major life change (graduating, new job, moving).")
        dev.add_indicator(Indicator(name="Life Transition", value=transition/4, description="Major life change load", domain="Developmental"))
        
        identity = self.ask_rating("I feel unsure about my future path or identity.")
        dev.add_indicator(Indicator(name="Identity Stress", value=identity/4, description="Identity formation stress", domain="Developmental"))
        self.session.add_domain(dev)

        # Optional Specifics
        open_ended = self.ask_text("Is there anything else contributing to your stress right now? (Optional)")
        if open_ended:
             # Add to Psych/General or store separately? For now, add to Psych as qualitative
             psych.add_indicator(Indicator(name="User Notes", value=-1, description="Open text", domain="Psychological", text_value=open_ended))

        return self.session
