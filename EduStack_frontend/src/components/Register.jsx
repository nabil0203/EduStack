import React from 'react'
import { useAuth } from '../contexts/AuthProvider'


function Register() { 

    const { register } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const values = {
            first_name: e.target.firstName.value,
            last_name: e.target.lastName.value,
            username: e.target.username.value,
            phone: e.target.phone.value,
            password: e.target.password.value
        }
    

        await register(values);

    }


    return (
        <div>
            <h2>Register</h2>

            <form onSubmit={handleSubmit}>
                <input name="firstName" type="text" placeholder = "First Name" />
                <input name="lastName" type="text" placeholder = "Last Name" />
                <input name="username" type="text" placeholder = "Username" />
                <input name="phone" type="text" placeholder = "Phone" />
                <input name="password" type="password" placeholder = "Password" />
                <input type="submit" value="Register" />
            </form>
        
        </div>
    )
}

export default Register