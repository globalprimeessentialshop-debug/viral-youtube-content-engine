"""
Main Entry Point - Run Master Brain Agent
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.master_brain_agent import MasterBrainAgent


async def main():
    """
    Main execution function
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                  🧠 MASTER BRAIN AGENT - OpenJarvis                        ║
    ║              Autonomous YouTube Content Creation System                    ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize Master Brain
    master_brain = MasterBrainAgent()
    
    # Run autonomous cycle
    try:
        results = await master_brain.run_autonomous_cycle()
        print("\n✅ Autonomous cycle completed successfully!")
        return results
    except KeyboardInterrupt:
        print("\n⏹️  Master Brain interrupted by user")
        master_brain.save_session()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
