"""
Real-time Monitoring Dashboard for Master Brain Agents
Provides web interface to see agent work in progress
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import threading
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global state
DASHBOARD_STATE = {
    "agents": {},
    "current_project": None,
    "logs": [],
    "metrics": {},
    "evolution_data": {},
    "last_update": datetime.now().isoformat()
}


class DashboardMonitor:
    """
    Monitors Master Brain and agents in real-time
    Updates dashboard state continuously
    """

    def __init__(self):
        self.monitoring = False
        self.update_interval = 2  # seconds

    def start_monitoring(self):
        """Start monitoring thread"""
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("📡 Dashboard monitoring started")

    def stop_monitoring(self):
        """Stop monitoring thread"""
        self.monitoring = False
        logger.info("📡 Dashboard monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Update agent status
                self._update_agent_status()
                # Update metrics
                self._update_metrics()
                # Update logs
                self._update_logs()
                
                DASHBOARD_STATE["last_update"] = datetime.now().isoformat()
                
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
            
            threading.Event().wait(self.update_interval)

    def _update_agent_status(self):
        """Update status of all agents"""
        # This would pull from master_brain.get_agent_status()
        pass

    def _update_metrics(self):
        """Update performance metrics"""
        pass

    def _update_logs(self):
        """Update log entries"""
        pass


monitor = DashboardMonitor()


# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify(DASHBOARD_STATE)


@app.route('/api/agents')
def get_agents():
    """Get all agent statuses"""
    return jsonify(DASHBOARD_STATE["agents"])


@app.route('/api/agent/<agent_name>')
def get_agent(agent_name):
    """Get specific agent status"""
    agent = DASHBOARD_STATE["agents"].get(agent_name)
    if agent:
        return jsonify(agent)
    return jsonify({"error": "Agent not found"}), 404


@app.route('/api/project')
def get_project():
    """Get current project details"""
    return jsonify(DASHBOARD_STATE["current_project"])


@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    limit = request.args.get('limit', 100, type=int)
    return jsonify(DASHBOARD_STATE["logs"][-limit:])


@app.route('/api/metrics')
def get_metrics():
    """Get system metrics"""
    return jsonify(DASHBOARD_STATE["metrics"])


@app.route('/api/evolution')
def get_evolution():
    """Get evolution progress"""
    return jsonify(DASHBOARD_STATE["evolution_data"])


@app.route('/api/approval/pending')
def check_pending_approval():
    """Check if approval is pending"""
    return jsonify({
        "pending": DASHBOARD_STATE["current_project"] is not None,
        "project": DASHBOARD_STATE["current_project"]
    })


@app.route('/api/approval/approve', methods=['POST'])
def approve_project():
    """Approve current project"""
    DASHBOARD_STATE["approval_status"] = "approved"
    return jsonify({"status": "approved", "message": "Project approved!"})


@app.route('/api/approval/reject', methods=['POST'])
def reject_project():
    """Reject current project"""
    feedback = request.json.get('feedback', '')
    DASHBOARD_STATE["approval_status"] = "rejected"
    DASHBOARD_STATE["rejection_feedback"] = feedback
    return jsonify({"status": "rejected", "message": "Project rejected"})


@app.route('/api/stream/logs')
def stream_logs():
    """Stream logs in real-time (SSE)"""
    def generate():
        while True:
            yield f"data: {json.dumps(DASHBOARD_STATE)}\n\n"
            threading.Event().wait(2)
    
    return generate(), 200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    }


if __name__ == '__main__':
    monitor.start_monitoring()
    app.run(host='0.0.0.0', port=8000, debug=False)
