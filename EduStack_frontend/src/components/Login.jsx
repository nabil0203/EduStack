import React from "react";
import { useAuth } from '../contexts/AuthProvider'

function Login() { 

    const { login } = useAuth();


    const handleSubmit = async (event) => {
        event.preventDefault();
        const values = {
            phone: event.target.phone.value,
            password: event.target.password.value
        }

        await login(values);
    }


    return (
       <div>
            <h2>Login</h2>

            <form onSubmit={handleSubmit}>  
                <input name="phone" type="text" placeholder = "Phone" />
                <input name="password" type="password" placeholder = "Password" />
                <input type="submit" value="Login" />


            </form>



       </div>
        
    )
}

export default Login