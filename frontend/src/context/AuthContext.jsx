import {createContext, useContext, useState} from "react";

const AuthContext = createContext();

export function AuthProvider({children}) {

	const [isAuthenticated, setIsAuthenticated] = useState(
		localStorage.getItem("auth") === "true"
		);

	const login = (username, password) => {
		
		if(username === "admin" && password === "admin") {

			setIsAuthenticated(true);
			localStorage.setItem("auth", "true");
			return true;
		}
		return false;
	};


	const logout = () => {
		setIsAuthenticated(false);
		localStorage.removeItem("auth");
		

	};
	
	return (
		<AuthContext.Provider value={{isAuthenticated, login, logout}}>
			{children}
		</AuthContext.Provider>
	);
}

export const useAuth = () => useContext(AuthContext);