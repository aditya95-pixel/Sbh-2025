"use client";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold mb-6">Welcome to Timetable Scheduler</h1>
      <div className="space-x-4">
        <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded">Login</Link>
        <Link href="/register" className="bg-green-500 text-white px-4 py-2 rounded">Register</Link>
      </div>
    </div>
  );
}
