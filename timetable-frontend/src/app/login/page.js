"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/login", { username, password });
      localStorage.setItem("token", res.data.access_token);
      router.push("/dashboard");
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-900">
      <Card className="w-96 p-6">
        <CardHeader>
          <CardTitle className="text-center text-xl font-semibold">Login</CardTitle>
        </CardHeader>
        <CardContent>
          <Input
            type="text"
            placeholder="Username"
            className="mb-4"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            className="mb-4"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button onClick={handleLogin} className="w-full bg-blue-600 hover:bg-blue-700">
            Login
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
