"""
Tabla Audio Annotation Tool
Helps you create descriptive captions for tabla clips by guiding you through
a structured questionnaire. Saves progress automatically so you can resume anytime.
"""

import os
import json
import simpleaudio as sa
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
PROJECT_ROOT = r"C:\Motz_ACE_AI\raw_references\tabla"
AUDIO_FOLDERS = [
    # r"C:\Motz_ACE_AI\raw_references\tabla\references\tabla_1",
    # r"C:\Motz_ACE_AI\raw_references\tabla\references\tabla_2",
    r"C:\Motz_ACE_AI\raw_references\tabla\references\tabla_3",
]
OUTPUT_JSON = r"C:\Motz_ACE_AI\raw_references\tabla\dataset.json"
PROGRESS_FILE = r"C:\Motz_ACE_AI\raw_references\tabla\annotation_progress.json"

# Musical characteristics to evaluate
CHARACTERISTICS = {
    "tempo": {
        "question": "What is the tempo?",
        "options": {
            "1": "Very slow (meditative, ~40-60 BPM)",
            "2": "Medium (~80-120 BPM)",
            "3": "Very fast (~160+ BPM)"
        }
    },
    "energy": {
        "question": "What is the overall energy level?",
        "options": {
            "1": "Very calm, meditative",
            "2": "Moderate, steady",
            "3": "Very energetic, intense"
        }
    }

}

# Auto-populated default values
DEFAULTS = {
    "custom_tag": "tablastyle",
    "source": "Unknown",
    "bpm": 0  # Will be calculated or left empty
}


def load_audio_files(folders: List[str]) -> List[Tuple[str, str]]:
    """Scan folders and return list of (full_path, filename) tuples."""
    audio_files = []
    supported_extensions = {'.wav', '.mp3', '.flac', '.m4a'}
    
    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"⚠️ Warning: Folder not found: {folder}")
            continue
            
        for ext in supported_extensions:
            for file_path in folder_path.glob(f"*{ext}"):
                # Get relative path from project root for the JSON
                rel_path = str(file_path.relative_to(Path(PROJECT_ROOT)))
                audio_files.append((str(file_path), rel_path))
    
    # Sort for consistent order
    audio_files.sort(key=lambda x: x[0])
    return audio_files


def load_progress() -> Dict:
    """Load the progress tracking file if it exists."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed": [], "current_index": 0, "annotations": {}}


def save_progress(progress: Dict):
    """Save progress to file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def load_existing_annotations() -> Dict:
    """Load any existing annotations from the main dataset.json."""
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, 'r') as f:
            return {item['audio_path']: item for item in json.load(f)}
    return {}


def play_audio(file_path: str):
    """Play audio file using Windows Media Player."""
    print(f"🔊 Playing: {os.path.basename(file_path)}")
    print("   Listen to the audio and then press Enter...")
    
    # Open with default Windows player
    os.startfile(file_path)
    
    # Wait for user to finish listening
    input("\n   Press Enter after you've finished listening...")


def get_user_choice(prompt: str, options: Dict) -> str:
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for key, value in options.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("Enter choice (1-5): ").strip()
        if choice in options:
            return options[choice]
        print("❌ Invalid choice. Please enter a number between 1-5.")


def generate_caption(scores: Dict) -> str:
    """Generate a descriptive caption based on the user's choices."""
    tempo_map = {
        "Very slow (meditative, ~40-60 BPM)": "very slow, meditative",
        "Medium (~80-120 BPM)": "moderate tempo",
        "Very fast (~160+ BPM)": "very fast, energetic"
    }
    
    energy_map = {
        "Very calm, meditative": "with a calm, meditative energy",
        "Moderate, steady": "with steady, moderate energy",
        "Very energetic, intense": "with intense, high-energy playing"
    }

    
    # Build the caption
    caption_parts = []
    
    # Start with tempo and energy
    tempo_desc = tempo_map.get(scores['tempo'], scores['tempo'])
    energy_desc = energy_map.get(scores['energy'], scores['energy'])
    
    
    # Clean up and format
    caption = "".join(caption_parts)
    caption = caption.replace(",  ", ", ")
    caption = caption.replace(" ,", ",")
    caption = caption[0].upper() + caption[1:]
    
    return caption


