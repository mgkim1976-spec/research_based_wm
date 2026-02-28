import logging
from typing import List, Dict
from datetime import datetime
import uuid

from app.core.adapters.research_crawler import MiraeResearchCrawler
from app.core.adapters.youtube_connector import SmartMoneyConnector
from app.core.ai.openai_engine import OpenAIEngine
from app.core.engine.matcher import ContentMatcher
from app.core.engine.router import SegmentRouter
from app.models.resources import AuditRecord, PBActionDraft, HybridContentBundle

logger = logging.getLogger(__name__)

class WorkflowOrchestrator:
    def __init__(self):
        self.crawler = MiraeResearchCrawler()
        self.yt_connector = SmartMoneyConnector()
        self.ai = OpenAIEngine()
        self.matcher = ContentMatcher(self.ai)
        self.router = SegmentRouter(self.ai)
        
    def run_routine_a_morning(self, target_report_id: str = None) -> Dict[str, any]:
        """
        Workflow 1: Daily Morning Hybrid Routine
        1. Discover daily market reports
        2. Discover daily SmartMoney videos
        3. Parse & match
        4. Identify customers and generate drafts
        5. Write audit artifact
        """
        logger.info("Starting Routine A: Daily Morning Hybrid")
        
        # 1. Fetch Candidates (Store them for history)
        reports = self.crawler.fetch_recent_reports(limit=5)
        self.crawler.save_reports(reports) 
        
        videos = []
        try:
            videos = self.yt_connector.fetch_recent_videos(limit=3)
        except Exception as e:
            logger.warning(f"Failed to fetch videos: {e}")
            
        # 2. Add to historical matcher DB for mock RAG
        self.matcher.add_to_history(reports)
        
        if not reports and not videos:
            return {"status": "error", "message": "오늘의 루틴을 생성할 새로운 리서치나 영상이 없습니다."}
            
        main_report = None
        if target_report_id:
            logger.info(f"Targeting specific report: {target_report_id}")
            for r in reports:
                if r.report_id == target_report_id:
                    main_report = r
                    break
            
            if not main_report:
                # Look in full history if not in top 5
                all_history = self.crawler.load_all_reports()
                for r in all_history:
                    if r.report_id == target_report_id:
                        main_report = r
                        logger.info(f"Report found in history: {r.title}")
                        break
        
        if not main_report and reports:
            main_report = reports[0]
            logger.info(f"Falling back to latest report: {main_report.report_id}")
        
        if not main_report:
            return {"status": "error", "message": "요청하신 리포트를 찾을 수 없습니다."}
            
        main_video = videos[0] if videos else None
        
        # Keep track of other candidate reports for today (excluding the one we currenty focus on)
        other_reports = [r for r in reports if r.report_id != main_report.report_id]
        
        # If the main report was from history, it won't be in the 'reports' list, 
        # so candidates stay as they were fetched.
        
        report_data = {}
        if main_report:
            # Fetch full contents if possible
            self.crawler.fetch_report_contents(main_report)
            report_data = self.ai.parse_research_report(main_report.normalized_text or main_report.title) 
            report_data['report_title'] = main_report.title # Pass Title to UI
            report_data['source_url'] = main_report.source_url # Pass URL to UI
            if main_report.attachment_urls:
                report_data["pdf_url"] = main_report.attachment_urls[0]
            main_report.tags = report_data.get("sector_impact", []) + report_data.get("asset_class_impact", [])
        else:
            report_data = {"thesis": "지정된 리서치 리포트가 없습니다.", "sector_impact": [], "asset_class_impact": []}
        
        video_data = {}
        if main_video:
            video_data = self.ai.analyze_video(main_video.title, main_video.description)
            video_data["source_url"] = main_video.source_url # Pass URL to UI
            main_video.tags = video_data.get("topic_tags", [])
            
        # 4. Matching
        bundle = self.matcher.create_hybrid_bundle(main_report, main_video, "Routine A: Daily Morning")
        
        # 5. Routing
        mock_customers = self.router.get_mock_customers()
        # Use empty dict if data is missing, so AI knows it's empty
        drafts: List[PBActionDraft] = self.router.route_and_draft(bundle, mock_customers, report_data or {}, video_data or {})
        
        # 6. Audit
        audit = AuditRecord(
            audit_id=f"audit_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            report_id=main_report.report_id if main_report else None,
            video_id=main_video.video_id if main_video else None,
            workflow_name="Routine A: Daily Morning",
            decision_points={"match_reason": bundle.match_reason, "target_segments": bundle.target_segments},
            generated_outputs={"draft_count": len(drafts)},
            rationale="Generated morning routine based on latest available contents."
        )
        
        return {
            "status": "success",
            "bundle": bundle,
            "drafts": drafts,
            "audit": audit,
            "report_data": report_data,
            "video_data": video_data,
            "other_reports": other_reports
        }
        
    def run_routine_b_biweekly(self) -> Dict[str, any]:
        # Similar structure adapted for Biweekly Deep Portfolio (Sector/Earnings)
        pass

    def run_routine_c_weekend(self) -> Dict[str, any]:
        # Similar structure adapted for Weekend Theme Discovery
        pass
        
    def run_routine_d_educational(self) -> Dict[str, any]:
        # Similar structure adapted for Educational Confidence Building
        pass
