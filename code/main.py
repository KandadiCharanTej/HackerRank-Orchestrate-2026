"""
main.py — Entry point for HackerRank Orchestrate.
Enables command line execution of the prediction pipeline.
"""

import sys
from pathlib import Path

# Add project root to sys.path to allow importing run.py
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from run import process_claims

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HackerRank Orchestrate Entry Point")
    parser.add_argument("--input", default=None, help="Path to input claims CSV (defaults to dataset/claims.csv)")
    parser.add_argument("--output", default=None, help="Path to output predictions CSV (defaults to output.csv)")
    parser.add_argument("--history", default=None, help="Path to user history CSV")
    parser.add_argument("--requirements", default=None, help="Path to evidence requirements CSV")
    args = parser.parse_args()
    process_claims(
        input_path=args.input,
        output_path=args.output,
        history_path=args.history,
        req_path=args.requirements
    )
