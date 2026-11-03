import { NavLink, Route, Routes } from "react-router-dom";
import ChatPanel from "./components/ChatPanel";
import Archive from "./pages/Archive";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import Tasks from "./pages/Tasks";

const NAV = [
  { to: "/", label: "לוח משימות", end: true },
  { to: "/archive", label: "ארכיון" },
  { to: "/settings", label: "הגדרות" },
  { to: "/profile", label: "פרופיל" },
];

// The chat panel sits outside <Routes>, so the conversation survives page changes.
export default function App() {
  return (
    <div className="shell">
      <div className="banner" role="status">
        גרסת הרצה – המערכת בשלבי הרצה, ייתכנו תקלות ושינויים.
      </div>
      <div className="app">
      <div className="main">
        <header className="top">
          <div className="brand">Foo Tasks</div>
          <nav className="nav" aria-label="ניווט ראשי">
            {NAV.map((n) => (
              <NavLink key={n.to} to={n.to} end={n.end}>
                {n.label}
              </NavLink>
            ))}
          </nav>
        </header>
        <main className="content">
          <Routes>
            <Route path="/" element={<Tasks />} />
            <Route path="/archive" element={<Archive />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
      </div>
      <ChatPanel />
      </div>
    </div>
  );
}
