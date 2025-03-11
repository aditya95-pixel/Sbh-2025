"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { jwtDecode } from "jwt-decode"; // Install with: npm install jwt-decode
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function Dashboard() {
  const [username, setUsername] = useState("");
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      router.push("/login");
      return;
    }

    try {
      const decoded = jwtDecode(storedToken);
      const currentTime = Date.now() / 1000;

      if (decoded.exp < currentTime) {
        alert("Session expired. Please log in again.");
        localStorage.removeItem("token");
        router.push("/login");
      } else {
        setUsername(decoded.user); // Extract username from token
      }
    } catch (error) {
      console.error("Invalid token:", error);
      router.push("/login");
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-900">
      <Card className="w-96 p-6">
        <CardHeader>
          <CardTitle className="text-center text-xl font-semibold">Dashboard</CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <p className="mb-4 text-lg text-white">Welcome, {username}!</p>
          <Button onClick={handleLogout} className="w-full bg-red-600 hover:bg-red-700">
            Logout
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