def annotate_file(file_path: str, rel_path: str, existing_annotations: Dict) -> Optional[Dict]:
    """Annotate a single audio file."""
    if rel_path in existing_annotations:
        print(f"✅ Already annotated: {os.path.basename(file_path)}")
        return existing_annotations[rel_path]
    
    print(f"\n{'='*60}")
    print(f"📝 Annotating: {os.path.basename(file_path)}")
    print(f"   Path: {rel_path}")
    print(f"{'='*60}")
    
    # Play the audio
    play_audio(file_path)
    
    # Collect user choices
    scores = {}
    print("\n🎵 Please describe what you heard:")
    
    for key, char in CHARACTERISTICS.items():
        scores[key] = get_user_choice(char["question"], char["options"])
    
    # Generate the caption
    caption = generate_caption(scores)
    
    # Show the generated caption
    print(f"\n📝 Generated caption:")
    print(f"   {caption}")
    
    # Get final approval
    while True:
        response = input("\n✅ Is this caption accurate? (y/n/edit): ").strip().lower()
        if response == 'y':
            break
        elif response == 'n':
            caption = input("Enter your custom caption: ").strip()
            break
        elif response == 'edit':
            caption = input("Edit the caption: ").strip()
            break
        else:
            print("❌ Please enter 'y', 'n', or 'edit'.")
    
    # Build the annotation entry
    annotation = {
        "audio_path": rel_path,
        "caption": caption,
        "custom_tag": DEFAULTS["custom_tag"],
        "genre": DEFAULTS["genre"],
        "instrument": DEFAULTS["instrument"],
        "source": os.path.basename(os.path.dirname(file_path)),
        "bpm": DEFAULTS["bpm"],
        "duration": 0,  # Could be calculated
        "tempo_score": scores['tempo'],
        "energy_score": scores['energy']
    }
    
    return annotation


def main():
    """Main annotation workflow."""
    print("🎯 Tabla Annotation Tool")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Output JSON: {OUTPUT_JSON}")
    print("="*60)
    
    # Load progress
    progress = load_progress()
    existing_annotations = load_existing_annotations()
    
    # Load all audio files
    print("\n📂 Scanning for audio files...")
    audio_files = load_audio_files(AUDIO_FOLDERS)
    print(f"✅ Found {len(audio_files)} audio files")
    
    if not audio_files:
        print("❌ No audio files found!")
        return
    
    # Start from where we left off
    start_index = progress["current_index"]
    completed = progress["completed"]
    
    print(f"\n📊 Progress: {len(completed)}/{len(audio_files)} files completed")
    if start_index < len(audio_files):
        print(f"🔄 Resuming from file {start_index + 1}")
    
    # Annotate each file
    new_annotations = []
    
    for i, (full_path, rel_path) in enumerate(audio_files[start_index:], start=start_index):
        print(f"\n📍 File {i+1}/{len(audio_files)}")
        
        # Annotate the file
        annotation = annotate_file(full_path, rel_path, existing_annotations)
        
        if annotation:
            new_annotations.append(annotation)
            completed.append(rel_path)
            
            # Save progress after each file
            progress["completed"] = completed
            progress["current_index"] = i + 1
            
            # Update annotations in progress
            if "annotations" not in progress:
                progress["annotations"] = {}
            progress["annotations"][rel_path] = annotation
            
            save_progress(progress)
            
            # Save the main JSON file periodically
            all_annotations = list(existing_annotations.values()) + new_annotations
            with open(OUTPUT_JSON, 'w') as f:
                json.dump(all_annotations, f, indent=2)
            
            print(f"💾 Progress saved: {len(completed)}/{len(audio_files)}")
        
        # Ask if user wants to continue or pause
        if i < len(audio_files) - 1:
            response = input("\n⏸️  Continue to next file? (y/n): ").strip().lower()
            if response != 'y':
                print("⏹️  Pausing. Progress saved. Run the script again to resume.")
                return
    
    print(f"\n🎉 All done! Annotated {len(audio_files)} files.")
    print(f"📁 Output saved to: {OUTPUT_JSON}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user. Progress saved.")
        print("Run the script again to resume.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
