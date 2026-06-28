// DBMS Digest — Übersicht desktop widget (tabbed launcher + fresh items).
//
// 🏠 Home tab: up to 10 freshest items across all feeds (title + link).
// Topic tabs (Postgres / NoSQL / Distributed / Engines / Math) × type sub-tabs
// (Новости / Ресёрч / Компании / Личные / Статьи): each cell shows up to 5 fresh
// headlines pulled from that cell's sources, falling back to the curated source list
// when a feed is missing/offline.
//
// Data + fetching: build_widget_items.py (run as the command below). Pins & curated
// sources live in widget-data.json. Tabs are pure CSS (hidden radio + label); clicking
// needs Übersicht interaction (focus the desktop first).

import { run } from "uebersicht";

export const refreshFrequency = 60 * 60 * 1000; // hourly; the script caches ~90 min

// Fetch fresh items + merge with the curated data, print JSON. First run hits the
// network (~10-15s); the script caches, so later refreshes are instant.
export const command =
  `python3 "/Users/alena/dbms-digest/scripts/ubersicht/dbms-digest.widget/build_widget_items.py"`;

export const className = `
  top: 40px;
  right: 40px;
  width: 460px;
  box-sizing: border-box;
  padding: 16px 18px 18px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  color: #e8eef7;
  background: rgba(13, 27, 46, 0.92);
  border: 1px solid rgba(158, 197, 255, 0.18);
  border-radius: 16px;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  line-height: 1.4;

  h1 { margin: 0 0 10px; font-size: 15px; font-weight: 700; color: #fff; }
  h1 .upd { font-weight: 400; font-size: 11px; color: #7f93ad; margin-left: 6px; }
  h1 .dbw-refresh { cursor: pointer; pointer-events: auto; color: #9ec5ff; font-size: 13px;
                    margin-left: 8px; opacity: .65; }
  h1 .dbw-refresh:hover { opacity: 1; }

  .dbw-pins { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px; }
  .dbw-pins label, .dbw-pins a {
    font-size: 10.5px; font-weight: 600; padding: 2px 8px; border-radius: 6px;
    color: #9ec5ff; background: rgba(158,197,255,.10); text-decoration: none;
    cursor: pointer; pointer-events: auto; white-space: nowrap;
  }
  .dbw-pins a { opacity: .72; }            /* plain link (no live feed) — opens on click */
  .dbw-pins label:hover, .dbw-pins a:hover { background: rgba(158,197,255,.22); color: #fff; }
  .dbw-pinbody { margin: 0 0 13px; padding-bottom: 12px;
                 border-bottom: 1px solid rgba(158,197,255,.12); }
  .dbw-pinpanel { display: none; padding-top: 6px; }
  .dbw-close {
    display: inline-block; font-size: 10px; font-weight: 600; color: #8aa0bd;
    background: rgba(158,197,255,.10); border-radius: 5px; padding: 1px 7px;
    cursor: pointer; pointer-events: auto; margin-bottom: 7px;
  }
  .dbw-close:hover { background: rgba(158,197,255,.22); color: #fff; }

  input.dbw-r { display: none; }

  .dbw-tabs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
  .dbw-tabs label {
    font-size: 12px; font-weight: 600; padding: 4px 11px; border-radius: 999px;
    color: #aebfd4; background: rgba(158, 197, 255, 0.07);
    border: 1px solid rgba(158, 197, 255, 0.12); cursor: pointer; pointer-events: auto;
  }
  .dbw-tabs label:hover { color: #fff; }

  .dbw-panel { display: none; }

  .dbw-subtabs { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 10px;
                 border-bottom: 1px solid rgba(158, 197, 255, 0.14); padding-bottom: 7px; }
  .dbw-subtabs label {
    font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px;
    color: #7f93ad; cursor: pointer; pointer-events: auto;
    border-bottom: 2px solid transparent; padding-bottom: 6px; margin-bottom: -8px;
  }
  .dbw-subtabs label:hover { color: #cfe; }

  .dbw-cell { display: none; }
  ul.dbw-list { margin: 0; padding: 0; list-style: none; }
  ul.dbw-list li { font-size: 12.5px; margin: 0 0 7px; padding-left: 13px; position: relative; }
  ul.dbw-list li:before { content: "›"; position: absolute; left: 0; color: #5b7aa8; }
  ul.dbw-list a { color: #d6e2f2; text-decoration: none; pointer-events: auto; }
  ul.dbw-list a:hover { color: #fff; }
  .dbw-srctag { font-size: 9.5px; color: #6f819a; margin-left: 5px; white-space: nowrap; }
  .dbw-empty { font-size: 12px; color: #6f819a; padding-left: 2px; }
  .dbw-ai { cursor: pointer; pointer-events: auto; margin-left: 6px; opacity: .5; font-size: 11px; }
  .dbw-ai:hover { opacity: 1; }
  .dbw-sum { display: none; margin: 5px 0 8px 13px; padding: 7px 10px; font-size: 12px;
             line-height: 1.45; color: #cfe0f4; background: rgba(158,197,255,.07);
             border-left: 2px solid #9ec5ff; border-radius: 5px; white-space: pre-wrap; }
  .dbw-sumclose { float: right; margin-left: 8px; cursor: pointer; pointer-events: auto;
                  color: #8aa0bd; font-size: 11px; }
  .dbw-sumclose:hover { color: #fff; }
`;

