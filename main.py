import numpy as np
from flask import Flask, request, render_template_string
from PIL import Image

app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Colour Palette</title>
<style>
  body { font-family: sans-serif; max-width: 600px; margin: 40px auto; }
  .swatch { display: flex; align-items: center; gap: 12px; margin: 6px 0; }
  .swatch div { width: 60px; height: 40px; border: 1px solid #ccc; }
</style>
<h1>Top 10 colours</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="image" accept="image/*" required>
  <button>Upload</button>
</form>
{% for hex, pct in colours %}
  <div class="swatch"><div style="background:{{ hex }}"></div>{{ hex }} — {{ '%.1f' % pct }}%</div>
{% endfor %}
"""


def top_colours(file, n=10):
    img = Image.open(file).convert("RGB")
    img.thumbnail((300, 300))  # fewer pixels, same proportions
    px = np.asarray(img).reshape(-1, 3)
    px = px // 16 * 16 + 8  # group near-identical shades so photos don't return 10 tiny variations
    colours, counts = np.unique(px, axis=0, return_counts=True)
    top = np.argsort(counts)[::-1][:n]
    return [("#%02x%02x%02x" % tuple(colours[i]), counts[i] / len(px) * 100) for i in top]


@app.route("/", methods=["GET", "POST"])
def index():
    colours = top_colours(request.files["image"]) if request.method == "POST" else []
    return render_template_string(PAGE, colours=colours)


if __name__ == "__main__":
    app.run(debug=True)
