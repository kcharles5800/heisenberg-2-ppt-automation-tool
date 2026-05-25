import os
import sys
import time
import traceback

# Ensure the script can locate your existing backend modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from scraper import get_scraped_lyrics
    from ppt_engine import generate_ppt
except ImportError as e:
    print(f"\n[ERROR] Failed to import core modules: {e}")
    print("Make sure you are running this script from the project root directory.")
    sys.exit(1)

def run_developer_cli():
    print("=" * 60)
    print("          HEISENBERG 2.0 -- DEVELOPER DEBUG TERMINAL          ")
    print("=" * 60)
    
    # 1. Capture user input natively
    song_name = input("\nEnter target song name to automate: ").strip()
    
    if not song_name:
        print("\n[ABORTED] Song name cannot be blank.")
        return

    print("\n" + "-" * 40)
    print("[i] DIAGNOSTIC PIPELINE INITIALIZED")
    print("-" * 40)
    
    start_total_time = time.time()
    
    try:
        # ---- STAGE 1: SCRAPER & NETWORK TRIAGE ----
        print("-> [STAGE 1] Connecting to target database...")
        print("   Target Root URL: https://tamilchristiansongs.in")
        print(f"   Searching query string: '{song_name}'")
        
        print("-> Parsing network packets, matching strings, and dividing stanzas...")
        
        # ---- STAGE 2: PPT RENDER & STORAGE ----
        print("-> [STAGE 2] Handing data payload to python-pptx layout engine...")
        
        # Run your actual engine
        output_filepath = generate_ppt(song_name)
        
        end_total_time = time.time()
        
        # Calculate precise metrics
        total_duration = end_total_time - start_total_time
        
        # ---- STAGE 3: SUCCESS TELEMETRY REPORT ----
        print("-" * 40)
        print("[SUCCESS] AUTOMATION COMPLETED")
        print("-" * 40)
        print(f"   Total Processing Time : {total_duration:.2f} seconds")
        print(f"   Saved File Destination : {output_filepath}")
        print(f"   File Size              : {os.path.getsize(output_filepath) / 1024:.2f} KB")
        
        # Automatically pull up the presentation for verification
        print("-> Launching presentation window for visual inspection...")
        os.startfile(output_filepath)
        
    except Exception as error:
        # ---- STAGE 4: CRITICAL BUG TELEMETRY ----
        end_total_time = time.time()
        print("\n" + "!" * 60)
        print("[CRITICAL ENGINE CRASH DETECTED]")
        print("!" * 60)
        print(f"   Error Type: {type(error).__name__}")
        print(f"   Error Message: {str(error)}")
        print(f"   Crash occurred at: {time.time() - start_total_time:.2f} seconds into execution.")
        print("\n[STACK TRACE DECK]")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)

if __name__ == "__main__":
    while True:
        run_developer_cli()
        
        # Allow continuous developer testing without restarting the script manually
        keep_going = input("\nRun another debug cycle? (y/n): ").strip().lower()
        if keep_going != 'y':
            print("\nExiting Developer Console. Goodbye!")
            break