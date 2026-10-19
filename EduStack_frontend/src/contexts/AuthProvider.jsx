import React from "react";
import { createContext, useContext } from "react";
import { registerUser, loginUser } from "../services/authService";                 // Import the register function from the API module



// Context for authentication state and functions
const AuthContext = createContext();



// hook to access the authentication context
export const useAuth = () => {
    const context = React.useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};



// provider component to wrap the application and provide authentication state and functions
const AuthProvider = ({ children }) => {


    const register = async (userdata) => {
        console.log("Registering Function", userdata)
        const res = await registerUser(userdata);
        console.log(res);
    };

    const login = async (userdata) => {
        console.log("Login Function", userdata)
        const res = await loginUser(userdata);
        localStorage.setItem("token", res.token);       // Store the token in local storage
        localStorage.setItem("refresh", res.refresh);   // Store the refresh token in local storage
    }

    const logout = async () => {
        console.log("Logout Function")
        localStorage.removeItem("token");                        // Remove the token from local storage
        localStorage.removeItem("refresh");                 // Remove the refresh token from local storage
    }




    return (
        <AuthContext.Provider value={{register, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;