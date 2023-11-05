// Sample data for bookings (you can replace this with actual booking data)
const bookings = [
    { name: "Booking 1", date: "2023-04-15" },
    { name: "Booking 2", date: "2023-04-20" },
    // Add more booking objects here
];

const bookingCardsContainer = document.getElementById("booking-cards");
const noBookingCard = document.querySelector(".no-booking-card");

// Sort bookings by date (ascending order)
bookings.sort((a, b) => new Date(a.date) - new Date(b.date));

if (bookings.length > 0) {
    noBookingCard.style.display = "none"; // Hide the "no bookings" card
    bookings.forEach((booking) => {
        const card = document.createElement("div");
        card.className = "booking-card";
        card.innerHTML = `
            <h2>${booking.name}</h2>
            <p>Date: ${booking.date}</p>
            <!-- Add more booking details here -->
        `;
        bookingCardsContainer.appendChild(card);
    });
} else {
    noBookingCard.style.display = "block"; // Display the "no bookings" card
}
/*
// Get the upcoming hotel reservations from the Amadeus Hotel API
// and store them in an array
const upcomingReservations = [];

// Sort the upcoming reservations by date, soonest first
upcomingReservations.sort((a, b) => a.checkInDate - b.checkInDate);

// Display the upcoming reservations in the card container
const cardContainer = document.querySelector('.card-container');
for (const reservation of upcomingReservations) {
  const card = document.createElement('div');
  card.classList.add('card');

  const title = document.createElement('h3');
  title.classList.add('title');
  title.textContent = reservation.hotelName;
  card.appendChild(title);

  const subtitle = document.createElement('p');
  subtitle.classList.add('subtitle');
  subtitle.textContent = reservation.roomType;
  card.appendChild(subtitle);

  const date = document.createElement('p');
  date.classList.add('date');
  date.textContent = `${reservation.checkInDate} - ${reservation.checkOutDate}`;
  card.appendChild(date);

  cardContainer.appendChild(card);
}

// If there are no upcoming reservations, display a white card with a button
// that reroutes the user to the index page
if (upcomingReservations.length === 0) {
  const whiteCard = document.createElement('div');
  whiteCard.classList.add('white-card');

  const text = document.createElement('p');
  text.classList.add('text');
  text.textContent = 'Looks like you have no upcoming bookings - Let\'s go fix that!';
  whiteCard.appendChild(text);

  const button = document.createElement('button');
  button.classList.add('button');
  button.textContent = 'Book a hotel now';
  button.addEventListener('click', () => {
    window.location.href = 'index.html';
  });
  whiteCard.appendChild(button);

  cardContainer.appendChild(whiteCard);
}
*/