from typing import List, Optional
from .models import Domain, Pattern, UserSession
from .knowledge_base import KnowledgeBase

class PatternAnalyzer:
    """
    Analyzes user data to identify non-linear patterns and interactions.
    """
    def __init__(self):
        self.kb = KnowledgeBase()

    def analyze(self, session: UserSession, history: List[UserSession] = []) -> List[Pattern]:
        detected_patterns = []

        # 1. Biological & Lifestyle Interactions
        bio = session.domains.get("Biological", None)
        lifestyle = session.domains.get("Lifestyle", None)
        if bio and lifestyle:
            sleep_var = next((i for i in lifestyle.indicators if i.name == "Sleep Variability"), None)
            stress_load = next((i for i in bio.indicators if i.name == "Stress Load"), None)

            if sleep_var and stress_load:
                if sleep_var.value > 0.7 and stress_load.value > 0.6:
                    ctx = self.kb.get_context("high_volatility_sleep_stress")
                    p = Pattern(
                        name="Compounding Sleep Volatility",
                        description="High sleep variability interacting with elevated stress load.",
                        severity="Elevated",
                        involved_domains=["Biological", "Lifestyle"],
                        evidence_context=ctx["context"],
                        protective_factors=[ctx["protective_factor"]]
                    )
                    detected_patterns.append(p)

        # 2. Social & Environmental Interactions
        social = session.domains.get("Social", None)
        env = session.domains.get("Environmental", None)
        if social and env:
            isolation = next((i for i in social.indicators if i.name == "Isolation"), None) # Higher value = more isolation
            financial = next((i for i in env.indicators if i.name == "Financial Pressure"), None)

            if isolation and financial:
                if isolation.value > 0.7 and financial.value > 0.6:
                     ctx = self.kb.get_context("social_isolation_financial_stress")
                     p = Pattern(
                        name="Resource-Strain Interaction",
                        description="Financial pressure amplified by lack of social buffering.",
                        severity="Elevated",
                        involved_domains=["Social", "Environmental"],
                        evidence_context=ctx["context"],
                        protective_factors=[ctx["protective_factor"]]
                     )
                     detected_patterns.append(p)

        # 3. Cognitive Load Analysis
        psych = session.domains.get("Psychological", None)
        if psych and bio:
             # Example: High cognitive load + low recovery
             cog_load = next((i for i in psych.indicators if i.name == "Cognitive Load"), None)
             recovery = next((i for i in bio.indicators if i.name == "Recovery"), None) 

             # Note: logic assumes 'Recovery' represents quality (higher is better)
             # If higher is better, low recovery is < 0.3
             if cog_load and recovery:
                 if cog_load.value > 0.8 and recovery.value < 0.4:
                     ctx = self.kb.get_context("sleep_deprivation_cognitive_load") 
                     p = Pattern(
                         name="Recovery-Load Imbalance",
                         description="High mental demand without sufficient physiological recovery.",
                         severity="Elevated",
                         involved_domains=["Psychological", "Biological"],
                         evidence_context=ctx["context"],
                         protective_factors=[ctx["protective_factor"]]
                     )
                     detected_patterns.append(p)

        # 4. Digital & Lifestyle Interactions (Phase 2)
        lifestyle = session.domains.get("Lifestyle", None)
        bio = session.domains.get("Biological", None)
        psych = session.domains.get("Psychological", None)

        if lifestyle and bio:
            screen_time = next((i for i in lifestyle.indicators if i.name == "Screen Time"), None)
            sleep_qual = next((i for i in bio.indicators if i.name == "Sleep Quality"), None)
            
            if screen_time and sleep_qual:
                if screen_time.value > 0.6 and sleep_qual.value > 0.5: # Both high risk
                     ctx = self.kb.get_context("digital_sleep_interference")
                     p = Pattern(
                         name="Digital-Sleep Interference",
                         description="High screen usage appearing to impact sleep quality.",
                         severity="Moderate",
                         involved_domains=["Lifestyle", "Biological"],
                         evidence_context=ctx["context"],
                         protective_factors=[ctx["protective_factor"]]
                     )
                     detected_patterns.append(p)
        
        if lifestyle and psych:
            # Sedentary - Anxiety
            sedentary = next((i for i in lifestyle.indicators if i.name == "Sedentary Time"), None)
            anxiety = next((i for i in psych.indicators if i.name == "Anxiety/Worry"), None)
            
            if sedentary and anxiety:
                if sedentary.value > 0.7 and anxiety.value > 0.6:
                     ctx = self.kb.get_context("sedentary_anxiety_loop")
                     p = Pattern(
                         name="Sedentary-Stress Loop",
                         description="Physical inactivity potentially reinforcing anxiety loops.",
                         severity="Moderate",
                         involved_domains=["Lifestyle", "Psychological"],
                         evidence_context=ctx["context"],
                         protective_factors=[ctx["protective_factor"]]
                     )
                     detected_patterns.append(p)

            # Diet - Mood
            diet = next((i for i in lifestyle.indicators if i.name == "Diet Irregularity"), None)
            mood = next((i for i in psych.indicators if i.name == "Mood Instability"), None)

            if diet and mood:
                if diet.value > 0.6 and mood.value > 0.6:
                    ctx = self.kb.get_context("diet_mood_connection")
                    p = Pattern(
                        name="Biological-Mood Correlation",
                        description="Irregular nutrition patterns associated with emotional variability.",
                        severity="Moderate",
                        involved_domains=["Lifestyle", "Psychological"],
                        evidence_context=ctx["context"],
                        protective_factors=[ctx["protective_factor"]]
                    )
                    detected_patterns.append(p)
            
            # Substance Coping
            substance = next((i for i in lifestyle.indicators if i.name == "Substance Coping"), None)
            if substance and substance.value > 0.3:
                 ctx = self.kb.get_context("substance_coping_cycle")
                 p = Pattern(
                     name="Substance-Stress Cycle",
                     description="Use of substances to manage stress, which may lower resilience over time.",
                     severity="Elevated",
                     involved_domains=["Lifestyle"],
                     evidence_context=ctx["context"],
                     protective_factors=[ctx["protective_factor"]]
                 )
                 detected_patterns.append(p)

        # 5. Developmental & Coping (New Phase 3)
        dev = session.domains.get("Developmental", None)
        coping = session.domains.get("Coping Strategies", None)
        psych = session.domains.get("Psychological", None)
        bio = session.domains.get("Biological", None)
        
        if dev and dev.average_level > 0.6:
             # Identity Stress is high
             ctx = self.kb.get_context("identity_stress_transition")
             p = Pattern(
                 name="Transitional Identity Stress",
                 description="High stress associated with current major life transitions/identity formation.",
                 severity="elevated",
                 involved_domains=["Developmental"],
                 evidence_context=f"{ctx['context']} (Source: {ctx['citation']})",
                 protective_factors=[ctx["protective_factor"]]
             )
             detected_patterns.append(p)
             
        if coping and psych:
            avoidance = next((i for i in coping.indicators if i.name == "Avoidance Coping"), None)
            anxiety = next((i for i in psych.indicators if i.name == "Anxiety/Worry"), None)
            
            if avoidance and anxiety and avoidance.value > 0.6 and anxiety.value > 0.6:
                 ctx = self.kb.get_context("avoidance_anxiety_loop")
                 p = Pattern(
                     name="Avoidance-Anxiety Loop",
                     description="Reliance on avoidance coping may be unintentionally maintaining anxiety levels.",
                     severity="Moderate",
                     involved_domains=["Coping Strategies", "Psychological"],
                     evidence_context=f"{ctx['context']} (Source: {ctx['citation']})",
                     protective_factors=[ctx["protective_factor"]]
                 )
                 detected_patterns.append(p)
                 
        if bio:
             somatic = next((i for i in bio.indicators if i.name == "Somatic Stress"), None)
             if somatic and somatic.value > 0.6:
                 ctx = self.kb.get_context("somatic_stress_feedback")
                 p = Pattern(
                     name="Somatic Stress Manifestation",
                     description="Physical stress signals (tension/pain) indicating high allostatic load.",
                     severity="Measured",
                     involved_domains=["Biological"],
                     evidence_context=f"{ctx['context']} (Source: {ctx['citation']})",
                     protective_factors=[ctx["protective_factor"]]
                 )
                 detected_patterns.append(p)

        # 6. Reinforcing Cycle Detection (Phase 4)
        cycles = self.detect_cycles(session)
        detected_patterns.extend(cycles)

        # 6. Longitudinal Analysis (Phase 5)
        trends = self.calculate_longitudinal_trends(session, history)
        detected_patterns.extend(trends)

        return detected_patterns

    def calculate_longitudinal_trends(self, session: UserSession, history: List[UserSession]) -> List[Pattern]:
        """
        Compares current session data against historical baseline (last 5 sessions).
        """
        patterns = []
        if not history:
            return patterns

        # Indicators to track
        track_list = ["Stress Load", "Sleep Variability", "Anxiety/Worry", "Fatigue", "Isolation", "Identity Stress"]
        
        # Helper to get value from a session
        def get_val(sess, i_name):
            for d in sess.domains.values():
                for i in d.indicators:
                    if i.name == i_name:
                        return i.value
            return None

        # Filter history to valid sessions (ignoring empty/broken ones)
        valid_history = [h for h in history if h.data_completeness > 0.5 or len(h.domains) > 2]
        if not valid_history:
            return patterns

        for name in track_list:
            current_val = get_val(session, name)
            if current_val is None: continue
            
            # Get historical values
            hist_vals = []
            for h in valid_history[-5:]: # Last 5 valid sessions
                 v = get_val(h, name)
                 if v is not None: hist_vals.append(v)
            
            if not hist_vals: continue
            
            avg = sum(hist_vals) / len(hist_vals)
            
            # Threshold: Current > Avg + 0.15 (absolute significant jump)
            if current_val > avg + 0.15:
                p = Pattern(
                    name=f"Escalating {name}",
                    description=f"{name} ({current_val:.2f}) is significantly higher than your recent baseline ({avg:.2f}).",
                    severity="Elevated",
                    involved_domains=["Longitudinal"],
                    evidence_context="Objective trend analysis indicates a significant deviation from your personal baseline.",
                    confidence="High"
                )
                patterns.append(p)
                
        return patterns

    def detect_cycles(self, session: UserSession) -> List[Pattern]:
        """
        Detects 3-step reinforcing loops (e.g. Stress -> Sleep -> Fatigue -> Stress)
        """
        cycles = []
        
        # Helper to get indicator value
        def get_val(d_name, i_name):
            dom = session.domains.get(d_name)
            if dom:
                ind = next((i for i in dom.indicators if i.name == i_name), None)
                if ind: return ind.value
            return 0.0

        # Define potential edges (A influences B)
        # Value > 0.6 means "High/Risk"
        
        # 1. Stress -> Sleep
        # 1. Stress -> Sleep
        stress = get_val("Biological", "Stress Load") 
        # Fallback: if general stress is not reported high, check specific workload
        if stress == 0.0: stress = get_val("Work/Academic", "Workload Pressure")
        
        sleep_var = get_val("Biological", "Sleep Variability")
        if sleep_var == 0.0: sleep_var = get_val("Biological", "Sleep Quality") # Inverted in model already?
            
        fatigue = get_val("Biological", "Fatigue")
        coping = get_val("Psychological", "Coping Style") # Text, can't measure easily? 
        # using Anxiety instead for loop
        anxiety = get_val("Psychological", "Anxiety/Worry")
        
        # Check Cycle: Stress -> Sleep -> Fatigue -> Stress/Anxiety
        # Nodes:
        # A: Stress/Workload (>0.6)
        # B: Sleep Issues (>0.6)
        # C: Fatigue (>0.6)
        # Link: Stress causes Sleep issues. Sleep issues cause Fatigue. Fatigue reduces resilience, increasing Stress impact.
        
        if stress > 0.6 and sleep_var > 0.6 and fatigue > 0.6:
            p = Pattern(
                name="Reinforcing Stress-Sleep-Fatigue Cycle",
                description="Detected a potential feedback loop: High Stress appears to disrupt Sleep, leading to Fatigue, which likely lowers resilience to Stress.",
                severity="Elevated",
                involved_domains=["Work/Academic", "Biological"],
                evidence_context="Research indicates these 'vicious cycles' are self-sustaining without targeted interruption (e.g., sleep stabilization).",
                confidence="High"
            )
            cycles.append(p)
            
        return cycles
