# OpenJarvis Integration Configuration
# This file enables OpenJarvis to load and use the Master Brain Skill

JARVIS_CONFIG = {
    "system_name": "OpenJarvis YouTube Content Engine",
    "version": "1.0.0",
    "enabled_skills": [
        "viral-youtube-master-brain"
    ],
    "skills": {
        "viral-youtube-master-brain": {
            "name": "viral-youtube-master-brain",
            "displayName": "Master Brain Agent System",
            "description": "Autonomous AI system for viral YouTube video creation with 5 specialized agents",
            "enabled": True,
            "module_path": "python/agents/master_brain_agent.py",
            "class_name": "MasterBrainAgent",
            "api_keys": [
                "ANTHROPIC_API_KEY",
                "OPENAI_API_KEY",
                "YOUTUBE_API_KEY"
            ],
            "supported_actions": [
                "analyze",
                "plan",
                "execute",
                "approve",
                "evolve",
                "monitor"
            ],
            "agents": {
                "script_agent": "python/agents/script_agent.py",
                "video_content_agent": "python/agents/video_content_agent.py",
                "social_media_agent": "python/agents/social_media_agent.py",
                "youtube_distributor_agent": "python/agents/youtube_distributor_agent.py"
            },
            "approval_required_at": [
                "plan_creation",
                "final_posting"
            ],
            "monitoring": {
                "enabled": True,
                "dashboard": "http://localhost:8000",
                "log_file": "logs/jarvis_master_brain.log"
            }
        }
    },
    "jarvis_commands": {
        "start_master_brain": "Open the Master Brain Agent system",
        "analyze_videos": "Analyze top 5 YouTube videos in a category",
        "create_project": "Create a new video project plan",
        "execute_pipeline": "Execute all agents in the pipeline",
        "show_status": "Show real-time status of all agents",
        "view_dashboard": "Open the monitoring dashboard",
        "evolution_report": "Show Master Brain evolution progress",
        "approve_plan": "Approve the current project plan",
        "reject_plan": "Reject and provide feedback",
        "approve_posting": "Approve video for final posting",
        "cancel_project": "Cancel current project"
    },
    "conversation_triggers": {
        "master_brain": ["open jarvis", "start jarvis", "hello jarvis", "jarvis", "master brain"],
        "analyze": ["analyze videos", "research", "find top videos", "what's trending"],
        "create": ["create video", "new project", "make video", "start new"],
        "monitor": ["show status", "how's it going", "what's happening", "status"],
        "approve": ["yes", "approve", "looks good", "go ahead", "yes approve"],
        "reject": ["no", "reject", "no approve", "needs changes", "not ready"]
    },
    "real_time_monitoring": {
        "enabled": True,
        "update_interval_seconds": 5,
        "track_agents": [
            "script_agent",
            "video_content_agent",
            "social_media_agent",
            "youtube_distributor_agent",
            "master_brain_agent"
        ],
        "metrics_to_track": [
            "agent_status",
            "task_progress",
            "errors",
            "viral_scores",
            "execution_time"
        ]
    },
    "approval_workflow": {
        "step_1_analysis": {
            "name": "Video Analysis",
            "description": "Master Brain analyzes top 5 videos",
            "requires_approval": False
        },
        "step_2_planning": {
            "name": "Project Planning",
            "description": "Create comprehensive project plan",
            "requires_approval": True,
            "approval_prompt": "Do you approve this project plan?"
        },
        "step_3_execution": {
            "name": "Agent Pipeline Execution",
            "description": "Execute all agents to create content",
            "requires_approval": False,
            "depends_on": "step_2_planning"
        },
        "step_4_review": {
            "name": "Final Review",
            "description": "Review all generated content",
            "requires_approval": True,
            "approval_prompt": "Approve this content for posting?"
        },
        "step_5_evolution": {
            "name": "System Evolution",
            "description": "Master Brain learns and improves",
            "requires_approval": False
        }
    },
    "dashboard_features": {
        "agent_status_panel": True,
        "real_time_logs": True,
        "viral_score_graphs": True,
        "agent_performance_metrics": True,
        "approval_notifications": True,
        "evolution_progress": True,
        "memory_summary": True,
        "conversation_history": True
    }
}
