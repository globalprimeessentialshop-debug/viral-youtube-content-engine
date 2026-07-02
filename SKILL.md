---
name: jarvis-youtube-automation
displayName: Jarvis YouTube Content Automation System
description: "Complete autonomous AI system for viral YouTube video creation with 5 specialized agents working collaboratively"
category: "content-creation"
version: "1.0.0"
author: "OpenJarvis Master Brain"
license: "MIT"
tags:
  - youtube
  - content-creation
  - video-production
  - ai-agents
  - viral-content
  - automation
  - multi-agent
  - autonomous

requiredAPIKeys:
  - ANTHROPIC_API_KEY
  - OPENAI_API_KEY
  - YOUTUBE_API_KEY

supportedActions:
  - analyze
  - plan
  - execute
  - approve
  - evolve
  - monitor

inputSchema:
  type: object
  properties:
    command:
      type: string
      enum: ["analyze", "plan", "execute", "status", "evolution"]
      description: "Master Brain command to execute"
    category:
      type: string
      description: "Video category for analysis (e.g., technology, gaming, education)"
    audience:
      type: string
      description: "Target audience description"
    theme:
      type: string
      description: "Content theme or idea"
    target_subscribers:
      type: integer
      description: "Target subscriber count"
    video_length:
      type: integer
      description: "Video length in minutes"
  required: ["command"]

outputSchema:
  type: object
  properties:
    status:
      type: string
      enum: ["success", "pending_approval", "error", "cancelled"]
    action:
      type: string
      description: "Action performed"
    data:
      type: object
      description: "Result data"
    approval_required:
      type: boolean
      description: "Whether user approval is needed"
    next_action:
      type: string
      description: "Next step in workflow"

externalLinks:
  - title: "GitHub Repository"
    url: "https://github.com/globalprimeessentialshop-debug/viral-youtube-content-engine"
  - title: "Integration Guide"
    url: "https://github.com/globalprimeessentialshop-debug/viral-youtube-content-engine/blob/main/JARVIS_INTEGRATION_GUIDE.md"
  - title: "Agents Documentation"
    url: "https://github.com/globalprimeessentialshop-debug/viral-youtube-content-engine/blob/main/AGENTS_GUIDE.md"

customPrompts:
  - trigger: "Jarvis"
    response: "Master Brain Agent activated! What would you like to do?"
  - trigger: "Open Jarvis"
    response: "Opening Master Brain system. Ready to create viral content!"
  - trigger: "analyze videos"
    response: "Starting video analysis mode. What category should I analyze?"
  - trigger: "create project"
    response: "Creating new project. Tell me about your video concept."
  - trigger: "execute"
    response: "Executing agent pipeline. This will create your entire video project."

monitoringDashboard:
  enabled: true
  url: "http://localhost:8000"
  features:
    - agent_status_panel
    - real_time_logs
    - viral_score_graphs
    - agent_performance_metrics
    - approval_notifications
    - evolution_progress
    - memory_summary
    - conversation_history

approvalWorkflow:
  checkpoints:
    - stage: 1
      name: "Plan Approval"
      description: "Review project plan before agents start"
      requires_approval: true
    - stage: 2
      name: "Final Approval"
      description: "Review all content before posting"
      requires_approval: true

agents:
  - id: 1
    name: "Master Brain (Brain)"
    description: "Orchestrates all agents, analyzes trends, makes decisions"
    role: "coordinator"
  - id: 2
    name: "Script Agent"
    description: "Writes viral scripts with hooks and retention patterns"
    role: "content_writer"
  - id: 3
    name: "Video Content Agent"
    description: "Creates video production specifications"
    role: "video_producer"
  - id: 4
    name: "Social Media Agent"
    description: "Creates thumbnails, titles, and social assets"
    role: "social_manager"
  - id: 5
    name: "YouTube Distributor Agent"
    description: "Plans distribution and growth strategies"
    role: "distributor"
---

# Jarvis YouTube Automation System

## Overview

Complete autonomous AI system for creating viral YouTube videos with 5 specialized agents working collaboratively.

## Quick Start

```bash
# Interactive mode
python jarvis_integration.py

# Web dashboard
python dashboard.py

# CLI mode
python jarvis_cli.py start
```

## How It Works

### Voice Activation

Just say or type: **"Jarvis"** or **"Open Jarvis"**

The system will:
1. Activate the Master Brain Agent
2. Show you available actions
3. Guide you through the process
4. **Ask for approval** before taking action
5. Execute agents step-by-step
6. Show real-time progress on the dashboard

### Two Approval Checkpoints

**Checkpoint 1: Plan Approval**
- Master Brain analyzes videos
- Creates project plan
- **PAUSES** - Waiting for your approval
- You review and approve/reject

**Checkpoint 2: Final Approval**
- All agents complete their work
- Master Brain assembles final package
- **PAUSES** - Waiting for your final approval
- You review and approve/reject

### Agent Pipeline

```
Agent 2: Script Agent
└─ Creates viral hooks
└─ Writes main content
└─ Adds retention patterns

Agent 3: Video Content Agent
└─ Generates shot lists
└─ Specifies B-roll
└─ Creates graphics specs

Agent 4: Social Media Agent
└─ Designs thumbnails
└─ Creates title variations
└─ Optimizes descriptions

Agent 5: YouTube Distributor Agent
└─ Plans premiere strategy
└─ Creates promotion plan
└─ Projects growth metrics
```

## Real-Time Monitoring

Open **http://localhost:8000** to watch:
- Agent execution in real-time
- Viral score calculation
- Metrics updates
- Evolution progress
- Approval prompts

## 24/7 Evolution

Master Brain continuously learns:
- Improves decision-making
- Better viral score predictions
- Optimized strategies
- Enhanced content quality

## Files

- `jarvis_config.py` - System configuration
- `jarvis_integration.py` - Main integration module
- `jarvis_cli.py` - Command-line interface
- `dashboard.py` - Web monitoring dashboard
- `templates/dashboard.html` - Dashboard UI
- `JARVIS_INTEGRATION_GUIDE.md` - Complete guide
- `AGENTS_GUIDE.md` - Agent documentation

## Support

For issues:
1. Check `JARVIS_INTEGRATION_GUIDE.md`
2. Review `AGENTS_GUIDE.md`
3. Check `jarvis_config.py` for settings
