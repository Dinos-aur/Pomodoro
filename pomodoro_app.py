import streamlit as st
import time

st.set_page_config(page_title="Focus Flow", page_icon="🍅", layout="centered")

# ── Sidebar: background URL ───────────────────────────────────────────────────
BG_URL = st.sidebar.text_input(
    "Background image URL",
    value="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600",
)

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
  .stApp {{
    background: url('{BG_URL}') center/cover no-repeat fixed;
  }}
  .stApp::before {{
    content: '';
    position: fixed; inset: 0;
    background: rgba(10, 8, 20, 0.55);
    backdrop-filter: blur(2px);
    z-index: 0;
  }}
  .glass {{
    position: relative; z-index: 1;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 24px;
    padding: 2.5rem 2rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.35);
    margin-bottom: 1.5rem;
    text-align: center;
  }}
  * {{ font-family: 'DM Sans', sans-serif; color: #f0ece4; }}
  h1, h2, h3 {{ font-family: 'DM Serif Display', serif; }}
  .timer-display {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(4rem, 12vw, 7rem);
    line-height: 1;
    color: #fff;
    text-shadow: 0 0 40px rgba(255,200,120,0.4);
  }}
  .timer-label {{
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.6;
    margin-bottom: 0.25rem;
  }}
  .progress-wrap {{
    width: 100%; height: 4px;
    background: rgba(255,255,255,0.12);
    border-radius: 99px;
    margin: 1.25rem 0;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, #f6a14b, #e86d4b);
    border-radius: 99px;
  }}
  .stButton > button {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #f0ece4 !important;
    border-radius: 12px !important;
    padding: 0.55rem 1.4rem !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
  }}
  .stButton > button:hover {{
    background: rgba(246,161,75,0.3) !important;
    border-color: #f6a14b !important;
  }}
  [data-testid="stSidebar"] {{
    background: rgba(10,8,20,0.7) !important;
    backdrop-filter: blur(12px) !important;
  }}
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 2rem !important; max-width: 680px; }}
</style>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────────────
MODES = {"Focus": 25 * 60, "Short Break": 5 * 60, "Long Break": 15 * 60}

if "mode"         not in st.session_state: st.session_state.mode         = "Focus"
if "seconds_left" not in st.session_state: st.session_state.seconds_left = MODES["Focus"]
if "running"      not in st.session_state: st.session_state.running      = False
if "last_tick"    not in st.session_state: st.session_state.last_tick    = None
if "tasks"        not in st.session_state: st.session_state.tasks        = []
if "pomodoros"    not in st.session_state: st.session_state.pomodoros    = 0
if "task_input"   not in st.session_state: st.session_state.task_input   = ""

# ── Auto-refresh (only while running, no sleep) ───────────────────────────────
if st.session_state.running:
    st.rerun()

# ── Tick (only when running) ──────────────────────────────────────────────────
if st.session_state.running:
    now = time.time()
    if st.session_state.last_tick is not None:
        elapsed = int(now - st.session_state.last_tick)
        if elapsed > 0:
            st.session_state.seconds_left = max(0, st.session_state.seconds_left - elapsed)
            if st.session_state.seconds_left == 0:
                st.session_state.running = False
                if st.session_state.mode == "Focus":
                    st.session_state.pomodoros += 1
    st.session_state.last_tick = now

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;margin-bottom:0;'>Focus Flow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:0.5;font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1.5rem;'>Pomodoro Timer</p>", unsafe_allow_html=True)

# ── Mode buttons ────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, label in zip([c1, c2, c3], MODES):
    with col:
        if st.button(label, key=f"mode_{label}", use_container_width=True):
            st.session_state.mode         = label
            st.session_state.seconds_left = MODES[label]
            st.session_state.running      = False
            st.session_state.last_tick    = None
            st.rerun()

# ── Timer display ───────────────────────────────────────────────────────────
total    = MODES[st.session_state.mode]
secs     = st.session_state.seconds_left
mins, s  = divmod(secs, 60)
pct      = 100 * (1 - secs / total) if total else 100

st.markdown(f"""
<div class="glass">
  <p class="timer-label">{st.session_state.mode}</p>
  <div class="timer-display">{mins:02d}:{s:02d}</div>
  <div class="progress-wrap">
    <div class="progress-fill" style="width:{pct:.1f}%"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls ────────────────────────────────────────────────────────────────
b1, b2, b3 = st.columns([1, 1, 1])
with b1:
    if st.button("⏸ Pause" if st.session_state.running else "▶ Start", use_container_width=True):
        st.session_state.running   = not st.session_state.running
        st.session_state.last_tick = time.time() if st.session_state.running else None
        st.rerun()
with b2:
    if st.button("↺ Reset", use_container_width=True):
        st.session_state.seconds_left = MODES[st.session_state.mode]
        st.session_state.running      = False
        st.session_state.last_tick    = None
        st.rerun()
with b3:
    st.markdown(f"<p style='text-align:center;padding-top:0.6rem;opacity:0.7;'>🍅 × {st.session_state.pomodoros}</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Task list ────────────────────────────────────────────────────────────────
st.markdown("<h3 style='margin-bottom:0.75rem;'>📋 Tasks</h3>", unsafe_allow_html=True)

# Use a form so the input only submits on Enter/button click, not every keystroke
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
