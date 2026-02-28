You are designing and implementing **Stage 1** of a **Research + Video Hybrid PB Copilot** for **Mirae Asset Securities** using Antigravity.

# Mission

Build an internal-use **Research-to-Wealth Stage 1 system** that combines:

1. Mirae Asset Securities research reports and attached PDFs
2. Mirae Asset Securities YouTube channel **SmartMoney (@SmartMoney0)** video content
3. PB-oriented daily/weekly/biweekly/monthly customer engagement routines

This is **not** a retail auto-advisory engine in Stage 1.
This is an **internal PB enablement and orchestration system** that converts research + video into structured signals, segment-aware routines, PB drafts, and customer follow-up queues.

The system must support a **text + video hybrid asset-management routine** so that PBs can lower customer friction, improve comprehension, and match the content format to customer behavior and confidence level.

---

# Core Business Context

## Why this system exists

Traditional research reports are text-heavy and cognitively demanding.
SmartMoney video content lowers the psychological barrier by:

* visualizing research ideas
* giving expert voice and tone
* making difficult investment topics easier to absorb
* improving the chance that clients actually consume the content

The operating principle is:
**Do not send raw research alone when video can improve comprehension, habit formation, and actionability.**

Instead, create a **hybrid delivery routine**:

* report for precision
* video for comprehension and emotional accessibility
* PB message for trust and conversion
* segment-based delivery for relevance

---

# Stage 1 Objective

Implement the **internal operating layer** that:

1. discovers research reports
2. discovers related SmartMoney video content
3. maps research to video by topic, asset class, region, sector, and routine
4. generates PB-facing summaries and outreach drafts
5. recommends the right hybrid routine by customer segment
6. creates a follow-up priority queue
7. logs all actions for auditability

---

# Stage 1 Scope

## In Scope

* Mirae research ingestion adapter / MCP
* SmartMoney content discovery adapter / MCP or feed connector
* research parsing and signal extraction
* video metadata ingestion and topic extraction
* cross-modal matching between report and video
* routine scheduler logic
* segment-aware delivery recommendation
* PB summary generation
* consultation script generation
* mock customer ranking
* audit logs
* evaluation artifacts

## Out of Scope

* direct client trade execution
* auto-trading
* final regulated customer advice engine
* full compliance workflow automation
* full CRM / OMS integration
* aggressive crawling or bulk archiving of source content
* production-scale recommendation learning

---

# Strategic Rules

You must obey these rules:

1. **Internal-use only**

   * outputs are PB-assistive drafts, not final client advice

2. **No mass crawling**

   * prefer bounded discovery and item-level reads

3. **No raw research redistribution**

   * do not package original research as a customer-facing archive

4. **No raw video dumping**

   * do not treat videos as an indiscriminate link blast
   * pair them to a customer routine and rationale

5. **Traceability**

   * every hybrid recommendation must reference:

     * source report ID or URL
     * source video ID or URL
     * matching rationale
     * target segment
     * intended routine

6. **Segment before send**

   * never assume the same research/video bundle is suitable for all clients

7. **Educational tone for low-confidence clients**

   * when the client is novice, disengaged, or young, prefer explanation and habit-building over technical density

8. **PB remains accountable**

   * the system prepares, ranks, drafts, and recommends
   * PB decides how to use the output

---

# Antigravity-Specific Mission

Use Antigravity to create:

* Rules
* Skills
* Workflows
* Resources
* Prompt templates
* Evaluation criteria
* Failure / fallback behavior
* Artifacts for human review

Design this as a **multi-agent, reviewable operating workflow** with clear artifacts at each step.

---

# Business Operating Model: Hybrid Content Routines

You must explicitly support the following **text + video hybrid asset-management routines**.

## Routine A — Daily / Morning Market Temperature

### Timing

* weekday morning
* target send window: 08:10–08:30

### Content Pairing

* report: **Market View** or equivalent daily market summary
* video: **Wall Street Finder** and/or daily live market video

### Goal

Help clients orient quickly during the morning information flood.

### Delivery Pattern

* short PB message with video link
* 3-line text summary for clients unable or unwilling to watch video
* emphasis on overnight U.S. market issues, key macro drivers, and near-term watchpoints

### Best-Fit Segments

* S1: low assets / low frequency → simplified morning summary
* S2: low assets / high frequency → faster tactical angle + risk framing
* S3/S4: optional PB call-list trigger if overnight moves materially affect portfolio exposures