const esc = (s) => String(s == null ? "" : s);

// Last live build time (unix seconds → "YYYY-MM-DD HH:MM", local) for the header.
const fmtBuilt = (ts) => {
  if (!ts) return "";
  const d = new Date(ts * 1000);
  const p = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
};

// ✨ button → Claude summary of one item (Übersicht runs the script via run()).
const SUMMARIZE = "/Users/alena/dbms-digest/scripts/ubersicht/dbms-digest.widget/summarize.py";
const CACHE = "/Users/alena/dbms-digest/scripts/ubersicht/dbms-digest.widget/.widget-live-cache.json";
// ⟳ button → drop the cache and force an immediate fresh rebuild + redraw.
const doRefresh = () =>
  run(`rm -f ${sh(CACHE)}; osascript -e 'tell application "Übersicht" to refresh'`)
    .catch((err) => console.error("dbms-digest ⟳:", err));
const sh = (s) => `'${String(s == null ? "" : s).replace(/'/g, "'\\''")}'`;
// ✨ click → fill the per-item .dbw-sum box inline (with a ✕ to hide it).
const doSummary = (e, it) => {
  const li = e.target && e.target.closest && e.target.closest("li");
  const box = li && li.querySelector(".dbw-sum");
  if (!box) return;
  const fill = (text) => {
    box.innerHTML = "";
    const close = document.createElement("span");
    close.className = "dbw-sumclose";
    close.textContent = "✕";
    close.onclick = (ev) => { ev.stopPropagation(); box.style.display = "none"; box.innerHTML = ""; };
    const t = document.createElement("span");
    t.textContent = text;
    box.appendChild(close);
    box.appendChild(t);
  };
  box.style.display = "block";
  fill("⏳ выжимка…");
  run(`DBMS_SUMMARY_INLINE=1 python3 ${sh(SUMMARIZE)} ${sh(it.u)} ${sh(it.t)}`)
    .then((out) => fill((out || "").trim() || "(пусто)"))
    .catch((err) => fill("ошибка: " + err));
};

// A cell may be an array of sources (no live data yet) or {sources, fresh}.
const cellOf = (c) => {
  if (Array.isArray(c)) return { sources: c, fresh: [] };
  return { sources: (c && c.sources) || [], fresh: (c && c.fresh) || [] };
};

const list = (items, withSrc) => (
  <ul className="dbw-list">
    {items.map((it, j) => (
      <li key={j}>
        <a href={it.u}>{esc(it.t)}</a>
        {withSrc && it.src ? <span className="dbw-srctag">{esc(it.src)}</span> : null}
        <span className="dbw-ai" onClick={(e) => doSummary(e, it)} title="Краткая выжимка (Claude)">✨</span>
        <div className="dbw-sum" />
      </li>
    ))}
  </ul>
);

