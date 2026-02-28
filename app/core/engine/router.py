import uuid
from typing import List, Dict
from app.models.resources import CustomerProfile, HybridContentBundle, PBActionDraft
from app.core.ai.openai_engine import OpenAIEngine

class SegmentRouter:
    def __init__(self, ai_engine: OpenAIEngine):
        self.ai = ai_engine
        
    def get_mock_customers(self) -> List[CustomerProfile]:
        """Returns mock customers for testing Stage 1 logic without CRM."""
        return [
            CustomerProfile(
                customer_id="cust_001",
                segment_id="S1",
                asset_tier="Low",
                trading_frequency="Low",
                modifiers=["Novice", "Video-preferred"],
                engagement_level="Dormant"
            ),
            CustomerProfile(
                customer_id="cust_002",
                segment_id="S2",
                asset_tier="Low",
                trading_frequency="High",
                modifiers=["Active", "ETF-heavy"],
                engagement_level="Active"
            ),
            CustomerProfile(
                customer_id="cust_003",
                segment_id="S3",
                asset_tier="High",
                trading_frequency="Low",
                modifiers=["Conservative", "Loss-sensitive"],
                engagement_level="Moderate"
            ),
            CustomerProfile(
                customer_id="cust_004",
                segment_id="S4",
                asset_tier="High",
                trading_frequency="High",
                modifiers=["Expert", "Concentrated sector exposure"],
                engagement_level="Very Active"
            )
        ]

    def route_and_draft(self, bundle: HybridContentBundle, customers: List[CustomerProfile], report_data: Dict, video_data: Dict) -> List[PBActionDraft]:
        """Determines applicability and generates drafts for appropriate segments."""
        drafts = []
        
        for customer in customers:
            # Simple rule-based logic for Segment Applicability
            is_applicable = False
            delivery_mode = "Hybrid"
            priority = 0
            
            if bundle.routine_type == "Routine A: Daily Morning":
                is_applicable = True # Morning is broad
                priority = 5 if customer.segment_id in ["S2", "S4"] else 2
                delivery_mode = "Video-First" if customer.segment_id in ["S1", "S2"] else "Text-First"
                    
            elif bundle.routine_type == "Routine B: Biweekly Deep":
                if customer.segment_id in ["S3", "S4"]:
                    is_applicable = True
                    priority = 8
                    delivery_mode = "Text-First"
                    
            elif bundle.routine_type == "Routine D: Educational":
                if "Novice" in customer.modifiers or customer.segment_id == "S1":
                    is_applicable = True
                    priority = 3
                    delivery_mode = "Video-First"
            else:
                is_applicable = True
                priority = 1
                
            if is_applicable:
                # Use AI to generate segment-specific PB drafting
                draft_resp = self.ai.generate_pb_draft(
                    routine_type=bundle.routine_type,
                    segment=customer.segment_id,
                    report_data=report_data,
                    video_data=video_data,
                    delivery_mode=delivery_mode
                )
                
                # Assign to bundle's target_segments if not already there
                if customer.segment_id not in bundle.target_segments:
                    bundle.target_segments.append(customer.segment_id)
                
                # Handle the case where pb_talking_points might be returned as a list by AI
                talking_points_raw = draft_resp.get("pb_talking_points", "")
                if isinstance(talking_points_raw, list):
                    talking_points_str = "\n".join(talking_points_raw)
                else:
                    talking_points_str = str(talking_points_raw)
                
                client_message = str(draft_resp.get("client_message_draft", ""))
                # Replace video link placeholders if they exist
                if bundle.video_id:
                    video_url = f"https://www.youtube.com/watch?v={bundle.video_id}"
                    client_message = client_message.replace("[영상 링크]", video_url).replace("[Video Link]", video_url)
                
                draft = PBActionDraft(
                    action_id=f"act_{uuid.uuid4().hex[:8]}",
                    customer_id=customer.customer_id,
                    bundle_id=bundle.bundle_id,
                    routine_type=bundle.routine_type,
                    outreach_channel="Kakao/SMS",
                    pb_talking_points=talking_points_str,
                    client_message_draft=client_message,
                    follow_up_priority=priority,
                    traceability=f"Match Reason: {bundle.match_reason}"
                )
                drafts.append(draft)
                
        # Sort drafts by priority descending (Customer Queue ranking)
        drafts.sort(key=lambda x: x.follow_up_priority, reverse=True)
        return drafts