### System Task

Given a daily report and relevant market video, produce:

* 3-line text summary
* video-first message draft
* who should receive video-first vs text-first
* PB list of clients materially exposed to relevant market moves

---

## Routine B — Biweekly / Deep Portfolio Skeleton

### Timing

* every other Thursday afternoon

### Content Pairing

* report: **Mirae Asset Minutes** or equivalent earnings / sector-change note
* video: **RE포트** or **Analyst Report**

### Goal

Move beyond surface market commentary and help clients understand actual changes in the earnings/sector picture.

### Delivery Pattern

* send a framing question such as:

  * “Which sectors are showing meaningful earnings revisions this cycle?”
* attach or reference the Minutes-style research summary
* add the relevant analyst video with timestamps or topic highlights
* connect the report to owned names or likely portfolio exposures

### Best-Fit Segments

* S2: active self-directed clients
* S3: affluent but lower-frequency clients with concentrated sector exposure
* S4: high-asset active clients requiring PB review before outreach

### System Task

Given a sector/company research note and related analyst video, produce:

* research thesis summary
* portfolio relevance explanation
* owned-name exposure mapping
* consultation talking points
* PB follow-up urgency score

---

## Routine C — Weekly / Theme Discovery for Weekend

### Timing

* Friday afternoon to Saturday morning

### Content Pairing

* report: **Week Ahead Snapshot**, **Visible China / China macro**, or equivalent thematic outlook
* video: **ETF&**, **Space&**, global theme video, AI / India / space / structural trend content

### Goal

Use weekend attention more effectively by framing investing as insight acquisition, not homework.

### Delivery Pattern

* “What could become next week’s inflection point?”
* pair a lighter but strategic video with a theme report
* encourage reflective, medium-horizon thinking rather than immediate trading

### Best-Fit Segments

* S1: light educational version
* S2: thematic opportunity/risk framing
* S3: allocation-aware thematic relevance
* S4: PB-curated theme note only if materially actionable

### System Task

Given a theme report and related theme video, produce:

* weekend theme bundle
* likely interested segments
* portfolio fit notes
* suggested CTA: watch / read / discuss / schedule review

---

## Routine D — Occasional / Educational Confidence Building

### Timing

* monthly, holidays, or soft-engagement periods

### Content Pairing

* video: educational original or narrative content such as finance web-drama / beginner series
* document: pension, IRP, long-term investing explainer, product education sheet

### Goal

Support novice and younger clients who feel intimidated by investing.

### Delivery Pattern

* emotionally accessible introduction
* narrative-first delivery
* lightweight supporting product education
* no hard-sell tone

### Best-Fit Segments

* Gen Z / novice / low-confidence / dormant clients
* pension prospects
* long-horizon investors with low current engagement

### System Task

Given educational video content and a pension or long-term investment explainer, produce:

* educational outreach draft
* beginner-safe summary
* suitable next conversation angle
* non-intimidating CTA

---

# Customer Segmentation Model

Implement a simple rule-based segmentation baseline.

## Base Segments

* **S1**: low assets, low trading frequency
* **S2**: low assets, high trading frequency
* **S3**: high assets, low trading frequency
* **S4**: high assets, high trading frequency

## Additional Modifiers

* novice / low-confidence
* retired / pension-oriented
* ETF-heavy
* single-stock-heavy
* concentrated sector exposure
* high cash balance
* loss-sensitive behavior
* dormant engagement
* digital-first media preference
* video-preferred learning style

You must allow content selection to be driven by both:

1. financial/portfolio relevance
2. content-consumption preference

---

# Resource Model

Define resources for the Antigravity system.

## Resource 1 — ResearchReport

Fields:

* report_id
* title
* date
* author
* report_type
* source_url
* attachment_urls
* normalized_text
* tags
* asset_class_tags
* region_tags
* sector_tags
* company_tags
* time_horizon
* risk_conditions

## Resource 2 — SmartMoneyVideo

Fields:

* video_id
* title
* publish_date
* source_url
* series_name
* duration
* description
* transcript_or_summary
* tags
* asset_class_tags
* region_tags
* sector_tags
* company_tags
* education_level
* content_style
* recommended_routine

## Resource 3 — HybridContentBundle

Fields:

