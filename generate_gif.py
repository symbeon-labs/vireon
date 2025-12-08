from PIL import Image, ImageDraw, ImageFont
import time
import os

# Configuration
WIDTH, HEIGHT = 800, 450
BG_COLOR = "#0D1117"  # GitHub Dark Dim
TEXT_COLOR = "#C9D1D9"
ACCENT_GREEN = "#00FF41" # Matrix/Bio Green
ACCENT_PURPLE = "#BD93F9" # Synth Purple
FONT_SIZE = 18
PADDING = 40
LINE_HEIGHT = 28

# Simulated terminal sequence
SEQUENCE = [
    ("$ vireon init --swarm-mode=active", 0.5),
    ("", 0.2),
    (f"[VIREON] Initializing Core v0.2.0...", 0.1),
    (f"[SYSTEM] Loading Neural Bridge modules... OK", 0.1),
    (f"[SYSTEM] Connecting to MCP Server... LINKED", 0.1),
    ("", 0.5),
    (f"> Task: Optimize symbiotic_bridge.rs for latency", 0.1),
    ("", 0.2),
    (f"[ORCHESTRATOR] Spawning Agents:", 0.0),
    (f"  ├─ [ARCHITECT] (Claude-3.5) Analyzing traits...", 0.3),
    (f"  ├─ [ENGINEER] (Copilot) Refactoring structs...", 0.4),
    (f"  └─ [AUDITOR] (GPT-4) Verifying memory safety...", 0.4),
    ("", 0.5),
    (f"[ENGINEER] Applied zero-copy deserialization.", 0.1),
    (f"[AUDITOR] Security Scan: PASS (Score: 99/100)", 0.1),
    ("", 0.2),
    (f"[VIREON] Consensus Reached.", 0.2),
    (f"[RESULT] Performance improved by 450%. Merging...", 0.5),
    ("", 1.0)
]

def create_frame(lines, cursor_visible=True):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to load a monospace font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE) # Standard Windows font
        # If user has a code font installed, even better, but keep it safe.
        font = ImageFont.truetype("consola.ttf", FONT_SIZE) 
    except:
        font = ImageFont.load_default()

    y = PADDING
    for line in lines:
        color = TEXT_COLOR
        if "[VIREON]" in line or "[RESULT]" in line:
            color = ACCENT_GREEN
        elif "[ORCHESTRATOR]" in line or "Task:" in line:
            color = ACCENT_PURPLE
        elif "$" in line:
            color = "#FFFFFF"
            
        draw.text((PADDING, y), line, font=font, fill=color)
        y += LINE_HEIGHT
    
    # Draw Cursor
    if cursor_visible:
        # Calculate cursor position roughly
        last_line_len = len(lines[-1]) if lines else 0
        cursor_x = PADDING + (last_line_len * (FONT_SIZE // 1.7)) # Approx width char
        # A simpler cursor at the start of next line if empty, or end of current
        if not lines:
             draw.rectangle([PADDING, y, PADDING+10, y+20], fill=ACCENT_GREEN)
        # Actually detailed cursor logic is hard with proportional fonts, 
        # let's just draw a blinking block at the bottom left if "processing" or end of text.
        
    return img

def generate_gif():
    frames = []
    current_lines = []
    
    # Header
    HEADER = "VIREON@SYMBEON-LABS:~/workspace"
    
    for text, delay in SEQUENCE:
        # typing effect for the command
        if text.startswith("$"):
            prefix = "$ "
            cmd = text[2:]
            for i in range(len(cmd) + 1):
                frame_lines = current_lines + [prefix + cmd[:i] + "█"]
                frames.append(create_frame(frame_lines, cursor_visible=False))
            # Remove cursor from command line final state
            current_lines.append(text)
        else:
            current_lines.append(text)
            frames.append(create_frame(current_lines, cursor_visible=False))
        
        # Add delay frames
        n_frames = int(delay * 10) # 10 fps
        if n_frames > 0:
            last_frame = frames[-1]
            for _ in range(n_frames):
                frames.append(last_frame)
    
    # Save
    print("Saving GIF...")
    frames[0].save('assets/vireon_demo.gif', save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
    print("Done: assets/vireon_demo.gif")

if __name__ == "__main__":
    generate_gif()
