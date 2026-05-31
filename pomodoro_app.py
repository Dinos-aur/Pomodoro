import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Focus Flow", page_icon="🍅", layout="centered")

MODES = {"Focus": 25 * 60, "Short Break": 5 * 60, "Long Break": 15 * 60}

if "mode"      not in st.session_state: st.session_state.mode      = "Focus"
if "tasks"     not in st.session_state: st.session_state.tasks     = []
if "pomodoros" not in st.session_state: st.session_state.pomodoros = 0
if "bg_url"    not in st.session_state: st.session_state.bg_url    = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600"

bg = st.session_state.bg_url

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: url('{bg}') center/cover no-repeat fixed !important;
  }}
  .stApp::before {{
    content: '';
    position: fixed; inset: 0;
    background: rgba(10, 8, 20, 0.55);
    backdrop-filter: blur(2px);
    z-index: 0;
  }}
  [data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }}
  #MainMenu, footer, header {{ visibility: hidden; }}
  * {{ font-family: 'DM Sans', sans-serif; color: #f0ece4; }}
  h1, h2, h3 {{ font-family: 'DM Serif Display', serif; }}
  .stButton > button {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #f0ece4 !important;
    border-radius: 12px !important;
    padding: 0.55rem 1.4rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
    box-shadow: 0 12px 50px rgba(0,0,0,0.6) !important;
  }}
  .stButton > button:hover {{
    background: rgba(246,161,75,0.3) !important;
    border-color: #f6a14b !important;
  }}
  .block-container {{ padding-top: 2rem !important; max-width: 680px; }}
</style>
""", unsafe_allow_html=True)

# ── Title ───────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;margin-bottom:0;position:relative;z-index:1;'>Focus Flow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:0.5;font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1.5rem;position:relative;z-index:1;'>Pomodoro Timer</p>", unsafe_allow_html=True)

# ── Mode buttons ───────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, label in zip([c1, c2, c3], MODES):
    with col:
        if st.button(label, key=f"mode_{label}", use_container_width=True):
            st.session_state.mode = label
            st.rerun()

total_secs = MODES[st.session_state.mode]
mins_init  = total_secs // 60
pomodoros  = st.session_state.pomodoros

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; font-family:'DM Sans',sans-serif; overflow-x:hidden; }}

  #hamburger {{
    position: absolute;
    top: 0.6rem; right: 0.75rem;
    width: 2.2rem; height: 2.2rem;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.20);
    border-radius: 8px;
    cursor: pointer;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 4px; z-index: 100;
    transition: background 0.2s;
    box-shadow: 0 8px 35px rgba(0,0,0,0.5);
  }}
  #hamburger:hover {{ background: rgba(246,161,75,0.25); border-color:#f6a14b; }}
  #hamburger span {{
    display:block; width:1rem; height:2px;
    background:#f0ece4; border-radius:2px;
    transition: all 0.25s;
  }}
  #hamburger.open span:nth-child(1) {{ transform: translateY(6px) rotate(45deg); }}
  #hamburger.open span:nth-child(2) {{ opacity:0; }}
  #hamburger.open span:nth-child(3) {{ transform: translateY(-6px) rotate(-45deg); }}

  #settings-panel {{
    display: none;
    background: rgba(10,8,20,0.80);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 12px 50px rgba(0,0,0,0.6);
  }}
  #settings-panel.open {{ display: block; }}
  .settings-label {{
    font-size: 0.75rem; letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(240,236,228,0.5);
    margin-bottom: 0.5rem;
  }}
  .settings-row {{ display:flex; gap:0.5rem; align-items:center; }}
  #bg-input {{
    flex:1;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 10px;
    padding: 0.45rem 0.75rem;
    color: #f0ece4;
    font-size: 0.85rem;
    font-family: 'DM Sans', sans-serif;
    outline: none;
  }}
  #bg-input:focus {{ border-color: #f6a14b; }}
  #bg-apply {{
    background: rgba(246,161,75,0.25);
    border: 1px solid #f6a14b;
    color: #f0ece4; border-radius: 10px;
    padding: 0.45rem 0.9rem; font-size: 0.85rem;
    cursor: pointer; font-family: 'DM Sans', sans-serif;
    white-space: nowrap; transition: background 0.2s;
    box-shadow: 0 8px 35px rgba(0,0,0,0.5);
  }}
  #bg-apply:hover {{ background: rgba(246,161,75,0.45); }}

  .glass {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 24px;
    padding: 2rem 2rem 1.5rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 12px 50px rgba(0,0,0,0.6);
    margin-bottom: 1rem; text-align: center;
  }}
  .timer-label {{
    font-size: 0.8rem; letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(240,236,228,0.6);
    margin-bottom: 0.75rem;
  }}
  .timer-row {{
    display:flex; align-items:center;
    justify-content:center; gap:1rem;
  }}
  .adj-btn {{
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.22);
    color: #f0ece4; border-radius: 10px;
    width:2.6rem; height:2.6rem; font-size:1.4rem;
    cursor:pointer; font-family:'DM Sans',sans-serif;
    transition:all 0.2s; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    box-shadow: 0 8px 35px rgba(0,0,0,0.5);
  }}
  .adj-btn:hover {{ background:rgba(246,161,75,0.3); border-color:#f6a14b; }}
  .adj-btn:disabled {{ opacity:0.3; cursor:not-allowed; }}

  .timer-wrap {{
    position:relative; min-width:11rem;
    display:flex; flex-direction:column; align-items:center;
  }}
  #timer-display {{
    font-family:'DM Serif Display',serif;
    font-size:5.5rem; line-height:1; color:#fff;
    text-shadow:0 0 40px rgba(255,200,120,0.4);
    cursor:pointer; border-radius:8px;
    padding:0.1rem 0.3rem;
    transition:background 0.2s;
    white-space:nowrap;
    border:2px solid transparent;
  }}
  #timer-display:hover {{ background:rgba(255,255,255,0.07); }}

  #timer-input {{
    font-family:'DM Serif Display',serif;
    font-size:5.5rem; line-height:1; color:#fff;
    text-shadow:0 0 40px rgba(255,200,120,0.4);
    background:rgba(255,255,255,0.07);
    border:2px solid #f6a14b;
    border-radius:8px;
    padding:0.1rem 0.3rem;
    text-align:center; width:100%; outline:none;
    display:none;
  }}
  .edit-hint {{
    font-size:0.72rem; color:rgba(240,236,228,0.45);
    margin-top:0.35rem; min-height:1em;
    letter-spacing:0.05em;
  }}

  .progress-wrap {{
    width:100%; height:4px;
    background:rgba(255,255,255,0.12);
    border-radius:99px; margin:1.25rem 0 0; overflow:hidden;
  }}
  #progress-fill {{
    height:100%;
    background:linear-gradient(90deg,#f6a14b,#e86d4b);
    border-radius:99px; width:0%;
    transition:width 0.9s linear;
  }}
  .controls {{ display:flex; justify-content:center; gap:0.75rem; margin-top:1rem; }}
  .timer-btn {{
    background:rgba(255,255,255,0.12);
    border:1px solid rgba(255,255,255,0.25);
    color:#f0ece4; border-radius:12px;
    padding:0.55rem 1.8rem; font-size:0.9rem;
    letter-spacing:0.05em; cursor:pointer;
    font-family:'DM Sans',sans-serif; transition:all 0.2s;
    box-shadow: 0 8px 35px rgba(0,0,0,0.5);
  }}
  .timer-btn:hover {{ background:rgba(246,161,75,0.3); border-color:#f6a14b; }}
  .pomodoro-count {{
    text-align:center; color:rgba(240,236,228,0.7);
    font-size:0.95rem; margin-top:0.75rem;
  }}
</style>
</head>
<body>

<div id="hamburger" onclick="toggleSettings()">
  <span></span><span></span><span></span>
</div>

<div id="settings-panel">
  <p class="settings-label">Background Image</p>
  <div class="settings-row">
    <input id="bg-input" type="text" value="{bg}" placeholder="Paste image URL…" />
    <button id="bg-apply" onclick="applyBg()">Apply</button>
  </div>
</div>

<div class="glass">
  <p class="timer-label">{st.session_state.mode}</p>
  <div class="timer-row">
    <button class="adj-btn" id="minus-btn">−</button>
    <div class="timer-wrap">
      <div id="timer-display">{mins_init:02d}:00</div>
      <input id="timer-input" type="text" maxlength="6" placeholder="e.g. 25" />
      <p class="edit-hint" id="edit-hint">click timer to edit</p>
    </div>
    <button class="adj-btn" id="plus-btn">+</button>
  </div>
  <div class="progress-wrap"><div id="progress-fill"></div></div>
</div>

<div class="controls">
  <button class="timer-btn" id="start-btn">▶ Start</button>
  <button class="timer-btn" id="reset-btn">↺ Reset</button>
</div>
<p class="pomodoro-count" id="pomo-count">🍅 × {pomodoros}</p>

<script>
  // ── background ───────────────────────────────────────────────────────────
  function applyBg() {{
    const url = document.getElementById('bg-input').value.trim();
    if (url) {{
      window.parent.postMessage({{type:'setBg', url}}, '*');
      // Persist to session state
      if (window.parent !== window) {{
        window.parent.postMessage({{type:'saveBgUrl', url}}, '*');
      }}
    }}
  }}
  document.getElementById('bg-input').addEventListener('keydown', function(e) {{
    if (e.key === 'Enter') applyBg();
  }});

  // listen for ack from parent to confirm it worked
  window.addEventListener('message', function(e) {{
    if (e.data && e.data.type === 'bgApplied') {{
      document.getElementById('bg-apply').textContent = '✓';
      setTimeout(() => document.getElementById('bg-apply').textContent = 'Apply', 1500);
    }}
  }});

  function toggleSettings() {{
    document.getElementById('settings-panel').classList.toggle('open');
    document.getElementById('hamburger').classList.toggle('open');
  }}

  // ── timer ────────────────────────────────────────────────────────────
  const STEP = 5 * 60;
  let TOTAL       = {total_secs};
  let secondsLeft = TOTAL;
  let running     = false;
  let interval    = null;
  let editing     = false;
  let pomodoros   = {pomodoros};

  const display   = document.getElementById('timer-display');
  const input     = document.getElementById('timer-input');
  const hint      = document.getElementById('edit-hint');
  const progress  = document.getElementById('progress-fill');
  const startBtn  = document.getElementById('start-btn');
  const resetBtn  = document.getElementById('reset-btn');
  const plusBtn   = document.getElementById('plus-btn');
  const minusBtn  = document.getElementById('minus-btn');
  const pomoCount = document.getElementById('pomo-count');

  function fmt(s) {{
    return String(Math.floor(s/60)).padStart(2,'0') + ':' + String(s%60).padStart(2,'0');
  }}
  function render() {{
    display.textContent  = fmt(secondsLeft);
    progress.style.width = (100 * (1 - secondsLeft / TOTAL)) + '%';
  }}
  function tick() {{
    if (secondsLeft > 0) {{
      secondsLeft--;
      render();
    }} else {{
      clearInterval(interval);
      running = false;
      startBtn.textContent = '▶ Start';
      pomodoros++;
      pomoCount.textContent = '🍅 × ' + pomodoros;
    }}
  }}

  startBtn.addEventListener('click', function() {{
    if (editing) commitEdit();
    if (running) {{
      clearInterval(interval); running = false;
      startBtn.textContent = '▶ Start';
    }} else {{
      interval = setInterval(tick, 1000); running = true;
      startBtn.textContent = '⏸ Pause';
    }}
  }});

  resetBtn.addEventListener('click', function() {{
    clearInterval(interval); running = false;
    secondsLeft = TOTAL;
    startBtn.textContent = '▶ Start';
    render();
  }});

  plusBtn.addEventListener('click',  function() {{ if (!running) {{ TOTAL = Math.min(TOTAL + STEP, 99*60); secondsLeft = TOTAL; render(); }} }});
  minusBtn.addEventListener('click', function() {{ if (!running) {{ TOTAL = Math.max(TOTAL - STEP, STEP);  secondsLeft = TOTAL; render(); }} }});

  // ── smart time parsing ────────────────────────────────────────────────────
  // Accepts:
  //   "25"     → 25 minutes
  //   "25:00"  → 25 minutes
  //   "1000"   → 10 minutes 00 seconds  (MMSS)
  //   "500"    → 5 minutes 00 seconds   (MSS)
  //   "5"      → 5 minutes
  //   "0:30"   → 30 seconds
  //   "30s"    → 30 seconds
  function parseTime(raw) {{
    const val = raw.trim().toLowerCase();
    if (!val) return null;

    // explicit colon format  MM:SS  or  M:SS
    if (/^\d{{1,2}}:\d{{2}}$/.test(val)) {{
      const [m, s] = val.split(':').map(Number);
      if (s < 60) return m * 60 + s;
    }}

    // trailing 's' = seconds  e.g. "30s"
    if (/^\d+s$/.test(val)) {{
      const s = parseInt(val);
      if (s > 0 && s < 3600) return s;
    }}

    // pure digits
    if (/^\d+$/.test(val)) {{
      const n = parseInt(val);
      // 1-3 digits → treat as whole minutes
      if (val.length <= 3) return n * 60;
      // 4 digits → MMSS  e.g. 2500 = 25min, 1000 = 10min
      if (val.length === 4) {{
        const m = parseInt(val.slice(0, 2));
        const s = parseInt(val.slice(2));
        if (s < 60) return m * 60 + s;
      }}
      // 5+ digits → HMMSS or fall back to treating as minutes
      if (val.length === 5) {{
        const m = parseInt(val.slice(0, 3));
        const s = parseInt(val.slice(3));
        if (s < 60) return m * 60 + s;
      }}
      // fallback: just minutes
      return n * 60;
    }}
    return null;
  }}

  display.addEventListener('click', function() {{
    if (running) return;
    editing = true;
    input.value = fmt(secondsLeft);
    display.style.display = 'none';
    input.style.display   = 'block';
    hint.textContent = '25 = 25 min · 1000 = 10:00 · 30s = 30 sec · Enter to confirm';
    input.focus(); input.select();
  }});

  function commitEdit() {{
    editing = false;
    const parsed = parseTime(input.value);
    if (parsed && parsed > 0 && parsed <= 99*60) {{
      TOTAL = parsed; secondsLeft = TOTAL;
    }}
    input.style.display   = 'none';
    display.style.display = 'block';
    hint.textContent = 'click timer to edit';
    render();
  }}

  input.addEventListener('keydown', function(e) {{
    if (e.key === 'Enter') commitEdit();
    if (e.key === 'Escape') {{
      editing = false;
      input.style.display   = 'none';
      display.style.display = 'block';
      hint.textContent = 'click timer to edit';
    }}
  }});
  input.addEventListener('blur', function() {{ if (editing) commitEdit(); }});

  render();
</script>
</body>
</html>
""", height=340)