* bundle_id
* routine_type
* report_id
* video_id
* match_reason
* target_segments
* pb_summary
* client_summary
* recommended_cta
* urgency
* confidence
* compliance_notes

## Resource 4 — CustomerProfile

Fields:

* customer_id
* asset_tier
* trading_frequency
* risk_profile
* portfolio_style
* account_types
* sector_exposures
* geographic_exposures
* cash_ratio
* concentration_flags
* engagement_level
* media_preference
* segment_id
* modifiers

## Resource 5 — PBActionDraft

Fields:

* action_id
* customer_id
* bundle_id
* routine_type
* outreach_channel
* pb_talking_points
* client_message_draft
* follow_up_priority
* traceability
* review_required

## Resource 6 — AuditRecord

Fields:

* audit_id
* timestamp
* report_id
* video_id
* customer_id
* workflow_name
* decision_points
* generated_outputs
* rationale
* human_review_status

---

# Required Skills / Agents

## Skill 1 — Research Discovery Skill

Purpose:

* discover candidate research reports from Mirae research sources

Inputs:

* date window
* report type
* tags / keywords

Outputs:

* structured ResearchReport metadata candidates

Requirements:

* bounded discovery only
* safe failure on source variability
* create artifacts of discovered items

---

## Skill 2 — Video Discovery Skill

Purpose:

* discover candidate SmartMoney videos relevant to a research topic or routine

Inputs:

* topic tags
* series name
* date window
* routine type

Outputs:

* SmartMoneyVideo candidates with topic tags and series classification

Requirements:

* classify into likely series:

  * daily market
  * analyst/report
  * theme/weekend
  * educational/confidence-building

---

## Skill 3 — Report Reading Skill

Purpose:

* read report page and PDF attachment when available
* normalize text
* extract thesis candidates

Outputs:

* normalized research text
* metadata enrichment
* source confidence flags

---

## Skill 4 — Video Understanding Skill

Purpose:

* read video metadata and transcript/summary if available
* classify tone, topic depth, and routine fit

Outputs:

* transcript summary
* topic tags
* content style:

  * urgent market
  * analytical
  * thematic
  * educational
  * narrative / emotional
* education level:

  * beginner
  * intermediate
  * advanced

---

## Skill 5 — Structured Signal Extraction Skill

Purpose:
Transform report and optionally matched video into a structured investment signal.

Output schema:

* thesis
* report_type
* asset_class_impact
* region_impact
* sector_impact
* company_impact
* time_horizon
* risk_conditions
* confidence_level
* educational_complexity
* recommended_routines

Rule:
If the report is analytically important but the video is beginner-friendly, keep both truths:

* analytical relevance
* communication simplicity

---

## Skill 6 — Cross-Modal Matching Skill

Purpose:
Match research reports with SmartMoney videos.

Matching dimensions:

* asset class
* region
* sector
* company
* theme
* time horizon
* communication purpose
* client comprehension need

Outputs:

* match score
* match reasons
* preferred routine type
* fallback if no valid video exists

---

## Skill 7 — Segment Applicability Skill

Purpose:
Given a structured signal + customer segment, determine whether this bundle is:

* relevant
* understandable
* action-worthy
* educational only

Outputs:

* segment relevance score
* communication style recommendation
* send/no-send suggestion
* PB-review requirement
* best CTA

CTA examples:

* watch first
* read first
* skim summary only
* discuss with PB
* schedule review
* educational nurture only

---

## Skill 8 — PB Copilot Draft Skill

Purpose:
Generate PB-facing outputs.

Outputs:

* PB summary
* consultation prep note
* call script draft
* chat message draft
* why-this-client note
* risk disclosure reminders
* suggested next step

Tone:

* concise
* practical
* segment-aware
* never overstate certainty

---

## Skill 9 — Priority Queue Skill

Purpose:
Create a PB follow-up ranking using mock or connected customer data.

Scoring dimensions:

* portfolio exposure relevance
* high cash opportunity
* concentration risk
* large mismatch vs current house-view
* recent trading behavior
* low engagement but high relevance
* educational fit for dormant or novice clients

Outputs:

* ranked customer list
* reason codes
* suggested outreach routine
* suggested channel

---

## Skill 10 — Audit and Explainability Skill

Purpose:
Record why a research + video bundle was generated and who it was considered for.

Outputs:

* audit record
* traceability links
* explanation summary
* flagged assumptions

---

# Workflow Design

