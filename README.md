# SmartBTech USTP

## Project Overview
SmartBTech USTP is a smart monitoring system that provides real-time tracking of power usage in buildings. The system integrates Django REST framework for backend API services, React for the web dashboard, and React Native (Expo) for the mobile application. WebSockets are used to stream live sensor data to the dashboard.

## Features
- **Real-Time Monitoring**: Display power, voltage, and current data from multiple sensors.
- **User Authentication**: Secure login system using JWT.
- **Web Dashboard**: Built using React and Material UI.
- **Mobile App**: Developed with React Native and Expo.
- **WebSocket Integration**: Enables live data updates.
- **Device & Building Management**: Users can add and manage buildings and smart devices.
- **Analytics & Charts**: Visual representation of power consumption.

## System Requirements
- Python 3.9+
- Node.js 18+
- Expo CLI (for mobile development)
- Vite (for web development)
- PostgreSQL or SQLite (for the backend database)

## Installation & Setup

### Backend (Django)
1. Clone the repository:
   ```bash
   git clone [<repository_url>](https://github.com/ronelnale/SmartBTech/tree/91766e9d9bb0e757d4157604a2d9d20ac2d744f3/Capstone/capstone)
   cd capstone
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

### Web Dashboard (React + Vite)
1. Navigate to the frontend folder:
   ```bash
   cd SmartBtech-Web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Mobile App (React Native + Expo)
1. Navigate to the mobile project folder:
   ```bash
   cd SmartBtech-Mobile
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Expo development server:
   ```bash
   npx expo start
   ```

## API Endpoints
- **Authentication**:
  - `POST /api/token/` – Obtain JWT token
  - `POST /api/token/refresh/` – Refresh JWT token
- **Buildings**:
  - `GET /api/buildings/` – Retrieve all buildings
  - `POST /api/buildings/` – Add a new building
- **Devices**:
  - `GET /api/devices/` – Retrieve all smart devices
  - `POST /api/devices/` – Register a new smart device
- **WebSocket**:
  - Connect to `ws://192.168.1.61:8000/ws/sensors/` for real-time data streaming.

## Dependencies

### Mobile Dependencies
- `@react-navigation` (for navigation)
- `socket.io-client` (for WebSocket communication)
- `expo` (for development framework)
- `axios` (for API requests)

### Web Dependencies
- `react-router-dom` (for routing)
- `socket.io-client` (for real-time communication)
- `chart.js` (for visualizing analytics)
- `axios` (for handling API requests)
- `tailwindcss` (for styling)

## Contributing
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, reach out via email or through the project repository.

