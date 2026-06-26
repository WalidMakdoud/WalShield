import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ArpScanner from "./pages/ArpScanner.jsx";
import PortScanerDetection from "./pages/port_scaner_detection.jsx";
import DosScanne from "./pages/Dos_Scanner.jsx";
import DeauthScanner from "./pages/Deauth_Scanner.jsx";
import Logs from "./pages/Logs.jsx";
import Settings from "./pages/Settings.jsx";

function App() {
  return (
    <Routes>

      <Route path="/" element={<Login />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/arp" element={<ArpScanner />} />

      <Route path="/portscanner" element={<PortScanerDetection />} />

      <Route path="/dos" element={<DosScanne />} />

      <Route path="/deauth" element={<DeauthScanner />} />

      <Route path="/logs" element={<Logs />} />

      <Route path="/settings" element={<Settings />} />

    </Routes>
  );
}

export default App;
