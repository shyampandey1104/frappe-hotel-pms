"""Hotel Property Management System (PMS) engine for Frappe / ERPNext."""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field


class Room(BaseModel):
    room_number: str
    room_type: str  # Deluxe, Suite, Executive, Standard
    base_rate: float
    status: str = "Available"  # Available, Occupied, Cleaning, Maintenance


class FolioCharge(BaseModel):
    charge_type: str  # Room Tariff, Restaurant, Laundry, Mini-bar
    amount: float
    tax_rate: float = 12.0  # GST %
    date: str


class Reservation(BaseModel):
    booking_id: str
    guest_name: str
    phone: str
    room_number: str
    check_in_date: str
    check_out_date: str
    status: str = "Confirmed"  # Confirmed, Checked-In, Checked-Out, Cancelled
    charges: List[FolioCharge] = []


class HotelPMSEngine:
    """Core hotel operations engine managing room inventory, bookings, and folios."""

    def __init__(self, rooms: List[Room]):
        self.rooms = {r.room_number: r for r in rooms}
        self.reservations: Dict[str, Reservation] = {}

    def calculate_stay_nights(self, check_in: str, check_out: str) -> int:
        d1 = datetime.strptime(check_in, "%Y-%m-%d").date()
        d2 = datetime.strptime(check_out, "%Y-%m-%d").date()
        return max(1, (d2 - d1).days)

    def check_in_guest(self, booking_id: str) -> bool:
        if booking_id not in self.reservations:
            return False
        res = self.reservations[booking_id]
        res.status = "Checked-In"
        if res.room_number in self.rooms:
            self.rooms[res.room_number].status = "Occupied"
        return True

    def add_charge_to_folio(self, booking_id: str, charge: FolioCharge) -> bool:
        if booking_id not in self.reservations:
            return False
        self.reservations[booking_id].charges.append(charge)
        return True

    def generate_final_invoice(self, booking_id: str) -> Dict[str, Any]:
        """Generate final guest checkout bill with GST tax breakdown."""
        if booking_id not in self.reservations:
            raise ValueError("Booking ID not found")

        res = self.reservations[booking_id]
        room = self.rooms.get(res.room_number)
        rate = room.base_rate if room else 2500.0
        nights = self.calculate_stay_nights(res.check_in_date, res.check_out_date)

        room_tariff_subtotal = rate * nights
        room_tax = room_tariff_subtotal * (0.12 if rate < 7500 else 0.18)

        extra_charges_subtotal = sum(c.amount for c in res.charges)
        extra_tax = sum(c.amount * (c.tax_rate / 100.0) for c in res.charges)

        grand_total = (room_tariff_subtotal + room_tax) + (extra_charges_subtotal + extra_tax)

        return {
            "invoice_number": f"INV-{booking_id}",
            "guest_name": res.guest_name,
            "room_number": res.room_number,
            "nights": nights,
            "room_tariff_subtotal": round(room_tariff_subtotal, 2),
            "room_tax": round(room_tax, 2),
            "extra_services_subtotal": round(extra_charges_subtotal, 2),
            "extra_services_tax": round(extra_tax, 2),
            "grand_total": round(grand_total, 2),
            "status": "Paid",
        }

    def get_occupancy_analytics(self) -> Dict[str, Any]:
        total_rooms = len(self.rooms)
        occupied_rooms = len([r for r in self.rooms.values() if r.status == "Occupied"])
        occupancy_rate = (occupied_rooms / total_rooms * 100.0) if total_rooms > 0 else 0.0
        return {
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": total_rooms - occupied_rooms,
            "occupancy_rate_percent": round(occupancy_rate, 1),
        }
