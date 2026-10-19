import axios from "axios";

const API_URL = "http://localhost:8000/api";



// registerUser function to send a POST request to the backend API for user registration
export async function registerUser(userData) {

    const response = await axios.post(`${API_URL}/register/`, userData);                    // calling the register endpoint of the backend API with user data
    return response.data;

}


// loginUser function to send a POST request to the backend API for user login
export async function loginUser(credentials) {
    try {
        const response = await axios.post(`${API_URL}/login/`, {
            phone: credentials.phone,                                   // Using phone field
            password: credentials.password
        });

        return {
            token: response.data.tokens.access,                                 // Assuming the backend returns an access token in the response
            refresh: response.data.tokens.refresh,                              // Assuming the backend returns a refresh token in the response     
            user: response.data.tokens.user,
            user:{
                id: response.data.user_id,
                username: response.data.username,
            }
        };
    }

    catch (error) {
        throw new Error(error.response?.data?.detail || 'Login failed');
    }
}

