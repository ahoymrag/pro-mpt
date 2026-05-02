#!/usr/bin/env python3
"""
Unified ingestion script for pro-mpt
Runs all registered connectors to pull in new data.
"""

from pro_mpt.connectors.claude import ClaudeConnector
from pro_mpt.connectors.gemini import GeminiConnector

def main():
    connectors = [
        ClaudeConnector(),
        GeminiConnector(),
    ]
    
    total_new = 0
    print("🚀 Running pro-mpt ingestion...\n")
    
    for connector in connectors:
        count = connector.scan_and_import()
        if count:
            total_new += count
            
    if total_new == 0:
        print("\n✨ All sources up to date.")
    else:
        print(f"\n✨ Successfully imported {total_new} new items to pro-mpt.")

if __name__ == "__main__":
    main()
