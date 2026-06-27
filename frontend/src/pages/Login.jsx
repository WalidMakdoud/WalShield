import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (login(username, password)) {
      navigate("/dashboard");
    } else {
      alert("Invalid username or password");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <div className="w-full max-w-md">
        <form
          onSubmit={handleLogin}
          className="bg-slate-900 border border-cyan-500/30 rounded-2xl shadow-2xl p-8"
        >
          <h1 className="text-4xl font-bold text-center text-cyan-400 mb-2">
            WalShield
          </h1>

          <p className="text-center text-slate-400 mb-8">
            Network Security Dashboard
          </p>

          <div className="mb-5">
            <label className="block text-slate-300 mb-2">
              Username
            </label>

            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>

          <div className="mb-6">
            <label className="block text-slate-300 mb-2">
              Password
            </label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-cyan-500 hover:bg-cyan-300 hover:text-black text-slate-900 font-bold py-3 rounded-lg transition duration-300 hover:cursor-pointer"
          >
            Login
          </button>

          <div className="mt-8 text-center text-sm text-slate-500">
            Default credentials:
            <br />
            <span className="text-cyan-400">admin / admin</span>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;