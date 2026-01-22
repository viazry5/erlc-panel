import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

function Card({ title, children }) {
  return (
    <div style={{padding:16, border:"1px solid #1f2933", borderRadius:18, background:"#020617"}}>
      <div style={{color:"#9ca3af", fontSize:12}}>{title}</div>
      <div style={{marginTop:10}}>{children}</div>
    </div>
  );
}

export default function App() {
  const [server, setServer] = useState(null);
  const [players, setPlayers] = useState([]);
  const [kills, setKills] = useState([]);
  const [err, setErr] = useState("");

  async function load() {
    try {
      setErr("");
      const [s, p, k] = await Promise.all([
        fetch(`${API}/api/server`).then(r => r.json()),
        fetch(`${API}/api/players`).then(r => r.json()),
        fetch(`${API}/api/kills`).then(r => r.json()),
      ]);
      setServer(s);
      setPlayers(Array.isArray(p) ? p : []);
      setKills(Array.isArray(k) ? k : []);
    } catch (e) {
      setErr(String(e));
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{minHeight:"100vh", background:"#0b0b0f", color:"white", display:"flex"}}>

      {/* Sidebar */}
      <div style={{width:260, borderRight:"1px solid #1f2933", padding:18}}>
        <h2 style={{margin:0}}>Liberty County Panel</h2>
        <p style={{marginTop:6, color:"#9ca3af", fontSize:12}}>ER:LC Dashboard</p>

        <div style={{marginTop:20, display:"grid", gap:10}}>
          <div style={{padding:"10px 12px", borderRadius:12, background:"#111827"}}>Dashboard</div>
          <div style={{padding:"10px 12px", borderRadius:12, background:"#0f172a"}}>Players</div>
          <div style={{padding:"10px 12px", borderRadius:12, background:"#0f172a"}}>Kill Logs</div>
          <div style={{padding:"10px 12px", borderRadius:12, background:"#0f172a"}}>Staff</div>
        </div>

        <button
          onClick={load}
          style={{
            marginTop:18, width:"100%", padding:"10px 12px",
            borderRadius:12, background:"#16a34a", border:"none",
            color:"white", fontWeight:700, cursor:"pointer"
          }}
        >
          Refresh
        </button>

        {err && <div style={{marginTop:10, color:"#f87171", fontSize:12}}>Error: {err}</div>}
      </div>

      {/* Main */}
      <div style={{flex:1, padding:22}}>
        <h1 style={{marginTop:0}}>Overview</h1>
        <p style={{color:"#9ca3af"}}>Live ERLC data refreshes every 5 seconds.</p>

        <div style={{display:"grid", gridTemplateColumns:"repeat(3, minmax(0,1fr))", gap:14, marginTop:18}}>
          <Card title="Server Info">
            {server ? (
              <div style={{fontSize:14, color:"#e5e7eb", lineHeight:1.6}}>
                <div><b>Name:</b> {server.Name}</div>
                <div><b>Players:</b> {server.CurrentPlayers} / {server.MaxPlayers}</div>
                <div><b>Join Code:</b> {server.JoinKey}</div>
              </div>
            ) : "Loading..."}
          </Card>

          <Card title="Players Online">
            <div style={{fontSize:34, fontWeight:800}}>{players.length}</div>
          </Card>

          <Card title="Recent Kills">
            <div style={{color:"#cbd5e1", fontSize:13, display:"grid", gap:6}}>
              {kills.slice(0, 6).map((k, i) => (
                <div key={i}>• {k.Killer ?? k.killer} → {k.Killed ?? k.killed}</div>
              ))}
              {kills.length === 0 && <div style={{color:"#9ca3af"}}>No kills yet</div>}
            </div>
          </Card>
        </div>

        {/* Player list */}
        <div style={{marginTop:16, padding:16, border:"1px solid #1f2933", borderRadius:18, background:"#020617"}}>
          <div style={{color:"#9ca3af", fontSize:12, marginBottom:10}}>Player List</div>

          <div style={{display:"flex", flexWrap:"wrap", gap:8}}>
            {players.map((p, i) => (
              <div key={i} style={{padding:"6px 10px", borderRadius:999, background:"#0f172a", border:"1px solid #1f2933", fontSize:12}}>
                {p.Username ?? p.Player ?? "Player"}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
