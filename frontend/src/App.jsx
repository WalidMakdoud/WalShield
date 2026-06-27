import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ArpScanner from "./pages/ArpScanner.jsx";
import PortScanerDetection from "./pages/port_scaner_detection.jsx";
import DosScanne from "./pages/Dos_Scanner.jsx";
import DeauthScanner from "./pages/Deauth_Scanner.jsx";
import Logs from "./pages/Logs.jsx";
import Settings from "./pages/Settings.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

function App() {
  return (
    <Routes>

      <Route path="/" element={<Login />} />

      <Route path="/dashboard" element={ <ProtectedRoute><Dashboard /></ProtectedRoute> } />

      <Route path="/arp" element={ <ProtectedRoute><ArpScanner /></ProtectedRoute>} />

      <Route path="/portscanner" element={ <ProtectedRoute><PortScanerDetection /></ProtectedRoute>} />

      <Route path="/dos" element={ <ProtectedRoute><DosScanne /></ProtectedRoute>} />

      <Route path="/deauth" element={ <ProtectedRoute><DeauthScanner /></ProtectedRoute>} />

      <Route path="/logs" element={ <ProtectedRoute><Logs /></ProtectedRoute>} />

      <Route path="/settings" element={ <ProtectedRoute><Settings /></ProtectedRoute>} />

    </Routes>
  );
}

export default App;
