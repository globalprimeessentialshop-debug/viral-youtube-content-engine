"""
Command-line Interface for OpenJarvis Master Brain
Provides CLI access to all system functions
"""

import asyncio
import click
import json
from datetime import datetime
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from jarvis_integration import JarvisIntegration


class ClickState:
    """Maintain state across CLI commands"""
    def __init__(self):
        self.jarvis = None
        self.initialized = False


click_state = ClickState()


@click.group()
async def cli():
    """OpenJarvis Master Brain CLI"""
    pass


@cli.command()
@click.pass_context
async def start(ctx):
    """
    Start the interactive Jarvis session
    """
    click.echo("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║              🤖 OpenJarvis + Master Brain 🧠                         ║
    ║                                                                       ║
    ║        Type 'help' for available commands                           ║
    ║        Type 'exit' to quit                                          ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    jarvis = JarvisIntegration()
    
    if await jarvis.initialize():
        click.echo("✅ Master Brain initialized successfully\n")
        await jarvis.run_interactive_session()
    else:
        click.echo("❌ Failed to initialize Master Brain")


@cli.command()
@click.option('--category', prompt='Video category', help='Category to analyze')
@click.option('--audience', prompt='Target audience', help='Target audience description')
async def analyze(category: str, audience: str):
    """
    Analyze top 5 YouTube videos
    """
    jarvis = JarvisIntegration()
    
    if not await jarvis.initialize():
        click.echo("❌ Failed to initialize")
        return
    
    click.echo(f"🔍 Analyzing top 5 videos in '{category}'...\n")
    
    result = await jarvis.start_analysis()
    click.echo(json.dumps(result, indent=2))


@cli.command()
@click.option('--theme', prompt='Content theme', help='Video theme/idea')
@click.option('--subs', prompt='Target subscribers', help='Target subscriber count')
@click.option('--length', prompt='Video length', default='10', help='Video length in minutes')
async def plan(theme: str, subs: str, length: str):
    """
    Create a new video project plan
    """
    jarvis = JarvisIntegration()
    
    if not await jarvis.initialize():
        click.echo("❌ Failed to initialize")
        return
    
    click.echo(f"📋 Creating project plan for '{theme}'...\n")
    
    result = await jarvis.start_planning()
    click.echo(json.dumps(result, indent=2))


@cli.command()
async def execute():
    """
    Execute the agent pipeline
    """
    jarvis = JarvisIntegration()
    
    if not await jarvis.initialize():
        click.echo("❌ Failed to initialize")
        return
    
    click.echo("🎬 Executing agent pipeline...\n")
    
    result = await jarvis.execute_pipeline()
    click.echo(json.dumps(result, indent=2))


@cli.command()
async def status():
    """
    Show real-time agent status
    """
    jarvis = JarvisIntegration()
    
    if not await jarvis.initialize():
        click.echo("❌ Failed to initialize")
        return
    
    result = await jarvis.show_status()
    click.echo(json.dumps(result, indent=2))


@cli.command()
async def evolution():
    """
    Show Master Brain evolution progress
    """
    jarvis = JarvisIntegration()
    
    if not await jarvis.initialize():
        click.echo("❌ Failed to initialize")
        return
    
    result = await jarvis.show_evolution()
    click.echo(json.dumps(result, indent=2))


@cli.command()
def dashboard():
    """
    Open the web dashboard
    """
    click.echo("🌐 Opening dashboard at http://localhost:8000...")
    import webbrowser
    webbrowser.open('http://localhost:8000')


@cli.command()
def help_command():
    """
    Show help and available commands
    """
    click.echo("""
    Available Commands:
    ═══════════════════════════════════════════════════════════════
    
    start            - Start interactive Jarvis session
    analyze          - Analyze top 5 YouTube videos
    plan             - Create a new video project plan
    execute          - Execute the agent pipeline
    status           - Show real-time agent status
    evolution        - Show Master Brain evolution progress
    dashboard        - Open web dashboard
    help             - Show this help message
    
    Example Usage:
    ═══════════════════════════════════════════════════════════════
    
    # Start interactive mode
    python jarvis_cli.py start
    
    # Analyze videos
    python jarvis_cli.py analyze --category technology --audience "tech enthusiasts"
    
    # Create project plan
    python jarvis_cli.py plan --theme "AI Tutorials" --subs 100000 --length 10
    
    # Execute pipeline
    python jarvis_cli.py execute
    
    # Check status
    python jarvis_cli.py status
    
    # View evolution progress
    python jarvis_cli.py evolution
    
    # Open dashboard
    python jarvis_cli.py dashboard
    """)


if __name__ == '__main__':
    cli()
