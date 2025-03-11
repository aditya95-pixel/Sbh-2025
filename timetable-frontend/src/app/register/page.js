"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleRegister = async () => {
    try {
      await axios.post("http://127.0.0.1:5000/register", { username, password });
      alert("User registered successfully");
      router.push("/login");
    } catch (error) {
      alert(error.response?.data?.message || "Error registering user");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-900">
      <Card className="w-96 p-6">
        <CardHeader>
          <CardTitle className="text-center text-xl font-semibold">Register</CardTitle>
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
          <Button onClick={handleRegister} className="w-full bg-green-600 hover:bg-green-700">
            Register
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
