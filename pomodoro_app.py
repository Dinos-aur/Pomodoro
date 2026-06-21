import streamlit as st
import streamlit.components.v1 as components
import re

st.set_page_config(page_title="Focus Flow", page_icon="🍅", layout="centered")

MODES = {"Focus": 25 * 60, "Short Break": 5 * 60, "Long Break": 15 * 60}

if "mode"      not in st.session_state: st.session_state.mode      = "Focus"
if "tasks"     not in st.session_state: st.session_state.tasks     = []
if "pomodoros" not in st.session_state: st.session_state.pomodoros = 0
if "bg_url"    not in st.session_state: st.session_state.bg_url    = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1600"
if "yt_url"    not in st.session_state: st.session_state.yt_url    = "https://www.youtube.com/live/X4VbdwhkE10"

def extract_yt_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

bg    = st.session_state.bg_url
yt    = st.session_state.yt_url
yt_id = extract_yt_id(yt) if yt else None

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
  html, body, .stApp, [data-testid="stAppViewContainer"] {{
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
  }}
  .stButton > button:hover {{
    background: rgba(246,161,75,0.3) !important;
    border-color: #f6a14b !important;
  }}
  .block-container {{ padding-top: 2rem !important; max-width: 680px; }}
  div[data-testid="stForm"] {{ background: transparent !important; border: none !important; }}
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;margin-bottom:0;position:relative;z-index:1;'>Focus Flow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:0.5;font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1.5rem;position:relative;z-index:1;'>Pomodoro Timer</p>", unsafe_allow_html=True)

# ── Settings expander ─────────────────────────────────────────────────────────
with st.expander("⚙️ Settings"):
    st.markdown("<p style='font-size:0.8rem;letter-spacing:0.15em;text-transform:uppercase;opacity:0.5;margin-bottom:0.25rem;'>Background Image URL</p>", unsafe_allow_html=True)
    with st.form("bg_form"):
        bg_col, bg_btn = st.columns([0.82, 0.18])
        with bg_col:
            new_bg = st.text_input("bg", value=st.session_state.bg_url, label_visibility="collapsed")
        with bg_btn:
            bg_submitted = st.form_submit_button("Apply", use_container_width=True)
        if bg_submitted and new_bg.strip():
            st.session_state.bg_url = new_bg.strip()
            st.rerun()

    st.markdown("<p style='font-size:0.8rem;letter-spacing:0.15em;text-transform:uppercase;opacity:0.5;margin-bottom:0.25rem;margin-top:0.75rem;'>YouTube Music URL</p>", unsafe_allow_html=True)
    with st.form("yt_form"):
        yt_col, yt_btn = st.columns([0.82, 0.18])
        with yt_col:
            new_yt = st.text_input("yt", value=st.session_state.yt_url, placeholder="e.g. https://youtube.com/watch?v=...", label_visibility="collapsed")
        with yt_btn:
            yt_submitted = st.form_submit_button("Load", use_container_width=True)
        if yt_submitted:
            st.session_state.yt_url = new_yt.strip()
            st.rerun()

