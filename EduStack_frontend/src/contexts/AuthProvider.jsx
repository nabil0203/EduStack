import { createContext, useContext } from "react";



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
        console.log("Registering Function")
    };

    const login = async (userdata) => {
        console.log("Login Function")
    }

    const logout = async () => {
        console.log("Logout Function")
    }




    return (
        <AuthContext.Provider value={{register, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;