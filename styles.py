"""Look and feel for the digital twin Gradio app.

The theme does most of the work (colors, font, corners, light/dark).
CSS only handles layout and the custom header.
"""

import gradio as gr

EXAMPLES = [
    "Tell me about your background and experience.",
    "What are you working on right now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

HEADER = """
<div class="twin-header">
  <div class="twin-avatar">SA</div>
  <div class="twin-id">
    <h1>Sameer Ahmed</h1>
    <p>Frontend engineer · React, TypeScript &amp; Shopify</p>
  </div>
  <span class="twin-badge">AI twin</span>
</div>
"""

PLACEHOLDER = """
**Hi, I'm Sameer's AI twin.**

Ask me about my work, skills or experience. Want to work together? Leave your email and I'll pass it on.
"""

THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.indigo,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "monospace"],
    radius_size=gr.themes.sizes.radius_lg,
    text_size=gr.themes.sizes.text_md,
).set(
    body_background_fill="#f6f7f9",
    body_background_fill_dark="#0e1015",
    background_fill_primary="#ffffff",
    background_fill_primary_dark="#161922",
    background_fill_secondary="#f1f3f6",
    background_fill_secondary_dark="#1e2230",
    # Panels (chat area, input card) sit on the primary fill, so bot bubbles
    # (secondary fill) stand out against them
    block_background_fill="#ffffff",
    block_background_fill_dark="#161922",
    block_border_color="#e3e6eb",
    block_border_color_dark="#262b38",
    border_color_primary="#e3e6eb",
    border_color_primary_dark="#262b38",
    color_accent_soft="#eef0ff",
    color_accent_soft_dark="#2a2f55",
    button_primary_background_fill="#4f46e5",
    button_primary_background_fill_hover="#4338ca",
    button_primary_background_fill_dark="#6366f1",
    button_primary_background_fill_hover_dark="#818cf8",
    button_primary_text_color="#ffffff",
    input_background_fill="#ffffff",
    input_background_fill_dark="#161922",
    block_shadow="0 1px 2px rgba(16, 24, 40, 0.04)",
    block_shadow_dark="none",
)

CSS = """
footer, .built-with, .show-api { display: none !important; }

.gradio-container {
  max-width: 760px !important;
  margin: 0 auto !important;
  padding: 24px 16px !important;
}

/* ---------- Header ---------- */
.twin-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 4px 2px 8px;
}
.twin-avatar {
  flex: none;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 600;
  font-size: 17px;
  letter-spacing: 0.02em;
  color: #ffffff;
  background: linear-gradient(135deg, #6366f1, #4338ca);
}
.twin-id { flex: 1; min-width: 0; }
.twin-id h1 {
  margin: 0 !important;
  font-size: 20px !important;
  font-weight: 650 !important;
  letter-spacing: -0.01em;
  color: var(--body-text-color);
}
.twin-id p {
  margin: 2px 0 0 !important;
  font-size: 14px;
  color: var(--body-text-color-subdued);
}
.twin-badge {
  flex: none;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
  color: #4338ca;
  background: #eef0ff;
}
.dark .twin-badge { color: #c7d2fe; background: #2a2f55; }

/* ---------- Chat ---------- */
.twin-chat .message { font-size: 15px; line-height: 1.6; padding: 10px 14px !important; }
.twin-chat .message.bot { border: 1px solid var(--border-color-primary); border-radius: 14px 14px 14px 4px !important; }
.twin-chat .message.user { border-radius: 14px 14px 4px 14px !important; }
.twin-chat .placeholder { text-align: center; padding: 0 32px; color: var(--body-text-color-subdued); }
.twin-chat table th, .twin-chat table td { word-break: normal; overflow-wrap: normal; }

/* ---------- Input: one card, text field blends in, gap before the button ---------- */
.input-container { gap: 10px; align-items: center; }
.input-container textarea {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 8px 4px !important;
  font-size: 15px;
}
.submit-button {
  flex: none;
  width: 36px !important;
  height: 36px !important;
  border-radius: 50% !important;
  background: var(--button-primary-background-fill) !important;
  color: #ffffff !important;
}
.submit-button:hover { background: var(--button-primary-background-fill-hover) !important; }
.block:has(> label > .input-container) {
  border-radius: 14px !important;
  border: 1px solid var(--border-color-primary) !important;
  padding: 6px 8px 6px 14px !important;
}
.block:has(> label > .input-container):focus-within { border-color: var(--color-accent) !important; }

@media (max-width: 640px) {
  .gradio-container { padding: 16px 12px !important; }
  .twin-badge { display: none; }
}
"""

JS = """
() => {
  document.title = 'Sameer Ahmed · AI twin';

  // Put the cursor back in the message box whenever Gradio re-enables it
  // (i.e. after the twin finishes replying).
  const watch = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled;
    new MutationObserver(() => {
      if (wasDisabled && !area.disabled) area.focus();
      wasDisabled = area.disabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled'] });
  };
  const scan = () => document.querySelectorAll('textarea').forEach(watch);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
  setTimeout(() => { scan(); document.querySelector('textarea')?.focus(); }, 300);
}
"""
