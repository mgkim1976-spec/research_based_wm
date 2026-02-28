import os
import json
import logging
from typing import Dict, Any, List
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logger = logging.getLogger(__name__)

class OpenAIEngine:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODEL_NAME", "gpt-4.1-mini")
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("OpenAI client not initialized. Missing OPENAI_API_KEY or openai package.")

    def parse_research_report(self, text: str) -> Dict[str, Any]:
        """Reads a research report text and extracts structured thesis."""
        if not self.client:
            return self._mock_report_parse(text)
            
        system_prompt = """You are an expert financial analyst at Mirae Asset. Always respond in KOREAN.
Extract a structured investment thesis from the following research report content.
If full text is provided, analyze it deeply. If only the title is provided, infer the core idea.
Return JSON ONLY with these fields:
- thesis (string): 핵심 아이디어 및 결론 (본문에 기반하거나 제목에서 유추)
- asset_class_impact (list of strings): 영향 자산군 (예: ["주식", "채권"])
- region_impact (list of strings): 영향 지역 (예: ["미국", "한국", "글로벌"])
- sector_impact (list of strings): 영향 섹터 (예: ["반도체", "방산"])
- company_impact (list of strings): 언급된 구체적인 티커나 기업명
- time_horizon (string): 투자 시계 (예: "단기 (1-3M)", "중기 (3-12M)", "장기 (1Y+)")
- risk_conditions (string): 주요 리스크 요인
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Report Content:\n{text[:15000]}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            logger.error(f"Error parsing report: {e}")
            return self._mock_report_parse(text)

    def analyze_video(self, title: str, description: str, transcript: str = "") -> Dict[str, str]:
        """Classifies a video's tone, topic, and education level."""
        if not self.client:
            return self._mock_video_parse(title)
            
        system_prompt = """You are an expert PB content curator. Always respond in KOREAN.
Classify the given YouTube video metadata and transcript.
Return JSON ONLY with these fields:
- education_level: "beginner", "intermediate", or "advanced" (문자열은 영어 그대로 유지)
- content_style: "urgent market", "analytical", "thematic", "educational", or "narrative" (문자열은 영어 그대로 유지)
- topic_tags: 주제 태그 리스트 (한국어로 작성)
- transcript_summary: 영상의 핵심 메시지를 2문장 내외의 한국어로 요약
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Title: {title}\nDesc: {description}\nTranscript: {transcript[:10000]}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            return self._mock_video_parse(title)

    def generate_pb_draft(self, 
                          routine_type: str, 
                          segment: str, 
                          report_data: Dict, 
                          video_data: Dict, 
                          delivery_mode: str) -> Dict[str, str]:
        """Generates PB-facing talking points and a client message draft."""
        if not self.client:
            return self._mock_draft(video_present=bool(video_data))
            
        system_prompt = f"""You are a master Private Banker (PB) at Mirae Asset Securities. Always respond in KOREAN.
Your task is to draft a message and talking points for a client based on a research report and a SmartMoney video.
Routine Type: {routine_type}
Target Segment: {segment}
Delivery Priority: {delivery_mode}

Tone Rules:
- S1/Novice: 친절하고 교육적이며 정중한 어조. 전문 용어 지양.
- S4/Expert: 간결하고 데이터 중심적이며 행동 중심적인 전략적 어조.
- 공통: 전문성을 유지하면서도 친근해야 함. 직접적인 투자 권유(Sell/Buy)가 아닌, 정보를 공유하고 소통을 유도하는 형태여야 함. 반드시 한국어로 답변할 것.

Return JSON ONLY with these fields:
- pb_summary: PB가 상황을 빨리 파악할 수 있도록 3줄 내외 한국어 요약.
- pb_talking_points: PB가 고객과 통화할 때 사용할 수 있는 불렛 포인트 (한국어).
- client_message_draft: 고객에게 보낼 카카오톡/문자 메시지 실제 본문 초안. 
  CRITICAL: 
  1. 제공된 Video Details가 비어있다면 영상에 대해 절대 언급하지 말고 [영상 링크]도 포함하지 마십시오.
  2. 영상이 있는 경우에만 [영상 링크]라는 텍스트를 메시지 적절한 위치에 포함하십시오.
  3. 리포트와 영상을 자연스럽게 결합하되, 하나가 결여된 경우 나머지 하나에 집중하십시오. (한국어)
"""
        prompt_content = f"""
Report Details: {json.dumps(report_data, ensure_ascii=False)}
Video Details: {json.dumps(video_data, ensure_ascii=False)}
"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.4
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating PB draft: {e}")
            return self._mock_draft(video_present=bool(video_data))

    # --- Mocks for fallback ---
    def _mock_report_parse(self, text: str) -> Dict:
        return {
            "thesis": "Placeholder thesis.",
            "asset_class_impact": ["Equities"],
            "region_impact": ["Global"],
            "sector_impact": ["Technology"],
            "company_impact": [],
            "time_horizon": "Medium-term",
            "risk_conditions": "Macro volatility"
        }
        
    def _mock_video_parse(self, title: str) -> Dict:
        return {
            "education_level": "intermediate",
            "content_style": "analytical",
            "topic_tags": ["Market Update"],
            "transcript_summary": "Video summary placeholder."
        }
        
    def _mock_draft(self, video_present: bool = True) -> Dict:
        msg = "안녕하세요 고객님, 오늘 주목해볼만한 시장 동향을 공유드립니다.\n\n"
        if video_present:
            msg += "[영상 링크]\n\n"
        msg += "궁금한 점 있으시면 언제든 연락주세요."
        return {
            "pb_summary": "Summary for PB",
            "pb_talking_points": "1. Point A\n2. Point B",
            "client_message_draft": msg
        }