## Workflow 1 — Daily Morning Hybrid Routine

Steps:

1. discover daily market reports
2. discover daily / market-oriented SmartMoney videos
3. parse report
4. summarize video
5. extract structured signal
6. match report + video
7. identify affected customers
8. produce:

   * 3-line summary
   * video-first PB message draft
   * text-first fallback draft
   * PB call-list
9. write audit artifact

Artifacts required:

* top morning bundle list
* one sample PB message
* one text-only fallback
* ranked affected customers

---

## Workflow 2 — Biweekly Deep Portfolio Routine

Steps:

1. discover Minutes-style / sector / earnings reports
2. discover analyst/report videos
3. parse and tag both
4. match report + video
5. identify customers with direct sector/company relevance
6. produce:

   * deep portfolio relevance note
   * owned-position mapping
   * consultation script
   * PB urgency ranking
7. write audit artifact

Artifacts required:

* one matched bundle
* one relevance matrix
* one consultation script
* one priority ranking

---

## Workflow 3 — Weekend Theme Routine

Steps:

1. discover week-ahead or theme reports
2. discover thematic SmartMoney videos
3. extract structural theme signal
4. choose appropriate segments
5. generate weekend hybrid bundle
6. label CTA and channel
7. write audit artifact

Artifacts required:

* theme bundle card
* segment map
* CTA rationale
* weekend outreach draft

---

## Workflow 4 — Educational Nurture Routine

Steps:

1. discover educational video content
2. discover related pension / IRP / long-term investment materials
3. classify target beginner segments
4. generate soft-touch draft
5. suppress hard-sell language
6. write audit artifact

Artifacts required:

* beginner-safe summary
* nurture draft
* follow-up recommendation
* do-not-push guardrail check

---

# Rules for Communication Logic

## Video-First Rule

Use video-first delivery when:

* the client is novice or low-confidence
* the topic is easier to absorb visually
* the emotional hurdle is high
* the report is too dense for first contact

## Text-First Rule

Use text-first delivery when:

* the client is time-constrained
* the client prefers concise summaries
* the topic is urgent and tactical
* the client is already sophisticated

## Hybrid Rule

Use both when:

* the topic is important
* the report is decision-relevant
* the video can improve clarity
* the client has enough engagement likelihood

## PB-Only Rule

Do not directly suggest outreach drafts for automated client send when:

* the topic has high sensitivity
* the portfolio implication is large
* the customer is high-asset/high-complexity
* regulatory or suitability ambiguity is present

---

# Evaluation Rubric

Evaluate each workflow on the following dimensions.

## 1. Relevance

* did the report/video bundle actually match the same topic?

## 2. Comprehension Fit

* is the content format suitable for the target segment?

## 3. Portfolio Fit

* does the bundle connect to actual exposures or client needs?

## 4. PB Usefulness

* would a PB actually use this output in the same day or week?

## 5. Explainability

* can every recommendation be traced back to source content?

## 6. Safety

* did the system avoid direct advice / execution language?

## 7. Engagement Quality

* does the bundle improve the chance of client consumption?

Rate each output:

* pass
* revise
* reject

---

# Failure and Fallback Logic

## If no video match exists

* still produce a text-only PB summary
* mark `video_match_missing = true`
* recommend whether PB should wait, proceed text-only, or skip

## If report parsing fails

* use metadata-only fallback
* do not hallucinate thesis
* mark low confidence

## If transcript is unavailable

* rely on title/description/series classification only
* lower confidence
* avoid over-specific talking points

## If customer relevance is weak

* classify bundle as educational or skip
* do not force outreach

## If the topic is complex and the client is novice

* downgrade from action-oriented to education-oriented routine

---

# Deliverables

You must produce:

1. Antigravity Rule Set
2. Skill definitions
3. Workflow graph for all 4 routines
4. resource schemas
5. prompt templates for each skill
6. evaluation rubric
7. fallback logic
8. example artifacts for one report-video bundle in each routine
9. handoff notes for backend implementation
10. explicit list of assumptions and unresolved dependencies

---

# Output Style

Be implementation-oriented and concrete.

Do not stop at generic concepts.
Design:

* the actual workflow objects
* inputs and outputs
* validation rules
* artifacts
* evaluation steps
* human review points

Start by defining:

1. the global Rules,
2. the resource schemas,
3. the four workflow graphs,
4. the skill prompt templates,
   in that order.