# ── Receive background changes from iframe via postMessage ────────────────────
# We inject a listener into the main Streamlit page
st.markdown("""
<script>
(function() {
  function applyBackground(url) {
    const targets = [
      document.querySelector('.stApp'),
      document.querySelector('[data-testid="stAppViewContainer"]'),
      document.body,
      document.documentElement
    ];
    targets.forEach(el => {
      if (el) {
        el.style.setProperty('background',
          "url('" + url + "') center/cover no-repeat fixed", 'important');
      }
    });
  }

  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'setBg') {
      applyBackground(e.data.url);
      // ack back to iframe
      const iframe = document.querySelector('iframe');
      if (iframe) iframe.contentWindow.postMessage({type:'bgApplied'}, '*');
    }
    // Handle saving bg URL to session state
    if (e.data && e.data.type === 'saveBgUrl') {
      // This would need server-side handling via Streamlit's callback
      // For now, the background change happens immediately via CSS
    }
  });
})();
</script>
""", unsafe_allow_html=True)

# ── Task list ────────────────────────────────────────────────────────────
st.markdown("<h3 style='margin-bottom:0.75rem;position:relative;z-index:1;'>📋 Tasks</h3>", unsafe_allow_html=True)

with st.form("add_task_form", clear_on_submit=True):
    col_input, col_btn = st.columns([0.82, 0.18])
    with col_input:
        new_task = st.text_input("", placeholder="Add a new task…", label_visibility="collapsed")
    with col_btn:
        submitted = st.form_submit_button("Add", use_container_width=True)
    if submitted and new_task.strip():
        st.session_state.tasks.append({"text": new_task.strip(), "done": False})

if not st.session_state.tasks:
    st.markdown("<p style='opacity:0.4;text-align:center;padding:1.5rem 0;'>No tasks yet — add one above ↑</p>", unsafe_allow_html=True)

for i, task in enumerate(st.session_state.tasks):
    col_check, col_text, col_del = st.columns([0.08, 0.8, 0.12])
    with col_check:
        checked = st.checkbox("", value=task["done"], key=f"chk_{i}", label_visibility="collapsed")
        if checked != task["done"]:
            st.session_state.tasks[i]["done"] = checked
            st.rerun()
    with col_text:
        style = "text-decoration:line-through;opacity:0.45;" if task["done"] else ""
        st.markdown(f"<p style='padding-top:0.4rem;{style}'>{task['text']}</p>", unsafe_allow_html=True)
    with col_del:
        if st.button("✕", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()
