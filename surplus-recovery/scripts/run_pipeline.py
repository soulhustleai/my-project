"""
Manual Pipeline Runner

Runs the full pipeline: monitor → ingest → normalize → score → enrich → outreach

Usage:
  python scripts/run_pipeline.py              # Full pipeline
  python scripts/run_pipeline.py --step score # Single step
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from packages.utils.logger import get_logger

logger = get_logger("pipeline")

STEPS = {
    "monitor": "Check sources and download new data",
    "ingest": "Parse downloaded files into records",
    "normalize": "Deduplicate and normalize records",
    "score": "Score opportunities",
    "enrich": "Enrich claimant contact info",
    "outreach-new": "Start outreach for new contactable leads",
    "outreach-scheduled": "Process scheduled follow-ups",
}


async def run_monitor():
    from services.source_monitor.monitor import run
    await run()


def run_ingest():
    from services.record_ingestion.ingest import ingest_pending
    ingest_pending()


def run_normalize():
    from services.normalization.normalize import normalize_pending
    normalize_pending()


def run_score():
    from services.opportunity_engine.score import score_pending
    score_pending()


def run_enrich():
    from services.claimant_enrichment.enrich import enrich_pending
    enrich_pending()


def run_outreach_new():
    from services.outreach_engine.outreach import start_new_outreach
    start_new_outreach()


def run_outreach_scheduled():
    from services.outreach_engine.outreach import process_scheduled
    process_scheduled()


def main():
    parser = argparse.ArgumentParser(description="Run surplus recovery pipeline")
    parser.add_argument("--step", choices=STEPS.keys(), help="Run a specific step")
    parser.add_argument("--list", action="store_true", help="List available steps")
    args = parser.parse_args()

    if args.list:
        print("Available pipeline steps:")
        for name, desc in STEPS.items():
            print(f"  {name:20s} — {desc}")
        return

    if args.step:
        steps = [args.step]
    else:
        steps = list(STEPS.keys())

    for step in steps:
        logger.info(f"Running step: {step}")
        try:
            if step == "monitor":
                asyncio.run(run_monitor())
            elif step == "ingest":
                run_ingest()
            elif step == "normalize":
                run_normalize()
            elif step == "score":
                run_score()
            elif step == "enrich":
                run_enrich()
            elif step == "outreach-new":
                run_outreach_new()
            elif step == "outreach-scheduled":
                run_outreach_scheduled()

            logger.info(f"Step complete: {step}")
        except Exception as e:
            logger.error(f"Step failed: {step} — {e}")
            if args.step:
                sys.exit(1)
            # Continue with next step if running full pipeline


if __name__ == "__main__":
    main()
