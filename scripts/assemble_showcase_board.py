from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root = Path(__file__).resolve().parents[1]
out = root/'reports'/'live_capture'/'showcase_board.txt'
out.write_text('Assemble final board from workstation screenshots in demo/live_capture/raw and processed metrics.
')
print(out)
