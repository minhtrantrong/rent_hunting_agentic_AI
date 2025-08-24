import json
import re
from typing import Dict, Any, List
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class CVJDExtractorAgent:
    """
    Agent to extract structured data from CV and Job Description (JD),
    using regex first (fast + deterministic) and falling back to LLM if needed.
    """

    def __init__(self, model_id: str = "gemini-1.5-flash-latest"):
        self.model = Gemini(id=model_id)
        self.agent = Agent(
            model=self.model,
            description=(
                "You are an agent that extracts structured information "
                "from CVs and Job Descriptions, and compares them."
            ),
            instructions=(
                "Given a CV and a Job Description, extract skills, education, "
                "experience, qualifications, and responsibilities. "
                "Then compare the skills between CV and JD, "
                "and summarize matches, gaps, and extras."
            ),
            show_tool_calls=False
        )



    def detect_domain(self, text: str) -> str:
            """
            Detect job domain/industry from JD or CV using simple LLM classification.
            """
            prompt = f"""
            Identify the industry domain of the following job description or CV:
            {text}

            Choose one from: IT, Finance, Healthcare, Marketing, Education, Engineering, Sales, Other.
            Return only the domain as a single word.
            """
            result = self.agent.run(prompt)

            if hasattr(result, "content"):
                return result.content.strip()
            return str(result).strip()
    
    def analyze_jd_fields(self, jd_text: str, domain: str) -> List[str]:
        """
        Use LLM to analyze a JD (with domain context) and determine which fields 
        should be extracted for candidate comparison.

        Args:
            jd_text (str): Job description text.
            domain (str): Detected domain/industry (e.g., IT, Finance).

        Returns:
            List[str]: JSON list of field names, or default fallback.
        """
        prompt = f"""
        The job belongs to the domain: {domain}.

        Analyze the following Job Description text and identify the main fields
        that should be extracted for candidate comparison, considering this domain.

        Return the result strictly as a JSON list of field names 
        (e.g., ["Skills", "Qualifications", "Responsibilities", "Education", "Experience"]).
        
        JD Text:
        {jd_text}
        """
        response = self.agent.run(prompt)
        result = getattr(response, "content", str(response))

        try:
            fields = json.loads(result)
            if isinstance(fields, list):
                return fields
        except Exception:
            pass

        # fallback mặc định
        return ["Skills", "Qualifications", "Responsibilities", "Education", "Experience"]

        # ---------------------- EXTRACT METHODS ----------------------


    def extract_cv(self, cv_text: str) -> Dict[str, Any]:
        """
        Extract structured data from a CV.
        """
        patterns = {
            "Skills": r"Skills\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)",
            "Education": r"Education\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)",
            "Experience": r"(?:Experience|Work Experience|Professional Experience)\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)"
        }
        data = {}
        for key, pattern in patterns.items():
            data[key] = self._extract_pattern(cv_text, pattern, group=2 if key == "Experience" else 1)

        # fallback nếu không có dữ liệu
        if not any(data.values()):
            data = self._extract_with_llm(cv_text, "CV")

        return data

    def extract_jd(self, jd_text: str) -> Dict[str, Any]:
        """
        Extract structured data from a Job Description.
        """
        patterns = {
        "Skills": r"(?:Skills Required|Required Skills|Skills)\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)",
        "Qualifications": r"(?:Qualifications|Requirements)\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)",
        "Responsibilities": r"(?:Responsibilities|Duties)\s*\n([\s\S]*?)(?=\n[A-Z][a-zA-Z ]*\n|$)"
    }

        data = {}
        for key, pattern in patterns.items():
            data[key] = self._extract_pattern(jd_text, pattern, group=2)

        if not any(data.values()):
            data = self._extract_with_llm(jd_text, "Job Description")

        return data

    # ---------------------- COMPARISON ----------------------

    def compare_cv_jd(self, cv_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare skills between CV and JD.
        """
        cv_skills = set(self._normalize_list(self._split_items(cv_data.get("Skills", ""))))
        jd_skills = set(self._normalize_list(self._split_items(jd_data.get("Skills", ""))))

        matched = cv_skills & jd_skills
        missing = jd_skills - cv_skills
        extra = cv_skills - jd_skills

        return {
            "Matched Skills": sorted(matched),
            "Missing Skills (JD)": sorted(missing),
            "Extra Skills (CV)": sorted(extra)
        }

    # ---------------------- HELPER METHODS ----------------------

    def compare_cv_jd_2(self, cv_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dynamically compares CV and JD using an LLM to extract skills, experience, and qualifications alignment.
        """

        # --- Prompt-based comparison ---
        prompt = f"""
        Compare the following candidate CV data with the Job Description (JD).
        Focus on skills, experience, and qualifications. Extract matched items, missing items,
        and extra items. Return the result as structured JSON with keys:
        - Matched Skills
        - Missing Skills (JD)
        - Extra Skills (CV)
        - Experience Matches
        - Experience Missing (JD)
        - Matched Qualifications
        - Missing Qualifications (JD)
        - Extra Qualifications (CV)

        CV Data:
        {cv_data}

        JD Data:
        {jd_data}
        """

        result = self.agent.run(prompt)

        try:
            # Ensure valid JSON response
            import json
            comparison = json.loads(result.content if hasattr(result, "content") else str(result))
        except Exception:
            # fallback: return raw text if JSON parsing fails
            comparison = {"raw_output": result.content if hasattr(result, "content") else str(result)}

        return comparison

    def _extract_pattern(self, text: str, pattern: str, group: int = 1) -> str:
        """
        Extract text using regex pattern.
        """
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            if isinstance(matches[0], tuple):
                return " ".join(m[group].strip() for m in matches if len(m) > group and m[group].strip())
            return " ".join(m.strip() for m in matches if m.strip())
        return ""

    def _split_items(self, items: str) -> List[str]:
        """
        Split items by commas, semicolons, or newlines.
        """
        return [i.strip() for i in re.split(r"[;,\n]", items) if i.strip()]

    def _normalize_list(self, items: List[str]) -> List[str]:
        """
        Normalize list items to lowercase and remove special chars.
        """
        return [re.sub(r"[^a-z0-9+# ]", "", i.lower()).strip() for i in items]

    def _extract_with_llm(self, text: str, doc_type: str) -> Dict[str, Any]:
        """
        Fallback extraction using LLM when regex fails.
        """
        prompt = (
            f"Extract structured information from the following {doc_type}:\n\n{text}\n\n"
            "Return JSON with fields: Skills, Education, Experience, Qualifications, Responsibilities."
        )
        response = self.agent.run(prompt)
        return response if isinstance(response, dict) else {}

# ---------------------- DEMO ----------------------
if __name__ == "__main__":
    cv_text = """Skills
Python, SQL, Data Visualization, Machine Learning, Deep Learning, Tableau, TensorFlow, Data Analysis

Education
Master of Data Science, University of Toronto, 2020
Bachelor of Computer Science, ABC University, 2018

Experience
Data Scientist, FinTech Solutions Inc, 2020–2024
- Built predictive models for customer churn using Python and TensorFlow.
- Developed interactive dashboards with Tableau and SQL for business stakeholders.
- Collaborated with engineering team to deploy ML models into production.

Data Analyst, Retail Insights Ltd, 2018–2020
- Conducted sales forecasting using regression models.
- Automated reporting pipelines using SQL and Python.
- Presented analytical findings to marketing and operations teams.
"""
    jd_text = """Skills Required
Python, SQL, Machine Learning, Communication, Cloud Platforms (AWS or GCP), Data Engineering

Qualifications
Master’s degree in Computer Science, Data Science, or related field
3+ years of professional experience in data-focused roles

Responsibilities
- Design and implement scalable ML models for financial risk analysis.
- Work with cross-functional teams to translate business requirements into data-driven solutions.
- Maintain data pipelines and ensure high-quality data availability.
- Communicate findings and insights effectively to both technical and non-technical audiences.
"""

    agent = CVJDExtractorAgent()
    cv_data = agent.extract_cv(cv_text)
    jd_data = agent.extract_jd(jd_text)
    comparison = agent.compare_cv_jd_2(cv_data, jd_data)

    print("CV Data:", cv_data)
    print("JD Data:", jd_data)
    print("Comparison:", comparison)
