"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function RoomForm() {
  const [roomno, setRoomno] = useState("");
  const [seatcap, setSeatcap] = useState("");
  const [rooms, setRooms] = useState([]);

  // Fetch existing instructors
  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/rooms");
      setRooms(res.data);
    } catch (error) {
      console.error("Error fetching instructors:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:5000/rooms", {roomno,seatcap});
      alert("Room added successfully");
      setRoomno("");
      setSeatcap("");
      fetchRooms(); // Refresh the instructor list
    } catch (error) {
      alert("Failed to add instructor");
      console.error(error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <Card className="w-96 p-6 bg-gray-800">
        <CardHeader>
          <CardTitle className="text-center text-xl">Add Room</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="uid" className="text-white">Room Number</Label>
              <Input
                type="text"
                id="roomno"
                value={roomno}
                onChange={(e) => setRoomno(e.target.value)}
                className="w-full p-2 mt-1 bg-gray-700 text-white"
                required
              />
            </div>
            <div>
              <Label htmlFor="name" className="text-white">Seat Capacity</Label>
              <Input
                type="text"
                id="seatcap"
                value={seatcap}
                onChange={(e) => setSeatcap(e.target.value)}
                className="w-full p-2 mt-1 bg-gray-700 text-white"
                required
              />
            </div>
            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
              Add Room
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Displaying Instructors List */}
      <div className="mt-8 w-96">
        <h2 className="text-center text-lg font-semibold mb-2">Room List</h2>
        <ul className="bg-gray-800 p-4 rounded shadow">
          {rooms.length > 0 ? (
            rooms.map((room) => (
              <li key={room.id} className="p-2 border-b border-gray-700">
                {room.roomno} - {room.seatcap}
              </li>
            ))
          ) : (
            <p className="text-center">No rooms found.</p>
          )}
        </ul>
      </div>
    </div>
  );
}
