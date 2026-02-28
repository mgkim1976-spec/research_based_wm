import json
import logging
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from app.models.resources import ResearchReport, SmartMoneyVideo, HybridContentBundle

logger = logging.getLogger(__name__)

class ContentMatcher:
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        # In a real system, this would be a connection to ChromaDB or Pinecone.
        # For Stage 1 mock, we keep an in-memory history of 'embedded' reports.
        self.historical_reports_db: List[ResearchReport] = []
        
    def add_to_history(self, reports: List[ResearchReport]):
        self.historical_reports_db.extend(reports)

    def search_historical_reports(self, query_tags: List[str]) -> Optional[ResearchReport]:
        """Mock Vector Search: Finds a past report matching the current momentum tags."""
        best_match = None
        best_score = 0
        
        for report in self.historical_reports_db:
            score = len(set(report.tags).intersection(set(query_tags)))
            if score > best_score:
                best_score = score
                best_match = report
                
        # Return if there's a strong enough keyword overlap (mocking vector similarity > 0.7)
        return best_match if best_score > 0 else None

    def create_hybrid_bundle(self, 
                             report: Optional[ResearchReport], 
                             video: Optional[SmartMoneyVideo], 
                             routine_type: str) -> HybridContentBundle:
        """Matches a report and a video to create a bundle."""
        bundle_id = f"bndl_{uuid.uuid4().hex[:8]}"
        
        # 1. Matching Reason (Korean)
        if report and video:
            overlap = set(report.tags or []).intersection(set(video.tags or []))
            if overlap:
                match_reason = f"리서치와 영상의 공통 키워드({', '.join(overlap)})를 기반으로 매칭되었습니다."
            else:
                match_reason = "오늘의 시장 흐름과 가장 연관성이 높은 리서치와 영상을 선정하였습니다."
        elif report:
            match_reason = "오늘 가장 주목해야 할 핵심 리서치 리포트입니다."
        elif video:
            match_reason = "오늘의 시장 상황을 가장 잘 설명하는 스마트머니 영상입니다."
        else:
            match_reason = "매칭된 콘텐츠가 없습니다."
                
        # 2. Recommended CTA (Korean & Content-Aware)
        urgency = "Normal"
        recommended_cta = "추후 여유로운 시간에 확인해 보세요."
        
        if routine_type == "Routine A: Daily Morning":
            urgency = "High"
            if report and video:
                recommended_cta = "영상으로 빠른 시황을 파악한 후, 리포트 원문으로 세부 지표를 확인하세요."
            elif report:
                recommended_cta = "장 시작 전, 리포트의 핵심 Thesis를 정독하십시오."
            elif video:
                recommended_cta = "출근길 영상을 통해 밤사이 미국 증시 흐름을 빠르게 캐치하세요."
        elif routine_type == "Routine B: Biweekly Deep":
            urgency = "Medium"
            recommended_cta = "리포트 요약본을 읽고 포트폴리오 영향도를 PB와 상담하세요."
        elif routine_type == "Routine D: Educational":
            urgency = "Low"
            recommended_cta = "부담 없이 시청/정독하며 투자 시야를 넓혀보세요."
            
        return HybridContentBundle(
            bundle_id=bundle_id,
            routine_type=routine_type,
            report_id=report.report_id if report else None,
            video_id=video.video_id if video else None,
            match_reason=match_reason,
            target_segments=[], # to be filled by the router
            pb_summary="", # to be filled by AI
            client_summary="", # to be filled by AI
            recommended_cta=recommended_cta,
            urgency=urgency,
            confidence="High" if (report and video) else "Medium",
            compliance_notes="내부 PB 보조용 초안입니다. 수정 없이 고객에게 그대로 전달하지 마십시오."
        )