export const render = ({ output }) => {
  let data;
  try { data = JSON.parse(output); } catch (e) { data = null; }
  if (!data || !data.topics) {
    return <div><h1>DBMS Digest</h1><div className="dbw-empty">Loading… (first fetch can take ~15s)</div></div>;
  }

  const types = data.types || [];
  const home = data.home || [];

  // Tabs = Home + each topic.
  const tabs = [{ id: "home", label: "🏠 Home" }, ...data.topics];

  const firstType = (tp) => {
    const t = types.find((ty) => {
      const c = cellOf(tp.cells[ty.id]);
      return c.fresh.length || c.sources.length;
    });
    return (t || types[0] || { id: "" }).id;
  };

  // Visibility wiring (computed from data so it matches whatever tabs exist).
  const rules = [];
  tabs.forEach((tp) => {
    rules.push(`#dbw-topic-${tp.id}:checked ~ .dbw-body .dbw-panel-${tp.id}{display:block}`);
    rules.push(`#dbw-topic-${tp.id}:checked ~ .dbw-tabs label[for=dbw-topic-${tp.id}]{background:rgba(158,197,255,.22);color:#fff;border-color:rgba(158,197,255,.4)}`);
  });
  data.topics.forEach((tp) => {
    types.forEach((ty) => {
      rules.push(`#dbw-type-${tp.id}-${ty.id}:checked ~ .dbw-subbody .dbw-cell-${tp.id}-${ty.id}{display:block}`);
      rules.push(`#dbw-type-${tp.id}-${ty.id}:checked ~ .dbw-subtabs label[for=dbw-type-${tp.id}-${ty.id}]{color:#fff;border-bottom-color:#9ec5ff}`);
    });
  });
  const pins = Array.isArray(data.pins) ? data.pins : [];
  const hasFresh = (p) => Array.isArray(p.fresh) && p.fresh.length > 0;
  pins.forEach((p, i) => {
    if (!hasFresh(p)) return;   // no-feed pins are plain links, not expandable
    rules.push(`#dbw-pin-${i}:checked ~ .dbw-pinbody .dbw-pinpanel-${i}{display:block}`);
    rules.push(`#dbw-pin-${i}:checked ~ .dbw-pins label[for=dbw-pin-${i}]{background:rgba(158,197,255,.30);color:#fff}`);
  });

  return (
    <div>
      <style dangerouslySetInnerHTML={{ __html: rules.join("\n") }} />
      <h1>DBMS Digest
        <span className="dbw-refresh" onClick={doRefresh} title="Обновить сейчас (свежий пересбор)">⟳</span>
        <span className="upd">обновлено {fmtBuilt(data.live_built) || esc(data.updated || "")}</span>
      </h1>

      {pins.some(hasFresh)
        ? <input className="dbw-r" type="radio" name="dbw-pin" id="dbw-pin-none" defaultChecked key="pr-none" />
        : null}
      {pins.map((p, i) => (
        hasFresh(p)
          ? <input className="dbw-r" type="radio" name="dbw-pin" id={`dbw-pin-${i}`} key={`pr-${i}`} />
          : null
      ))}
      {pins.length ? (
        <div className="dbw-pins">
          {pins.map((p, i) => (
            hasFresh(p)
              ? <label htmlFor={`dbw-pin-${i}`} key={`pl-${i}`}>{esc(p.t)}</label>
              : <a href={p.u} key={`pl-${i}`}>{esc(p.t)}</a>
          ))}
        </div>
      ) : null}
      {pins.some(hasFresh) ? (
        <div className="dbw-pinbody">
          {pins.map((p, i) => (
            hasFresh(p) ? (
              <div className={`dbw-pinpanel dbw-pinpanel-${i}`} key={`pp-${i}`}>
                <label className="dbw-close" htmlFor="dbw-pin-none">✕ свернуть</label>
                <ul className="dbw-list">
                  <li><a href={p.u}>Открыть {esc(p.t)} →</a></li>
                  {p.fresh.map((it, j) => (
                    <li key={j}>
                      <a href={it.u}>{esc(it.t)}</a>
                      {it.sub ? <span className="dbw-srctag">{esc(it.sub)}</span> : null}
                      <span className="dbw-ai" onClick={(e) => doSummary(e, it)} title="Краткая выжимка (Claude)">✨</span>
                      <div className="dbw-sum" />
                    </li>
                  ))}
                </ul>
              </div>
            ) : null
          ))}
        </div>
      ) : null}

      {tabs.map((tp, i) => (
        <input className="dbw-r" type="radio" name="dbw-topic" id={`dbw-topic-${tp.id}`}
               key={`tr-${tp.id}`} defaultChecked={i === 0} />
      ))}

      <div className="dbw-tabs">
        {tabs.map((tp) => (
          <label htmlFor={`dbw-topic-${tp.id}`} key={`tl-${tp.id}`}>{esc(tp.label)}</label>
        ))}
      </div>

      <div className="dbw-body">
        {/* Home panel: flat list of the 10 freshest items, no sub-tabs. */}
        <section className="dbw-panel dbw-panel-home" key="p-home">
          {home.length ? list(home, true)
                       : <div className="dbw-empty">Свежие новости подгружаются… обнови через минуту.</div>}
        </section>

        {data.topics.map((tp) => {
          const def = firstType(tp);
          return (
            <section className={`dbw-panel dbw-panel-${tp.id}`} key={`p-${tp.id}`}>
              {types.map((ty) => (
                <input className="dbw-r" type="radio" name={`dbw-type-${tp.id}`}
                       id={`dbw-type-${tp.id}-${ty.id}`} key={`yr-${tp.id}-${ty.id}`}
                       defaultChecked={ty.id === def} />
              ))}

              <div className="dbw-subtabs">
                {types.map((ty) => (
                  <label htmlFor={`dbw-type-${tp.id}-${ty.id}`} key={`yl-${tp.id}-${ty.id}`}>
                    {esc(ty.label)}
                  </label>
                ))}
              </div>

              <div className="dbw-subbody">
                {types.map((ty) => {
                  const c = cellOf(tp.cells[ty.id]);
                  const showFresh = c.fresh.length > 0;
                  const items = showFresh ? c.fresh : c.sources;
                  return (
                    <div className={`dbw-cell dbw-cell-${tp.id}-${ty.id}`} key={`c-${tp.id}-${ty.id}`}>
                      {items.length ? list(items, showFresh)
                                    : <div className="dbw-empty">— нет источников</div>}
                    </div>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
};
