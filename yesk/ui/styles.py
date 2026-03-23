"""Ana Streamlit sayfası için gömülü CSS."""

from __future__ import annotations

APP_MAIN_CSS: str = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}

/* Hero Section with Dynamic Gradient */
.hero {
    background: linear-gradient(-45deg, #0d3b1e, #1b5e20, #2e7d32, #004d40);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    border-radius: 24px;
    padding: 40px 28px;
    text-align: center;
    color: #fff;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(46,125,50,0.3);
    position: relative;
    overflow: hidden;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    transform: rotate(30deg);
    pointer-events: none;
}
.hero h1 {font-size: clamp(1.55rem, 4vw + 0.5rem, 2.6rem); font-weight: 800; margin: 0; letter-spacing: -1px; text-shadow: 0 2px 10px rgba(0,0,0,0.2); position: relative;}
.hero p {opacity: 0.9; margin-top: 8px; font-size: 1.1rem; font-weight: 500; position: relative;}
.hero .badge-container { margin-top: 15px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; position: relative; }
.hero .badge {
    background: rgba(255,255,255,0.2); backdrop-filter: blur(10px);
    padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;
    border: 1px solid rgba(255,255,255,0.3); letter-spacing: 0.5px;
}

/* Glassmorphism Cards */
.cards {display: flex; gap: 16px; margin-bottom: 30px; flex-wrap: wrap;}
.card {
    flex: 1; min-width: 140px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(150, 150, 150, 0.2);
    border-radius: 20px;
    padding: 20px 14px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    position: relative;
    overflow: hidden;
}
[data-theme="dark"] .card { background: rgba(30, 30, 30, 0.5); border: 1px solid rgba(255,255,255,0.08); }
[data-theme="light"] .card { background: rgba(255, 255, 255, 0.7); }

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 40px rgba(46,125,50,0.15);
    border-color: rgba(46,125,50,0.4);
}
.card .icon {font-size: 1.8rem; margin-bottom: 8px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));}
.card .lbl {font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; font-weight: 600;}
.card .val {font-size: 1.8rem; font-weight: 800; color: #2e7d32; margin: 4px 0;}
.card .unit {font-size: 0.75rem; opacity: 0.6; font-weight: 500;}
.card.total {
    border: 2px solid #2e7d32;
    background: rgba(46,125,50,0.05);
}
.card.total::after {
    content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: shine 3s infinite;
}
@keyframes shine {
    100% {left: 200%;}
}

/* Tabs styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    padding-bottom: 10px; margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    padding: 10px 20px;
    border-radius: 12px;
    background-color: transparent;
    border: 1px solid transparent;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(46,125,50,0.1) !important;
    border: 1px solid rgba(46,125,50,0.3) !important;
    color: #2e7d32 !important;
    font-weight: 700 !important;
}

/* Story Share Card */
.story-card-wrapper { display: flex; justify-content: center; margin: 40px 0; }
.story-card {
    background: linear-gradient(135deg, #111, #222);
    border-radius: 24px; padding: 30px; color: white;
    text-align: center; width: 100%; max-width: 350px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    position: relative; overflow: hidden;
}
.story-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
    background: linear-gradient(90deg, #4caf50, #81c784, #2e7d32);
}
.story-card h2 { margin: 0 0 5px 0; font-size: 1.3rem; font-weight: 800; color: #81c784; }
.story-card .score-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }
.story-card .big-score { font-size: 4rem; font-weight: 900; margin: 5px 0; line-height: 1; letter-spacing: -2px; }
.story-card .unit { font-size: 1rem; opacity: 0.8; font-weight: 500; }
.story-card .badge-text { font-size: 1.1rem; font-weight: 700; padding: 6px 16px; background: rgba(255,255,255,0.1); border-radius: 20px; display: inline-block; margin: 15px 0; border: 1px solid rgba(255,255,255,0.2); }
.story-card .tag { font-size: 0.9rem; color: #aaa; margin-top: 10px; font-weight: 500; }

.percentile-box {
    background: linear-gradient(135deg, rgba(46,125,50,0.15), rgba(46,125,50,0.05));
    border: 1px solid rgba(46,125,50,0.3);
    padding: 24px; border-radius: 16px; text-align: center; margin-bottom: 30px;
    box-shadow: 0 4px 20px rgba(46,125,50,0.1);
}
.percentile-box h3 { margin: 0; font-size: 1.5rem; color: #2e7d32; font-weight: 800; }

.cta-box{background:rgba(46,125,50,.1);border:2px solid rgba(46,125,50,.3);border-radius:20px;padding:30px;text-align:center;margin:30px 0}
.cta-box h3{color:#2e7d32;margin-top:0;font-weight:800;font-size:1.8rem}
.cta-box p{font-size:1.1rem;opacity:0.9}
.cta-btn{display:inline-block;background:linear-gradient(45deg, #2e7d32, #1b5e20);color:#fff !important;text-decoration:none;padding:14px 32px;border-radius:30px;font-weight:700;margin-top:15px;transition:.3s;box-shadow:0 8px 20px rgba(46,125,50,.4)}
.cta-btn:hover{transform:translateY(-3px);box-shadow:0 12px 25px rgba(46,125,50,.5)}
.recommendation{background:rgba(255,193,7,.1);border-left:5px solid #ffca28;padding:20px;border-radius:12px;margin-bottom:24px;box-shadow:0 4px 15px rgba(0,0,0,.05); border: 1px solid rgba(255,193,7,.2);}
.recommendation strong{color:#f57c00;font-size:1.2rem;display:inline-block;margin-bottom:8px}

@media (max-width: 768px){
    .cards{gap:12px;}
    .card{min-width:45%; padding: 16px 10px;}
    .hero{padding:30px 20px;}
    .story-card { margin: 20px auto; }
}
@media (prefers-reduced-motion: reduce) {
    .hero { animation: none !important; background-size: 100% 100% !important; }
    .card.total::after { animation: none !important; }
    .card:hover { transform: none !important; }
    .cta-btn:hover { transform: none !important; }
}
.stTabs [data-baseweb="tab"]:focus-visible {
    outline: 2px solid #2e7d32 !important;
    outline-offset: 2px !important;
}
a.cta-btn:focus-visible, button:focus-visible {
    outline: 2px solid #81c784;
    outline-offset: 2px;
}
footer{visibility:hidden}
</style>
"""
