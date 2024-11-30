"use client"

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function Login() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false); // State to handle the loader

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true); // Show loader when clicked

        // Simulate a delay of 2 seconds before redirecting
        setTimeout(() => {
            setLoading(false);
            router.push('/home');
        }, 2000);
    };

    return (
        <div
            className="flex min-h-screen min-w-full justify-center items-center bg-cover bg-center transition-all duration-500"
            style={{
                backgroundImage: 'url("/background.jpg")',
                backgroundSize: 'cover'
            }}
        >
            {/* Loader */}
            {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50">
                    <div className="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12"></div>
                </div>
            )}

            {/* Login form */}
            <div className="w-full max-w-md p-8 space-y-6 bg-gray-800 bg-opacity-70 rounded-lg shadow-lg transform hover:scale-105 transition-transform duration-300">
                <h2 className="text-center text-3xl font-extrabold text-white">Login to Your Account</h2>
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-300">Email address</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            autoComplete="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full p-2 mt-1 text-gray-900 placeholder-gray-500 rounded-md focus:ring-red-500 focus:border-red-500 transition-all duration-300"
                            placeholder="Email"
                        />
                    </div>

                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-300">Password</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autoComplete="current-password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full p-2 mt-1 text-gray-900 placeholder-gray-500 rounded-md focus:ring-red-500 focus:border-red-500 transition-all duration-300"
                            placeholder="Password"
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all duration-300"
                    >
                        {loading ? 'Signing in...' : 'Login'}
                    </button>
                </form>
            </div>
        </div>
    );
}