# ── YouTube player ─────────────────────────────────────────────────────────────
if yt_id:
    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:transparent; font-family:'DM Sans',sans-serif; }}
  .player-card {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 16px; padding: 0.85rem 1rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.25);
  }}
  .top-row {{ display:flex; align-items:center; gap:0.85rem; }}
  #video-wrap {{
    flex-shrink:0; transition:all 0.3s ease;
    border-radius:10px; overflow:hidden;
    width:140px; height:79px;
  }}
  #video-wrap.hidden {{ width:0; height:0; opacity:0; margin:0; padding:0; }}
  #video-wrap iframe {{ width:140px; height:79px; border:none; display:block; border-radius:10px; }}

  /* mini controls shown when video is hidden */
  #mini-controls {{
    display: none;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0;
  }}
  #video-wrap.hidden ~ .info ~ #toggle-video {{ }}
  .mini-btn {{
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.22);
    color: #f0ece4; border-radius: 8px;
    width: 2.2rem; height: 2.2rem;
    font-size: 0.9rem; cursor: pointer;
    font-family: 'DM Sans', sans-serif;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.2s;
  }}
  .mini-btn:hover {{ background: rgba(246,161,75,0.25); border-color: #f6a14b; }}
  .info {{ flex:1; min-width:0; }}
  .now-playing-label {{ font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; color:rgba(240,236,228,0.45); margin-bottom:0.2rem; }}
  .now-playing-text  {{ font-size:0.88rem; color:#f0ece4; opacity:0.9; }}
  .tip-text          {{ font-size:0.72rem; color:rgba(240,236,228,0.38); margin-top:0.15rem; }}
  #toggle-video {{
    flex-shrink:0; background:rgba(255,255,255,0.10);
    border:1px solid rgba(255,255,255,0.20); color:#f0ece4;
    border-radius:8px; padding:0.35rem 0.7rem; font-size:0.78rem;
    cursor:pointer; font-family:'DM Sans',sans-serif;
    white-space:nowrap; transition:all 0.2s; letter-spacing:0.04em;
  }}
  #toggle-video:hover {{ background:rgba(246,161,75,0.25); border-color:#f6a14b; }}
  .volume-row {{ display:flex; align-items:center; gap:0.6rem; margin-top:0.75rem; }}
  .vol-icon {{ font-size:0.9rem; }}
  input[type=range] {{
    -webkit-appearance:none; flex:1; height:4px;
    border-radius:99px; background:rgba(255,255,255,0.18);
    outline:none; cursor:pointer;
  }}
  input[type=range]::-webkit-slider-thumb {{
    -webkit-appearance:none; width:14px; height:14px;
    border-radius:50%; background:#f6a14b; cursor:pointer;
  }}
  input[type=range]::-moz-range-thumb {{
    width:14px; height:14px; border:none;
    border-radius:50%; background:#f6a14b; cursor:pointer;
  }}
  .vol-pct {{ font-size:0.75rem; color:rgba(240,236,228,0.5); min-width:2.5rem; text-align:right; }}
</style>
</head>
<body>
<div class="player-card">
  <div class="top-row">
    <div id="video-wrap">
      <!-- volume is controlled via the postMessage API to the iframe -->
      <iframe
        id="yt-iframe"
        src="https://www.youtube.com/embed/{yt_id}?autoplay=1&enablejsapi=1&controls=1"
        allow="autoplay; encrypted-media"
        allowfullscreen>
      </iframe>
    </div>
    <div class="info">
      <p class="now-playing-label">Now Playing</p>
      <p class="now-playing-text">YouTube Music</p>
      <p class="tip-text">Try a lo-fi playlist for best results</p>
    </div>
    <div id="mini-controls">
      <button class="mini-btn" id="play-btn" onclick="togglePlayPause()" title="Play / Pause">⏸</button>
    </div>
    <button id="toggle-video" onclick="toggleVideo()">🙈 Hide video</button>
  </div>
  <div class="volume-row">
    <span class="vol-icon">🔈</span>
    <input type="range" id="vol-slider" min="0" max="100" value="100" oninput="onVolume(this.value)" />
    <span class="vol-icon">🔊</span>
    <span class="vol-pct" id="vol-pct">100%</span>
  </div>
</div>

<script>
  // ── Volume via YouTube postMessage API ─────────────────────────────────
  // This is the only cross-origin safe way to control YT volume from a sandboxed iframe.
  // We post a "setVolume" command directly to the YouTube iframe's content window.

  var iframe = document.getElementById('yt-iframe');

  // Wait for the iframe to load before sending commands
  iframe.addEventListener('load', function() {{
    // Set initial volume to 100
    sendYTCommand('setVolume', [100]);
  }});

  function sendYTCommand(func, args) {{
    iframe.contentWindow.postMessage(JSON.stringify({{
      event: 'command',
      func: func,
      args: args || []
    }}), '*');
  }}

  function onVolume(val) {{
    document.getElementById('vol-pct').textContent = val + '%';
    sendYTCommand('setVolume', [parseInt(val)]);
    // also mute/unmute based on value
    if (parseInt(val) === 0) {{
      sendYTCommand('mute', []);
    }} else {{
      sendYTCommand('unMute', []);
    }}
  }}

  // ── Hide / show video ──────────────────────────────────────────────────
  var videoVisible = true;
  var isPlaying    = true;

  function toggleVideo() {{
    videoVisible = !videoVisible;
    const wrap        = document.getElementById('video-wrap');
    const btn         = document.getElementById('toggle-video');
    const miniControls = document.getElementById('mini-controls');
    wrap.classList.toggle('hidden', !videoVisible);
    btn.textContent = videoVisible ? '🙈 Hide video' : '👁 Show video';
    miniControls.style.display = videoVisible ? 'none' : 'flex';
  }}

  function togglePlayPause() {{
    if (isPlaying) {{
      sendYTCommand('pauseVideo', []);
      document.getElementById('play-btn').textContent = '▶';
    }} else {{
      sendYTCommand('playVideo', []);
      document.getElementById('play-btn').textContent = '⏸';
    }}
    isPlaying = !isPlaying;
  }}
</script>
</body>
</html>
""", height=155)

# ── Mode buttons ──────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, label in zip([c1, c2, c3], MODES):
    with col:
        if st.button(label, key=f"mode_{label}", use_container_width=True):
            st.session_state.mode = label
            st.rerun()

# ── Timer widget ──────────────────────────────────────────────────────────────
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
  body {{ background:transparent; font-family:'DM Sans',sans-serif; }}
  .glass {{
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 24px; padding: 2rem 2rem 1.5rem; backdrop-filter: blur(16px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.35); margin-bottom: 1rem; text-align: center;
  }}
  .timer-label {{ font-size:0.8rem; letter-spacing:0.2em; text-transform:uppercase; color:rgba(240,236,228,0.6); margin-bottom:0.75rem; }}
  .timer-row {{ display:flex; align-items:center; justify-content:center; gap:1rem; }}
  .adj-btn {{
    background:rgba(255,255,255,0.10); border:1px solid rgba(255,255,255,0.22);
    color:#f0ece4; border-radius:10px; width:2.6rem; height:2.6rem; font-size:1.4rem;
    cursor:pointer; transition:all 0.2s; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; font-family:'DM Sans',sans-serif;
  }}
  .adj-btn:hover {{ background:rgba(246,161,75,0.3); border-color:#f6a14b; }}
  .timer-wrap {{ min-width:11rem; display:flex; flex-direction:column; align-items:center; }}
  #timer-display {{
    font-family:'DM Serif Display',serif; font-size:5.5rem; line-height:1; color:#fff;
    text-shadow:0 0 40px rgba(255,200,120,0.4); cursor:pointer; border-radius:8px;
    padding:0.1rem 0.3rem; transition:background 0.2s; white-space:nowrap; border:2px solid transparent;
  }}
  #timer-display:hover {{ background:rgba(255,255,255,0.07); }}
  #timer-input {{
    font-family:'DM Serif Display',serif; font-size:5.5rem; line-height:1; color:#fff;
    text-shadow:0 0 40px rgba(255,200,120,0.4); background:rgba(255,255,255,0.07);
    border:2px solid #f6a14b; border-radius:8px; padding:0.1rem 0.3rem;
    text-align:center; width:100%; outline:none; display:none;
  }}
  .edit-hint {{ font-size:0.72rem; color:rgba(240,236,228,0.45); margin-top:0.35rem; min-height:1em; letter-spacing:0.05em; text-align:center; }}
  .progress-wrap {{ width:100%; height:4px; background:rgba(255,255,255,0.12); border-radius:99px; margin:1.25rem 0 0; overflow:hidden; }}
  #progress-fill {{ height:100%; background:linear-gradient(90deg,#f6a14b,#e86d4b); border-radius:99px; width:0%; transition:width 0.9s linear; }}
  .controls {{ display:flex; justify-content:center; gap:0.75rem; margin-top:1rem; }}
  .timer-btn {{
    background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.25);
    color:#f0ece4; border-radius:12px; padding:0.55rem 1.8rem; font-size:0.9rem;
    letter-spacing:0.05em; cursor:pointer; font-family:'DM Sans',sans-serif; transition:all 0.2s;
  }}
  .timer-btn:hover {{ background:rgba(246,161,75,0.3); border-color:#f6a14b; }}
  .pomodoro-count {{ text-align:center; color:rgba(240,236,228,0.7); font-size:0.95rem; margin-top:0.75rem; }}
</style>
</head>
<body>
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
  const STEP=5*60; let TOTAL={total_secs},secondsLeft=TOTAL,running=false,interval=null,editing=false,pomodoros={pomodoros};
  const display=document.getElementById('timer-display'),input=document.getElementById('timer-input'),
        hint=document.getElementById('edit-hint'),progress=document.getElementById('progress-fill'),
        startBtn=document.getElementById('start-btn'),resetBtn=document.getElementById('reset-btn'),
        plusBtn=document.getElementById('plus-btn'),minusBtn=document.getElementById('minus-btn'),
        pomoCount=document.getElementById('pomo-count');
  function fmt(s){{ return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }}
  function render(){{ display.textContent=fmt(secondsLeft); progress.style.width=(100*(1-secondsLeft/TOTAL))+'%'; }}
  function tick(){{
    if(secondsLeft>0){{ secondsLeft--; render(); }}
    else{{ clearInterval(interval); running=false; startBtn.textContent='▶ Start'; pomodoros++; pomoCount.textContent='🍅 × '+pomodoros; }}
  }}
  startBtn.addEventListener('click',function(){{
    if(editing) commitEdit();
    if(running){{ clearInterval(interval); running=false; startBtn.textContent='▶ Start'; }}
    else{{ interval=setInterval(tick,1000); running=true; startBtn.textContent='⏸ Pause'; }}
  }});
  resetBtn.addEventListener('click',function(){{ clearInterval(interval); running=false; secondsLeft=TOTAL; startBtn.textContent='▶ Start'; render(); }});
  plusBtn.addEventListener('click',function(){{ if(!running){{ TOTAL=Math.min(TOTAL+STEP,99*60); secondsLeft=TOTAL; render(); }} }});
  minusBtn.addEventListener('click',function(){{ if(!running){{ TOTAL=Math.max(TOTAL-STEP,STEP); secondsLeft=TOTAL; render(); }} }});
  function parseTime(raw){{
    const val=raw.trim().toLowerCase(); if(!val) return null;
    if(/^\d{{1,2}}:\d{{2}}$/.test(val)){{ const[m,s]=val.split(':').map(Number); if(s<60) return m*60+s; }}
    if(/^\d+s$/.test(val)){{ const s=parseInt(val); if(s>0&&s<3600) return s; }}
    if(/^\d+$/.test(val)){{
      const n=parseInt(val);
      if(val.length<=3) return n*60;
      if(val.length===4){{ const m=parseInt(val.slice(0,2)),s=parseInt(val.slice(2)); if(s<60) return m*60+s; }}
      if(val.length===5){{ const m=parseInt(val.slice(0,3)),s=parseInt(val.slice(3)); if(s<60) return m*60+s; }}
      return n*60;
    }}
    return null;
  }}
  display.addEventListener('click',function(){{
    if(running) return; editing=true; input.value=fmt(secondsLeft);
    display.style.display='none'; input.style.display='block';
    hint.textContent='25=25min · 1000=10:00 · 30s=30sec · Enter to confirm';
    input.focus(); input.select();
  }});
  function commitEdit(){{
    editing=false; const parsed=parseTime(input.value);
    if(parsed&&parsed>0&&parsed<=99*60){{ TOTAL=parsed; secondsLeft=TOTAL; }}
    input.style.display='none'; display.style.display='block';
    hint.textContent='click timer to edit'; render();
  }}
  input.addEventListener('keydown',function(e){{
    if(e.key==='Enter') commitEdit();
    if(e.key==='Escape'){{ editing=false; input.style.display='none'; display.style.display='block'; hint.textContent='click timer to edit'; }}
  }});
  input.addEventListener('blur',function(){{ if(editing) commitEdit(); }});
  render();
</script>
</body>
</html>
""", height=310)

# ── Task list ─────────────────────────────────────────────────────────────────
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
