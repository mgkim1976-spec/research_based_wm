import os
import sys
# Add project root to path for local execution testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from app.core.workflows.routines import WorkflowOrchestrator
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Note: In a real environment, you'd cache the orchestrator results 
# or run them in a background job (like Celery / PythonAnywhere Always-on task). 
# For Stage 1 testing, we initialize it globally.
orchestrator = WorkflowOrchestrator()

# In-memory mock storage for the daily run
latest_run_cache = None

@app.route("/", methods=["GET"])
def dashboard():
    """PB Dashboard Main page - Today's Hybrid Routines & Customer Queues."""
    global latest_run_cache
    if not latest_run_cache:
        # Run Routine A (Morning Hybrid) forcefully if empty for demo
        latest_run_cache = orchestrator.run_routine_a_morning()
        
    # Also load all historical reports for the bottom list
    all_reports = orchestrator.crawler.load_all_reports()
    
    return render_template("index.html", data=latest_run_cache, all_reports=all_reports)

@app.route("/run_routine", methods=["POST"])
def run_routine_api():
    """Endpoint to trigger a routine explicitly."""
    global latest_run_cache
    if request.is_json:
        routine_type = request.json.get("routine_type", "A")
    else:
        routine_type = request.form.get("routine_type", "A")
        
    if routine_type == "A":
        report_id = request.json.get("report_id") if request.is_json else request.form.get("report_id")
        latest_run_cache = orchestrator.run_routine_a_morning(target_report_id=report_id)
        
    if not request.is_json:
        from flask import redirect, url_for
        return redirect(url_for('dashboard'))
        
    return jsonify({"status": "success", "message": f"Routine {routine_type} executed."})

@app.route("/guide", methods=["GET"])
def workflow_guide():
    """Workflow Guide explaining business routines to PBs."""
    return render_template("guide.html")

import time
import threading

def background_refresh():
    """Periodic background refresh every 1 hour."""
    while True:
        try:
            logger.info("Starting background research refresh...")
            orchestrator.crawler.fetch_recent_reports()
            logger.info("Background refresh completed.")
        except Exception as e:
            logger.error(f"Error in background refresh: {e}")
        time.sleep(3600) # 1 hour

# Start background thread
refresh_thread = threading.Thread(target=background_refresh, daemon=True)
refresh_thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=8080)
