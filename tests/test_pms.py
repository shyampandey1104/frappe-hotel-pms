"""Unit tests for HotelPMSEngine."""

from pms.engine import HotelPMSEngine, Room, Reservation, FolioCharge


def test_hotel_booking_and_invoice():
    rooms = [
        Room(room_number="101", room_type="Deluxe", base_rate=3000.0),
        Room(room_number="102", room_type="Suite", base_rate=6000.0),
    ]
    pms = HotelPMSEngine(rooms)

    res = Reservation(
        booking_id="BK-991",
        guest_name="Shyam Pandey",
        phone="9876543210",
        room_number="101",
        check_in_date="2026-11-10",
        check_out_date="2026-11-12",  # 2 nights
    )
    pms.reservations["BK-991"] = res

    # Check In
    assert pms.check_in_guest("BK-991") is True
    assert pms.rooms["101"].status == "Occupied"

    # Add Room Service Folio Charge
    pms.add_charge_to_folio("BK-991", FolioCharge(charge_type="Restaurant", amount=850.0, tax_rate=5.0, date="2026-11-11"))

    # Invoice Check
    bill = pms.generate_final_invoice("BK-991")
    assert bill["nights"] == 2
    assert bill["room_tariff_subtotal"] == 6000.0  # 3000 * 2
    assert bill["grand_total"] > 6000.0
