import { useNavigate } from "react-router-dom";

function Login() {

    const navigate = useNavigate();

    function login(e){

        e.preventDefault();

        navigate("/dashboard");

    }

    return (

        <div className="flex justify-center items-center h-screen bg-slate-900">

            <form
                onSubmit={login}
                className="bg-slate-800 p-10 rounded-xl w-96">

                <h1 className="text-3xl text-white mb-6">
                    WalShield Login
                </h1>

                <input
                    className="w-full p-3 mb-4 rounded bg-slate-700 text-white"
                    placeholder="Username"
                />

                <input
                    type="password"
                    className="w-full p-3 mb-6 rounded bg-slate-700 text-white"
                    placeholder="Password"
                />

                <button
                    className="bg-blue-600 w-full p-3 rounded text-white">

                    Login

                </button>

            </form>

        </div>

    );

}

export default Login;
