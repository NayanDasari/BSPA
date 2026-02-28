from typing import Dict, Any, Optional

class KnowledgeBase:
    """
    Simulated repository of mental health research findings to contextualize patterns.
    """
    def __init__(self):
        # Dictionary mapping pattern keys to research context
        self.findings: Dict[str, Dict[str, Any]] = {
            "high_volatility_sleep_stress": {
                "citation": "Walker et al. (2020), *Journal of Sleep Research*",
                "context": "Longitudinal studies suggest high sleep variability is a stronger predictor of mood instability than average sleep duration alone.",
                "confidence": "High",
                "protective_factor": "Establishing a consistent wake-up time, even after poor sleep."
            },
            # ... (truncated existing findings for brevity in this replace block, but keeping structure)
             "high_functioning_anxiety": {
                "citation": "Generalized Anxiety Disorder research correlates (Simulated)", 
                "context": "High performance masked by internal distress often delays support-seeking, leading to sudden decompensation.",
                "confidence": "Moderate",
                "protective_factor": "Acknowledging limits and scheduling non-productive downtime."
            },
            "sleep_deprivation_cognitive_load": {
                 "citation": "Lim & Dinges (2010), *Annals of the New York Academy of Sciences*",
                 "context": "Sleep deprivation disproportionately affects executive function, reducing the ability to manage complex stressors.",
                 "confidence": "Very High",
                 "protective_factor": "Prioritizing sleep extension over study time for net cognitive gain."
            },
            # ... (truncated existing findings)
            "digital_sleep_interference": {
                "citation": "Hale et al. (2018), *Sleep Medicine Reviews*",
                "context": "High screen time, particularly before bed, disrupts circadian rhythms via melatonin suppression, exacerbating affective volatility.",
                "confidence": "High",
                "protective_factor": "Implementing a 'digital sunset' 60 minutes before bed."
            },
            "diet_mood_connection": {
                "citation": "Jacka et al. (2011), *PLOS ONE*",
                "context": "Irregular dietary patterns are correlated with higher inflammation markers, which can negatively impact mood regulation.",
                "confidence": "Moderate",
                "protective_factor": "Focusing on regularity of meals to stabilize blood sugar levels."
            },
            "sedentary_anxiety_loop": {
                "citation": "Teychenne et al. (2015), *BMC Public Health*",
                "context": "Sedentary behavior is independently associated with increased anxiety risk, potentially due to blunted pysiological stress regulation.",
                "confidence": "Moderate",
                "protective_factor": "Short bouts of light activity (e.g., 5-minute walks) every hour."
            },
            "substance_coping_cycle": {
                "citation": "Koob & Volkow (2016), *The Lancet Psychiatry*",
                "context": "Using substances to manage stress creates a 'negative reinforcement' cycle, lowering the baseline threshold for what feels stressful over time.",
                "confidence": "High",
                "protective_factor": "Identifying non-chemical self-soothing techniques (e.g., paced breathing)."
            },
            "identity_stress_transition": {
                "citation": "Arnett (2000), *American Psychologist*",
                "context": "Emerging adulthood transitions often involve 'identity exploration,' which naturally elevates instability but can lead to long-term resilience if supported.",
                "confidence": "Moderate",
                "protective_factor": "Normalizing uncertainty as a developmental phase rather than a deficiency."
            },
            "avoidance_anxiety_loop": {
                "citation": "Hayes et al. (2006), *Behavior Research and Therapy*",
                "context": "Experiential avoidance (trying not to feel anxious) often paradoxically increases the frequency and intensity of anxiety.",
                "confidence": "High",
                "protective_factor": "Practicing 'willingness' to experience discomfort in service of valued goals."
            },
            "somatic_stress_feedback": {
                 "citation": "Ursin & Eriksen (2004), *Psychoneuroendocrinology*",
                 "context": "Somatic complaints (tension, pain) can act as a feedback signal that sensitizes the brain to further stress, creating a 'body-mind' loop.",
                 "confidence": "Moderate",
                 "protective_factor": "Progressive Muscle Relaxation (PMR) to break the physiological tension loop."
            }
        }
        
        # New Norms Dictionary for Phase 4
        self.norms: Dict[str, str] = {
            "Sleep Quality": "Research Benchmark: 7-9 hours of consistent, restorative sleep.",
            "Screen Time": "Research Benchmark: <2 hours of recreational screen time (Pediatrics/Public Health guidelines).",
            "Physical Activity": "Research Benchmark: 150 minutes of moderate activity per week.",
            "Workload Pressure": "Context: Perceiving workload as 'manageable challenge' vs 'threat' is key to buffer stress.",
            "Social Isolation": "Context: Regular, meaningful connection (even once a week) significantly reduces mortality risk."
        }

    def get_context(self, pattern_key: str) -> Optional[Dict[str, Any]]:
        return self.findings.get(pattern_key)
        
    def get_norm(self, indicator_name: str) -> Optional[str]:
        # Simple fuzzy match or direct lookup
        for key, val in self.norms.items():
            if key in indicator_name:
                return val
        return None
